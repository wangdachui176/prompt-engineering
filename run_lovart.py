import subprocess, sys, os

skill = r"D:\cursor\商店应用物料\.claude\skills\lovart-api\agent_skill.py"

tasks = [
    {
        "label": "App图标-即梦",
        "prompt": "战场金与热血红配色的游戏图标，英雄剪影与王者荣耀徽章融合，金色光晕从中心向外辐射，深红色背景带金属质感，3D立体设计带强烈光影层次，史诗奇幻游戏图标风格，圆角方形构图，小尺寸下辨识度极高，高细节，8K超清",
        "model": "generate_image_jimeng",
    },
    {
        "label": "App图标-Banana",
        "prompt": "王者荣耀游戏图标，英雄徽章与金色王冠融合，居中圆形构图，深红色金属质感背景，战场金色光晕从核心向外辐射，3D概念艺术风格，史诗奇幻游戏图标美学，戏剧性内发光，强烈明暗对比，高细节，8K超清",
        "model": "generate_image_nano_banana_pro",
    },
    {
        "label": "启动页-即梦",
        "prompt": "五位英雄并肩站立于王者峡谷入口，仰视广角构图，英雄身形渺小衬托宏伟峡谷背景，天空占画面60%，战场金色神光从天际倾泻而下，大气透视雾霭弥漫远山，主体暖色边缘光，背景冷色虚化，强烈明暗对比，3D概念艺术风格，史诗奇幻游戏插画，热血竞技氛围，前景仅保留英雄主体，中景简洁峡谷路径，背景柔焦虚化，8K超清，极致细节，电影级构图",
        "model": "generate_image_jimeng",
    },
    {
        "label": "启动页-Banana",
        "prompt": "五位英雄并肩站立于峡谷入口，电影级广角仰视构图，渺小英雄身形衬托宏伟峡谷背景，天空占画面60%，3D概念艺术风格，史诗奇幻游戏插画，战场金色神光从天际倾泻，大气透视雾霭，主体暖色边缘光，背景冷色景深虚化，强烈明暗对比，热血竞技史诗氛围，8K超清，极致细节",
        "model": "generate_image_nano_banana_pro",
    },
    {
        "label": "宣传海报-即梦",
        "prompt": "王者荣耀史诗竞技宣传海报，英雄登顶王者峡谷制高点，金色王冠从天而降；电影级广角仰视构图，渺小英雄衬托宏伟战场，天空占画面60%，视觉张力拉满；战场金、热血红、深紫品牌配色，高对比强烈色彩碰撞，金色神光丁达尔效应；3D概念艺术风格，HDR质感，弥散晕染暗部层次，边缘虚化；主体暖色边缘光，背景冷色虚化，强烈明暗对比，主体置于三分法交叉点；史诗荣耀感，热血竞技氛围，宿命感与压迫感凸显；8K超清，极致细节，视觉冲击力爆棚，震撼炸裂",
        "model": "generate_image_jimeng",
    },
    {
        "label": "宣传海报-Banana",
        "prompt": "王者荣耀史诗竞技宣传海报，英雄登顶制高点金色王冠从天而降，电影级广角仰视构图，渺小英雄衬托宏伟战场背景，天空占画面60%；战场金热血红深紫品牌配色，高对比强烈色彩碰撞；3D概念艺术风格，HDR质感，弥散晕染暗部层次；戏剧性金色神光丁达尔效应，主体暖色边缘光，背景冷色景深虚化；史诗荣耀感，热血竞技氛围，8K超清，极致细节，视觉冲击力爆棚",
        "model": "generate_image_nano_banana_pro",
    },
    {
        "label": "功能介绍图-即梦",
        "prompt": "5V5对称竞技场俯视示意图，蓝红两队英雄分列两侧，王者峡谷地图清晰呈现，战场金色分界线居中，前景仅保留双方英雄图标，中景简洁地图路径，背景柔焦虚化，3D概念艺术风格，战场金与热血红配色，主体暖色边缘光，强烈明暗对比，史诗竞技感，公平对战视觉隐喻，高细节，8K超清",
        "model": "generate_image_jimeng",
    },
    {
        "label": "功能介绍图-Banana",
        "prompt": "5V5对称竞技场俯视示意图，蓝红两队英雄分列两侧，王者峡谷地图清晰呈现，战场金色分界线居中，俯视广角构图，前景英雄图标清晰对焦，背景地图柔焦虚化，3D概念艺术风格，战场金与热血红配色，戏剧性顶光，主体暖色边缘光，强烈明暗对比，史诗竞技感，公平对战视觉隐喻，高细节，8K超清",
        "model": "generate_image_nano_banana_pro",
    },
]

import json, time

thread_id = None

for task in tasks:
    print(f"\n{'='*50}")
    print(f"正在生成：{task['label']}")
    print(f"{'='*50}")

    prefer = json.dumps({"IMAGE": [task["model"]]})
    cmd = [sys.executable, skill, "chat",
           "--prompt", task["prompt"],
           "--prefer-models", prefer,
           "--json", "--download",
           "--output-dir", r"D:\cursor\商店应用物料\output\王者荣耀"]

    if thread_id:
        cmd += ["--thread-id", thread_id]

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    print(result.stdout[:500] if result.stdout else "")
    if result.stderr:
        print("STDERR:", result.stderr[:300])

    try:
        data = json.loads(result.stdout)
        if not thread_id and data.get("thread_id"):
            thread_id = data["thread_id"]
        for dl in data.get("downloaded", []):
            if dl.get("local_path"):
                print(f"  已下载：{dl['local_path']}")
    except Exception as e:
        print(f"解析失败：{e}")

print("\n全部完成！")
