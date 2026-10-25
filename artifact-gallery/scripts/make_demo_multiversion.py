import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from register_version import register

DEMO_ID = "演示_无人车价格策略简历适配_跨对话迭代"
SRC = r"D:\intern\.workbuddy\artifacts\_demo_src"
os.makedirs(SRC, exist_ok=True)

stages = {
    "v1_初稿_照抄JD.html": """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>v1 初稿·照抄JD</title>
<style>body{font-family:sans-serif;padding:24px;color:#333}h3{color:#c0392b}li{margin:6px 0}</style></head>
<body><h2>无人车·价格策略运营 简历适配（v1 初稿）</h2>
<h3>问题写法：直接复用 JD 原词</h3>
<ul>
<li><b>质量评估与履约激励机制：</b>负责价格策略的质量评估与履约激励机制，确保价格合理性和竞争力。</li>
<li><b>价格洞察与策略调整：</b>监控和分析市场价格，进行价格洞察，提供价格分析报告，调整定价策略。</li>
</ul>
<p style="color:#999">（这是第一版，HR 会觉得在硬凑 JD 原词，不真实。）</p></body></html>""",
    "v2_口语化改版.html": """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>v2 口语化改版</title>
<style>body{font-family:sans-serif;padding:24px;color:#333}h3{color:#e67e22}li{margin:6px 0}</style></head>
<body><h2>无人车·价格策略运营 简历适配（v2 口语化改版）</h2>
<h3>过度修正：太口语、不严谨</h3>
<ul>
<li><b>把合作方的履约表现管起来：</b>用看板盯各家表现，说白了就是按表现分好差、调资源，逼跑得慢的提准时率。</li>
<li><b>把用户的槽点理清楚：</b>顺藤摸瓜找出是哪条规则在惹事，把体验一点点往上拉。</li>
</ul>
<p style="color:#999">（这是第二版，不像写在简历上的书面语言。）</p></body></html>""",
    "v3_书面化定稿.html": """<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8"><title>v3 书面化定稿</title>
<style>body{font-family:sans-serif;padding:24px;color:#333}h3{color:#27ae60}li{margin:6px 0}</style></head>
<body><h2>无人车·价格策略运营 简历适配（v3 书面化定稿）</h2>
<h3>定稿：书面化、意思对齐 JD 但不抄原词</h3>
<ul>
<li><b>建立服务商履约表现评估机制：</b>以准实验框架量化各家时效偏差，结合流量分配对表现优异者倾斜资源、对偏差较大者推动整改，保障价格方案落地后的履约质量。</li>
<li><b>持续开展市场价格监测与策略调优：</b>搭建价格与补贴效果监测看板，定期输出分析结论并据此调整定价与补贴方案，形成数据驱动的闭环。</li>
</ul>
<p style="color:#999">（这是定稿，动词开头、量化、客观，符合简历文风。）</p></body></html>""",
}

order = ["v1_初稿_照抄JD.html", "v2_口语化改版.html", "v3_书面化定稿.html"]
for fn in order:
    fp = os.path.join(SRC, fn)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(stages[fn])
    desc = {"v1_初稿_照抄JD.html":"对话A初稿(照抄JD原词)",
            "v2_口语化改版.html":"对话B按反馈改口语化(过度修正)",
            "v3_书面化定稿.html":"对话C改书面化定稿"}[fn]
    art, vn = register(fp, desc, artifact_id=DEMO_ID, name="演示_无人车价格策略简历适配(跨对话迭代)")
    print(f"registered {DEMO_ID} v{vn}")
print("demo done")
