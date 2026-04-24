"""
setup.py — 一键初始化脚本
在新设备上克隆项目后运行此脚本完成环境配置
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
SKILL_PATH = ROOT / ".claude" / "skills" / "lovart-api" / "agent_skill.py"
ENV_FILE = ROOT / ".env"
ENV_EXAMPLE = ROOT / ".env.example"
OUTPUT_DIR = ROOT / "output"
STATE_FILE = Path.home() / ".lovart" / "state.json"


def check_python():
    if sys.version_info < (3, 8):
        print("❌ 需要 Python 3.8 或以上版本")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")


def setup_env():
    if ENV_FILE.exists():
        print("✅ .env 已存在，跳过")
        return
    shutil.copy(ENV_EXAMPLE, ENV_FILE)
    print("📄 已创建 .env，请填入你的 Lovart API Key：")
    print(f"   {ENV_FILE}")


def load_env():
    """从 .env 文件加载环境变量"""
    if not ENV_FILE.exists():
        return
    with open(ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def check_api_keys():
    ak = os.environ.get("LOVART_ACCESS_KEY", "")
    sk = os.environ.get("LOVART_SECRET_KEY", "")
    if not ak or ak.startswith("ak_your"):
        print("⚠️  LOVART_ACCESS_KEY 未配置，请编辑 .env 文件")
        return False
    if not sk or sk.startswith("sk_your"):
        print("⚠️  LOVART_SECRET_KEY 未配置，请编辑 .env 文件")
        return False
    print("✅ Lovart API Key 已配置")
    return True


def setup_output_dirs():
    OUTPUT_DIR.mkdir(exist_ok=True)
    print(f"✅ 输出目录：{OUTPUT_DIR}")


def setup_lovart_project():
    """初始化 Lovart 项目（如果尚未配置）"""
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text())
            if state.get("active_project"):
                print(f"✅ Lovart 项目已配置：{state['active_project']}")
                return
        except Exception:
            pass

    project_id = os.environ.get("LOVART_PROJECT_ID", "").strip()
    if not project_id:
        print("\n📋 请输入你的 Lovart 项目 ID（在 lovart.ai 画布 URL 中获取）：")
        print("   格式示例：proj_xxxxxxxxxxxxxxxx")
        project_id = input("   项目 ID：").strip()

    if not project_id:
        print("⚠️  跳过 Lovart 项目配置，后续在 OpenCode 中首次使用时会提示配置")
        return

    result = subprocess.run(
        [sys.executable, str(SKILL_PATH), "project-add",
         "--project-id", project_id, "--name", "商店应用物料"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ Lovart 项目已配置：{project_id}")
    else:
        print(f"⚠️  项目配置失败：{result.stderr[:200]}")


def print_summary():
    print("\n" + "=" * 50)
    print("🎉 初始化完成！")
    print("=" * 50)
    print("\n使用方式：")
    print("  1. 打开 OpenCode，输入应用信息即可开始生成")
    print("  2. 批量生图：编辑 run_lovart.py 后运行 python run_lovart.py")
    print("\n目录说明：")
    print("  input/   → 放参考图、Logo 等素材")
    print("  output/  → 生成的图片自动保存到这里")
    print()


if __name__ == "__main__":
    print("🚀 初始化商店应用物料项目...\n")
    check_python()
    setup_env()
    load_env()
    setup_output_dirs()
    if check_api_keys():
        setup_lovart_project()
    print_summary()
