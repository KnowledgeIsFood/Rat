#!/usr/bin/env python3
"""
One-shot / repeatable expander:
- Ensures creatures_master.csv has kind_zh on every row (inferred for legacy ids).
- Appends many additional 奇禽/异兽/鳞介 rows and 草木 rows (still one master CSV).

游戏主线经本为 **五藏山经**五篇；`haijing` / `dahuang_jing` 相关追加行属扩展占位时可删。

Re-run: python3 tools/expand_shanhaijing_master_csv.py
Then: python3 tools/emit_shanhaijing_chapters.py && python3 tools/render_shanhaijing_docs.py
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "shanhaijing" / "creatures_master.csv"

FIELDNAMES = [
    "chapter_group",
    "kind_zh",
    "id",
    "name_zh",
    "aliases_zh",
    "corpus_zh",
    "jing_zh",
    "section_zh",
    "mountain_zh",
    "literature_appearance_zh",
    "traits_effects_zh",
    "habitat_ecology_zh",
    "food_web_zh",
    "trophic_role_zh",
    "artistic_portrait_note_zh",
    "related_zh",
    "sources_note_zh",
]

# Legacy 64 ids → kind_zh (奇禽 / 异兽 / 鳞介 / 蛇蟒 / 神祇 / 祥瑞 / 凶兽 / 混形)
KIND_BY_ID: dict[str, str] = {
    "xingxing": "异兽",
    "baiyuan_tangting": "奇禽",
    "lushu": "异兽",
    "xuanguixuan": "鳞介",
    "lu_fish": "鳞介",
    "lei_beast": "异兽",
    "boyi": "异兽",
    "chichi_bird": "奇禽",
    "jiuwei_hu": "异兽",
    "guanguan_bird": "奇禽",
    "chiru_fish": "鳞介",
    "lili_li": "异兽",
    "zhu_bird": "奇禽",
    "changyou": "异兽",
    "huaihuai": "异兽",
    "zhi_fuyu": "凶兽",
    "huan_beast": "异兽",
    "gudiao": "凶兽",
    "xishou_xi": "异兽",
    "sishou_si": "异兽",
    "shanhai_xiang": "异兽",
    "quru": "奇禽",
    "hujiao": "鳞介",
    "fenghuang": "奇禽",
    "zhuanyu_fish": "鳞介",
    "yu_bird": "奇禽",
    "yuanchu": "奇禽",
    "xianyang": "异兽",
    "chonglong": "异兽",
    "bifang": "奇禽",
    "luan_niao": "奇禽",
    "wenyao": "鳞介",
    "fei_snake": "蛇蟒",
    "jueru": "异兽",
    "jingwei": "奇禽",
    "renyu_beifang": "鳞介",
    "baoxiao": "凶兽",
    "heluo_yu": "鳞介",
    "ershu": "异兽",
    "mengji": "异兽",
    "zhuhuai": "凶兽",
    "zuzi": "异兽",
    "liuju": "异兽",
    "dangkang": "异兽",
    "ziyu_fish": "鳞介",
    "jiaojiao_fish": "鳞介",
    "qinglong_ma": "神祇",
    "chenghuang_beast": "祥瑞",
    "fuzhu": "异兽",
    "huashe": "蛇蟒",
    "dijiang": "神祇",
    "xingtian": "神祇",
    "xiangliu": "凶兽",
    "basha": "鳞介",
    "lulu_kunlun": "神祇",
    "kaiming_shou": "神祇",
    "jiuying": "凶兽",
    "kuafu": "神祇",
    "yinglong": "神祇",
    "kui_beast": "神祇",
    "tiangou": "异兽",
    "zheng_beast": "异兽",
    "qiongqi": "凶兽",
    "manman": "奇禽",
}

# Additional animals (id must be globally unique). chapter_group must match emit defaults.
EXTRA_ANIMALS: list[dict[str, str]] = [
    # 南山经 / 南次 — 补常见异兽
    ("nanshan_jing", "异兽", "hu", "虎（招搖之山）", "", "五藏山經", "南山經", "南山經之首", "招搖之山", "经文举郡多猛如虎；与狌狌同域形成顶级捕食压力。", "区域威胁与猎魂素材。", "林缘与溪谷。", "捕食有蹄类、灵长幼体；与人类路线冲突。", "顶级消费者", "虎纹与桂影交错，眼在雾中两点金。", "狌狌", "《南山經》招搖之山条大意。"),
    ("nanshan_jing", "鳞介", "chiwen", "赤鱬（条目补注）", "", "五藏山經", "南山經", "南山經之首", "即翼之泽", "人面鱼身类赤鱬族群。", "疥疾抗性药饵母题。", "暖水泥滩与泽草。", "鹭、狐、大型鱼捕食；人类捕捞。", "中级消费者", "赤鳞群游如霞，人面纹作浅浮雕感。", "赤鱬", "同域复述，便于关卡族群化。"),
    ("nanshan_jing", "奇禽", "luan_niao_alt", "赤鴳（南山系涉禽占位）", "", "五藏山經", "南山經", "南次二經", "柜山一带泽地", "小型涉禽集群，声杂。", "可做环境音效与警戒鸟群。", "英水—赤水间湿地。", "食软体动物与昆虫；蛇与小型猛禽捕食。", "次级消费者", "赤羽点破灰绿芦苇。", "鴸", "设计占位条目，可替换为经有专名之鸟。"),
    ("nanshan_jing", "异兽", "zouwu", "驺吾", "", "五藏山經", "海内北經", "海内北經", "林氏国珍兽（跨篇收录）", "五彩虎形，尾长于身，行千里。", "仁兽母题：不忍伤生，可做护送/不杀判定。", "平原疏林与驿道。", "大型肉食但叙事克制；与犀象群落区隔。", "顶级消费者（仁兽叙事）", "长尾拖彩如旗，足踏云纹。", "孟极", "《海内北經》林氏国条大意，游戏资料跨篇归并。"),
    # 西山经补
    ("xishan_jing", "异兽", "luolu", "罗罗鸟", "", "五藏山經", "西山經", "西次三經", "昆仑丘附近", "青色大鸟，食虎豹（夸张笔法）。", "空中压制与威慑。", "高寒风蚀崖线。", "顶级掠食猛禽生态位。", "顶级消费者", "青翼蔽日，爪下虎豹剪影。", "穷奇", "《西山經》西次三系大意。"),
    ("xishan_jing", "鳞介", "hairen", "赤鱬（西山泽系）", "", "五藏山經", "西山經", "西次一經", "钱来以西诸泽", "与南山赤鱬同名异物风险：此处作泽鱼族群。", "皮肤类祝福素材。", "冷凉高山泽。", "鸭雁、獭、人。", "中级消费者", "体型略小、鳞色偏青。", "赤鱬", "同名异地产区，游戏分表。"),
    ("xishan_jing", "奇禽", "shu_shu", "数斯", "", "五藏山經", "西山經", "西次三經", "皋涂之山", "状如鸮而人足，食之已瘿。", "颈部肿块治疗向词条。", "高山杜鹃灌丛与裸岩。", "啮齿、蜥蜴；雕类天敌。", "次级消费者", "鸮面人足立岩，瘿瘤以光斑隐喻。", "玃如", "《西山經》皋涂之山条大意。"),
    ("xishan_jing", "异兽", "mi_mi", "麋（皋涂之山）", "", "五藏山經", "西山經", "西次四經", "皋涂之山", "多麋，湿草食兽群。", "与玃如同域食源竞争者。", "寒湿草甸与溪边。", "狼、豹、人猎。", "初级消费者", "群麋踏雾，角如枯枝林立。", "玃如", "《西山經》皋涂之山条。"),
    ("xishan_jing", "鳞介", "tengshe", "腾蛇", "", "五藏山經", "中山經", "中次二經", "柴桑之山（跨系占位）", "神话飞蛇，兴云雾。", "机动位移/穿雾机制。", "中山多雨裂谷（借用）。", "食鸟、鼠；与化蛇争域。", "三级消费者", "无翼而飞，身绕薄云带。", "化蛇", "神话层条目，地理取大意。"),
    # 北山经补
    ("beishan_jing", "鳞介", "lingyu", "陵鱼", "", "五藏山經", "海内北經", "海内北經", "海中", "人面手足鱼身，居海中。", "与人鱼系谱相邻。", "近岸岩礁与洞窟。", "杂食软体动物；人类渔捞。", "次级消费者", "潮汐池中手足抓岩。", "人鱼", "《海内北經》条大意。"),
    ("beishan_jing", "异兽", "youhuo", "幽鴳", "", "五藏山經", "北山經", "北次二經", "边春之山", "状如禺而文身，善笑，见人则卧。", "伪装与欺诈 AI 原型。", "多蒲薮、落棠。", "果实与昆虫；豹、狼。", "次级消费者", "笑纹如绘，卧姿如石。", "足訾", "《北山經》边春之山条大意。"),
    ("beishan_jing", "鳞介", "shan_hui", "鳣鱼", "", "五藏山經", "北山經", "北山經", "诸怀之水", "大型鲤科意象。", "厚肉资源点。", "深潭缓流。", "食软体动物；人捕。", "中级消费者", "巨影破浪，金鳞一线。", "诸怀之水", "《北山經》水系大意。"),
    # 东山经补
    ("dongshan_jing", "鳞介", "jingjing", "精精", "", "五藏山經", "东山經", "东次三經", "踇隅之山", "状如牛马尾，赤尾。", "见则其国多疫火（旱火双象，取大意）。", "海滨多赤垩。", "草食；与旱灾叙事绑定。", "初级消费者", "赤尾如焰帚扫沙。", "东山经", "各本异文多，取袁珂系大意。"),
    ("dongshan_jing", "奇禽", "fu_sang_niao", "扶桑十日鸟（神话化占位）", "", "五藏山經", "东山經", "东次三經", "扶桑", "乌栖十日神话与《山海》叙海交互。", "时间轴/灼烧 hazard。", "东海日出雾带。", "神话位。", "神祇", "乌影叠日，枝如青铜。", "太阳神话", "非严格单兽，作关卡母题占位。"),
    ("dongshan_jing", "鳞介", "haoma", "豪鱼", "", "五藏山經", "中山經", "中次七經", "渠猪之山（跨系）", "赤尾赤喙，食之可已疣。", "治疗类掉落。", "石灰岩溪涧。", "杂食藻类；人捕。", "中级消费者", "赤尾如梳，游于白石隙。", "中山經", "跨系收录。"),
    # 中山经补
    ("zhongshan_jing", "异兽", "suolu", "犀渠", "", "五藏山經", "中山經", "中次十經", "厘山", "状如牛，苍身，其音如婴儿，食人。", "食人兽链。", "中山森林河谷。", "顶级掠食。", "顶级消费者", "苍牛婴啼，角宽如铲。", "厘山", "《中山經》厘山条大意。"),
    ("zhongshan_jing", "奇禽", "shanxiao", "山𤟤", "", "五藏山經", "中山經", "中次二經", "昆吾之山", "状如犬而人面，见则天下大风。", "大风 hazard。", "多赤铜，裸风坡。", "杂食；与风母题耦合。", "次级消费者", "犬面人笑，风纹绕爪。", "昆吾之山", "字形各本不同，取大意。"),
    ("zhongshan_jing", "鳞介", "hu_bao", "化蛇（水脉版）", "", "五藏山經", "中山經", "中次二經", "阳水", "与 huashe 条目互补：强调水脉。", "洪水。", "裂谷溪。", "肉食。", "三级消费者", "人面豺身顺水游弋。", "化蛇", "同兽分述。"),
    # 海经 / 大荒补
    ("haijing", "神祇", "yub", "禺强", "", "海經", "海外北經", "海外北經", "北海", "人面鸟身，珥两青蛇，践两赤蛇；海神风神。", "海域关卡主宰。", "北海冰洋与浮冰。", "神话位。", "神祇", "巨翼下青红双蛇如缰。", "玄武系", "《海外北經》大意。"),
    ("haijing", "凶兽", "jiu_feng", "九凤", "", "海經", "大荒北經", "大荒北經", "北极天柜", "九首人面鸟身。", "多首技能轮替。", "极寒风穴。", "神话掠食。", "神怪", "九颈扇开如屏。", "九婴", "《大荒北經》系大意。"),
    ("dahuang_jing", "神祇", "xihe", "羲和", "", "大荒經", "大荒南經", "大荒南經", "东南海之外", "生十日，浴日于甘渊。", "时间/日照机制叙事核。", "甘渊湿地。", "神话。", "神祇", "浴日金光喷涌。", "太阳神话", "人物神，资料层供剧情。"),
    ("dahuang_jing", "神祇", "changxi", "常羲", "", "大荒經", "大荒西經", "大荒西經", "月亮神话", "生十二月，浴月。", "月相关卡轴。", "西极寒池。", "神话。", "神祇", "月轮如十二缺片。", "月亮神话", "人物神。"),
]

# 草木：chapter_group 使用 plants_* 以便分文件；emit 会把 plants_nanshan_jing 等写入独立 json
EXTRA_PLANTS: list[dict[str, str]] = [
    ("plants_nanshan_jing", "草木", "zhuyu", "祝余", "", "五藏山經", "南山經", "南山經之首", "招搖之山", "状如韭而青华。", "食之不饥（耐力资源）。", "西海之滨山麓草本带。", "被食草兽与人类采集；与迷榖伴生。", "初级生产者", "青华如星点，叶如韭列。", "迷榖", "《南山經》招搖之山条。"),
    ("plants_nanshan_jing", "草木", "migu", "迷榖", "", "五藏山經", "南山經", "南山經之首", "招搖之山", "状如榖而黑理，其华四照。", "佩之不迷（导航 buff）。", "林缘与石缝。", "菌根与昆虫访花；被狌狌栖息地共享。", "初级生产者", "黑理树干，四照华光。", "祝余", "《南山經》招搖之山条。"),
    ("plants_nanshan_jing", "木本", "xian_tree", "棪木", "", "五藏山經", "南山經", "南山經之首", "堂庭之山", "赤实如柰。", "果实资源与猿群食源。", "亚热带山地林。", "白猿取食；种子被鸟扩散。", "初级生产者", "赤实垂枝如小灯笼。", "白猿", "《南山經》堂庭之山条。"),
    ("plants_nanshan_jing", "草木", "baihao", "白䓘", "", "五藏山經", "南山經", "南次三經", "仑者之山", "状如榖而赤理，其汗如漆，其味如饴，食者不饥，可释劳。", "双效药剂母题。", "多青雘的山阴。", "树脂昆虫共生；人割采。", "初级生产者", "赤理流漆如蜜线。", "仑者之山", "《南山經》仑者之山条。"),
    ("plants_xishan_jing", "草木", "wenshan", "文茎", "", "五藏山經", "西山經", "西山經之首", "符禺之山", "其实如枣。", "食之已聋（与旋龟佩不聋可联动）。", "铜铁矿染山坡灌丛。", "葱聋取食；鸟播。", "初级生产者", "赤实小枣簇。", "葱聋", "《西山經》符禺之山条大意。"),
    ("plants_xishan_jing", "草木", "hao", "薰草", "", "五藏山經", "西山經", "西次四經", "浮山", "麻叶而方茎，赤华而黑实，臭如蘼芜，佩之已疠。", "防疫类饰品。", "多垩土山坡。", "昆虫访花；人采佩。", "初级生产者", "方茎赤华，黑实如珠。", "浮山", "《西山經》浮山条大意。"),
    ("plants_xishan_jing", "草木", "duheng", "杜衡", "", "五藏山經", "西山經", "西次四經", "天帝之山", "状如葵，其臭如蘼芜，食之已瘿。", "颈部肿块治疗。", "中山湿性林下。", "鹿类啃食；人采药。", "初级生产者", "葵叶心形，气如蘼芜。", "天帝之山", "《西山經》天帝之山条大意。"),
    ("plants_beishan_jing", "木本", "zhe_tree", "柘木", "", "五藏山經", "北山經", "北次三經", "发鸠之山", "多柘。", "精卫衔枝的落地树种。", "海岸沙丘与砾质土。", "鸟食果；人取材。", "初级生产者", "柘刺如铁丝，叶浓绿。", "精卫", "《北山經》发鸠之山条。"),
    ("plants_beishan_jing", "草木", "gu", "箨（竹类意象）", "", "五藏山經", "北山經", "北山經", "北岳之山", "多枳棘刚木。", "荆棘地形伤害与阻挡。", "寒温山地。", "山羊啃枝；鹿避。", "初级生产者", "枳棘黄果刺如针。", "诸怀", "《北山經》北岳之山条。"),
    ("plants_dongshan_jing", "木本", "sang", "桑（东山系）", "", "五藏山經", "东山經", "东次一經", "尸胡之山", "多苍玉，多鲛；多桑（大意）。", "养蚕与弓材叙事。", "河谷台地。", "蚕、人；叶被鹿食。", "初级生产者", "桑冠如云。", "东山經", "各山桑系归纳。"),
    ("plants_zhongshan_jing", "草木", "qin", "蓁（莽草意象）", "", "五藏山經", "中山經", "中次二經", "昆吾之山", "多赤铜，山有蓁莽。", "毒草 hazard 与矿冶。", "裸岩热风。", "少大型食草；昆虫多。", "初级生产者", "赤茎蔓地。", "山𤟤", "归纳性条目。"),
    ("plants_zhongshan_jing", "木本", "li_tree", "栎", "", "五藏山經", "中山經", "中山诸列", "伊洛之间", "常见橡栎林，供橡实与炭材。", "资源点与兽道。", "落叶阔叶林。", "野猪、熊取食橡实。", "初级生产者", "壳斗垂枝。", "中山經", "归纳。"),
    ("plants_wucang_misc", "草木", "rongyu", "荣草", "", "五藏山經", "中山經", "中次七經", "鼓镫之山", "食之已风（大意）。", "风邪抗性。", "中山溪谷。", "被鹿啃食。", "初级生产者", "细叶软茎。", "鼓镫之山", "大意。"),
    ("plants_wucang_misc", "草木", "xiao", "萧（香蒿类）", "", "五藏山經", "中山經", "中山诸列", "祭祀沿线", "糈与萧茅类祭品植物。", "仪式资源。", "台地农田边缘。", "人采；昆虫寄主。", "初级生产者", "灰绿羽状叶。", "中山祠", "归纳。"),
]

# 大规模程序化补种：按「山经篇名 + 序号」生成占位异兽，便于后续人工替换为经有专名之兽
def synth_beasts() -> list[tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]]:
    rows: list[tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]] = []
    specs = [
        ("nanshan_jing", "南山經", "南次二經", "南次二經列山", "柜山—漆吴山链", "异兽"),
        ("nanshan_jing", "南山經", "南次三經", "南次三經列山", "天虞—南禺山链", "奇禽"),
        ("xishan_jing", "西山經", "西次二經", "西次二經列山", "钤山—莱山链", "异兽"),
        ("xishan_jing", "西山經", "西次三經", "西次三經列山", "崇吾—翼望山链", "鳞介"),
        ("beishan_jing", "北山經", "北次二經", "北次二經列山", "空桑—泰山链", "异兽"),
        ("beishan_jing", "北山經", "北次三經", "北次三經列山", "太行—无逢山链", "鳞介"),
        ("dongshan_jing", "东山經", "东次二經", "东次二經列山", "空桑—北号山链", "奇禽"),
        ("dongshan_jing", "东山經", "东次三經", "东次三經列山", "尸胡—北始山链", "鳞介"),
        ("zhongshan_jing", "中山經", "中次五經", "中次五經列山", "薄山—苟床山链", "异兽"),
        ("zhongshan_jing", "中山經", "中次十經", "中次十經列山", "首阳—丙山链", "蛇蟒"),
    ]
    for chapter_group, jing, section, place_hint, chain, default_kind in specs:
        for n in range(1, 9):  # 8 条占位 / 篇
            kid = f"synth_{chapter_group}_{n:02d}"
            name = f"「{chain}」未具名异兽占位{n:02d}"
            rows.append(
                (
                    chapter_group,
                    default_kind,
                    kid,
                    name,
                    "",
                    "五藏山經",
                    jing,
                    section,
                    f"{place_hint}·经载多怪兽/怪鸟/怪鱼（择一占位）",
                    "形体未单列专名；此行为关卡密度占位，宜后续替换为注本可核之专名。",
                    "可映射为普通精英或环境 hazard 模板。",
                    f"{chain}典型生境：溪谷、裸岩、疏林组合（推演）。",
                    "与区域顶级捕食者/人类聚落形成能流交换；细节待替换专名后重写。",
                    "中级消费者",
                    "剪影块面+一两处夸张器官（角/尾/翼）待原画定稿。",
                    "占位条目",
                    "非经文专条，纯设计占位；补全时删除或替换。",
                )
            )
    return rows


def synth_plants() -> list[tuple[str, str, str, str, str, str, str, str, str, str, str, str, str, str, str, str]]:
    rows = []
    plant_groups = [
        ("plants_nanshan_jing", "南山經", "南山經", "南山诸列", "亚热带林草带"),
        ("plants_xishan_jing", "西山經", "西山經", "西山诸列", "温凉山地林草带"),
        ("plants_beishan_jing", "北山經", "北山經", "北山诸列", "寒温河谷林草带"),
        ("plants_dongshan_jing", "东山經", "东山經", "东山诸列", "滨海盐碱与沙生植被带"),
        ("plants_zhongshan_jing", "中山經", "中山經", "中山诸列", "伊洛河谷农耕—落叶林带"),
    ]
    herbs = ["蒿", "蓼", "薇", "蕨", "苓", "芎", "术", "芍药", "芎䓖", "黄连木", "楮", "榆", "槐", "梓", "楠", "荆", "杞"]
    for chapter_group, jing, section, col, biome in plant_groups:
        for i, h in enumerate(herbs, start=1):
            kid = f"plant_{chapter_group}_{i:02d}_{h}"
            rows.append(
                (
                    chapter_group,
                    "草木",
                    kid,
                    f"{h}（{col}归纳）",
                    "",
                    "五藏山經",
                    jing,
                    section,
                    f"{col}常见草本/木本之一（归纳占位）。",
                    "资源采集/药剂基底；具体经效待按选定注本逐条核对后改写。",
                    biome,
                    "与昆虫、植食兽、人类采集形成能流；菌根分解者参与。",
                    "初级生产者",
                    f"{h}形态可做模块化植被资产；色块随{biome}调整。",
                    "草木归纳",
                    "归纳占位，非单山专条逐字稿。",
                )
            )
    return rows


def row_tuple_to_dict(t: tuple[str, ...]) -> dict[str, str]:
    keys = FIELDNAMES
    return dict(zip(keys, t))


def main() -> None:
    existing: list[dict[str, str]] = []
    with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise SystemExit("no header")
        for row in reader:
            existing.append(row)

    # Normalize: ensure kind_zh and full column set
    seen_ids: set[str] = set()
    fixed: list[dict[str, str]] = []
    for row in existing:
        rid = (row.get("id") or "").strip()
        if not rid or rid in seen_ids:
            continue
        seen_ids.add(rid)
        d = {k: (row.get(k) or "").strip() for k in FIELDNAMES}
        if not d.get("kind_zh"):
            d["kind_zh"] = KIND_BY_ID.get(rid, "异兽")
        fixed.append(d)

    extras: list[dict[str, str]] = []
    for t in EXTRA_ANIMALS:
        extras.append(row_tuple_to_dict(t))
    for t in EXTRA_PLANTS:
        extras.append(row_tuple_to_dict(t))
    for t in synth_beasts():
        extras.append(row_tuple_to_dict(t))
    for t in synth_plants():
        extras.append(row_tuple_to_dict(t))

    for d in extras:
        if d["id"] in seen_ids:
            continue
        seen_ids.add(d["id"])
        fixed.append(d)

    with CSV_PATH.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(fixed)

    print(f"wrote {CSV_PATH} rows={len(fixed)}")


if __name__ == "__main__":
    main()
