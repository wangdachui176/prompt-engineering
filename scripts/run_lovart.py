"""
run_lovart.py — 批量生图执行脚本

使用方式：
  1. 在 OpenCode 对话中生成 prompt 并通过质量自检
  2. 将 prompt 填入下方 TASKS 列表
  3. 运行：python run_lovart.py

支持的模型（MODEL 字段）：
  generate_image_jimeng          即梦 — 中文语义理解强，风格还原度高
  generate_image_nano_banana_pro Nano Banana Pro — 细节丰富，高质量插画
  generate_image_midjourney      Midjourney — 艺术感强，构图精致
  generate_image_seedream_3_0    Seedream — 写实风格，光影细腻
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# ─── 配置区 ───────────────────────────────────────────────────────────────────

# Lovart agent_skill.py 路径（相对于本文件）
SKILL_PATH = Path(__file__).parent.parent / ".claude" / "skills" / "lovart-api" / "agent_skill.py"

# 输出根目录
OUTPUT_ROOT = Path(__file__).parent.parent / "output"

# 应用名称（用于创建子目录）
APP_NAME = "应用名称"

# ─── 任务列表 ─────────────────────────────────────────────────────────────────
# 将 OpenCode 生成并通过自检的 prompt 填入此处
# label: 任务标识（用于日志和文件名）
# prompt: 中文 prompt（从 OpenCode 对话中复制）
# model: 生图模型（见上方说明）

TASKS = [
    # {
    #     "label": "App图标-即梦",
    #     "prompt": "在此粘贴即梦版本 prompt",
    #     "model": "generate_image_jimeng",
    # },
    # {
    #     "label": "App图标-Banana",
    #     "prompt": "在此粘贴 Banana 版本 prompt",
    #     "model": "generate_image_nano_banana_pro",
    # },
    # {
    #     "label": "启动页-即梦",
    #     "prompt": "在此粘贴即梦版本 prompt",
    #     "model": "generate_image_jimeng",
    # },
    # {
    #     "label": "启动页-Banana",
    #     "prompt": "在此粘贴 Banana 版本 prompt",
    #     "model": "generate_image_nano_banana_pro",
    # },
    # {
    #     "label": "宣传海报-即梦",
    #     "prompt": "在此粘贴即梦版本 prompt",
    #     "model": "generate_image_jimeng",
    # },
    # {
    #     "label": "宣传海报-Banana",
    #     "prompt": "在此粘贴 Banana 版本 prompt",
    #     "model": "generate_image_nano_banana_pro",
    # },
    # {
    #     "label": "功能介绍图-即梦",
    #     "prompt": "在此粘贴即梦版本 prompt",
    #     "model": "generate_image_jimeng",
    # },
    # {
    #     "label": "功能介绍图-Banana",
    #     "prompt": "在此粘贴 Banana 版本 prompt",
    #     "model": "generate_image_nano_banana_pro",
    # },
]

# ─── 执行逻辑（无需修改）──────────────────────────────────────────────────────

def load_env():
    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ.setdefault(key.strip(), val.strip())


def run_tasks():
    load_env()

    if not TASKS:
        print("⚠️  TASKS 列表为空，请先填入 prompt 再运行")
        return

    output_dir = OUTPUT_ROOT / APP_NAME
    output_dir.mkdir(parents=True, exist_ok=True)

    thread_id = None
    success, failed = 0, 0

    for i, task in enumerate(TASKS, 1):
        label = task.get("label", f"任务{i}")
        prompt = task.get("prompt", "").strip()
        model = task.get("model", "generate_image_jimeng")

        if not prompt:
            print(f"\n⚠️  [{label}] prompt 为空，跳过")
            continue

        print(f"\n{'='*55}")
        print(f"[{i}/{len(TASKS)}] 正在生成：{label}")
        print(f"{'='*55}")

        prefer = json.dumps({"IMAGE": [model]})
        cmd = [
            sys.executable, str(SKILL_PATH), "chat",
            "--prompt", prompt,
            "--prefer-models", prefer,
            "--json", "--download",
            "--output-dir", str(output_dir),
        ]
        if thread_id:
            cmd += ["--thread-id", thread_id]

        result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

        if result.stdout:
            print(result.stdout[:300])
        if result.stderr:
            print(f"STDERR: {result.stderr[:200]}")

        try:
            data = json.loads(result.stdout)
            if not thread_id and data.get("thread_id"):
                thread_id = data["thread_id"]
            downloaded = data.get("downloaded", [])
            if downloaded:
                for dl in downloaded:
                    if dl.get("local_path"):
                        print(f"  ✅ 已保存：{dl['local_path']}")
                success += 1
            else:
                print(f"  ⚠️  未获取到图片")
                failed += 1
        except Exception as e:
            print(f"  ❌ 解析失败：{e}")
            failed += 1

    print(f"\n{'='*55}")
    print(f"完成：{success} 成功 / {failed} 失败")
    print(f"输出目录：{output_dir}")
    print(f"{'='*55}")


if __name__ == "__main__":
    run_tasks()
