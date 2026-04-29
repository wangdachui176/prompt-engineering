import sys, json, os, time
import requests, base64
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent

# 读取Packy API配置
try:
    from dotenv import load_dotenv
    load_dotenv(ROOT / ".env")
except ImportError:
    # 如果没有安装python-dotenv，直接从环境变量读取
    pass

PACKY_BASE_URL = os.environ.get('PACKY_BASE_URL', 'https://www.packyapi.com')
PACKY_API_KEY = os.environ.get('PACKY_KEY_TAI_IPX7S')  # 使用高质量渠道

if not PACKY_API_KEY:
    print("Error: PACKY_API_KEY not found in environment variables")
    sys.exit(1)

output_dir = ROOT / "output"
os.makedirs(output_dir, exist_ok=True)

# 读取提示词
prompt_file = ROOT / "prompt.txt"
if prompt_file.exists():
    prompt = open(prompt_file, 'r', encoding='utf-8').read().strip()
else:
    # 如果prompt.txt不存在，使用默认提示词
    prompt = "专业插画质感的跑步主题图像，未来感跑道，动感光效，运动能量感，8K超清"

print(f"Generating image for prompt: {prompt[:50]}...")

# 调用Packy API
payload = {
    "contents": [{"role": "user", "parts": [{"text": prompt}]}],
    "generationConfig": {
        "responseModalities": ["IMAGE"],
        "imageConfig": {
            "aspectRatio": "16:9",
            "imageSize": "1K"
        }
    }
}

try:
    resp = requests.post(
        f'{PACKY_BASE_URL}/v1beta/models/gemini-2.5-flash-image:generateContent',
        headers={'Authorization': f'Bearer {PACKY_API_KEY}', 'Content-Type': 'application/json'},
        json=payload,
        verify=False,  # 根据.env配置，忽略SSL验证
        timeout=180
    )

    if resp.status_code != 200:
        print(f"Error: {resp.status_code} - {resp.text}")
        sys.exit(1)

    data = resp.json()
    candidates = data.get('candidates', [])

    if not candidates:
        print(f"No candidates: {data}")
        sys.exit(1)

    first_cand = candidates[0]
    content = first_cand.get('content', {})
    parts = content.get('parts', [])

    image_saved = False
    for part in parts:
        inline = part.get('inlineData', {})
        img_data = inline.get('data', '')
        if img_data:
            img_bytes = base64.b64decode(img_data)
            
            # 生成文件名
            ts = time.strftime('%Y%m%d_%H%M%S')
            filepath = output_dir / f"img_{ts}.png"
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
            print(f"Saved: {filepath}")
            image_saved = True
            break
    
    if not image_saved:
        print(f"No image in response")
        sys.exit(1)

    # 保存结果信息
    result_info = {
        "prompt": prompt,
        "api_used": "packy",
        "model": "gemini-2.5-flash-image",
        "timestamp": ts,
        "output_file": str(filepath.name) if 'filepath' in locals() else None
    }
    
    with open(ROOT / "output" / "result.json", 'w', encoding='utf-8') as f:
        json.dump(result_info, f, ensure_ascii=False, indent=2)
    print('Done. Saved to result.json')

except Exception as e:
    print(f"Error occurred: {str(e)}")
    sys.exit(1)

    data = resp.json()
    candidates = data.get('candidates', [])

    if not candidates:
        print(f"No candidates: {data}")
        sys.exit(1)

    first_cand = candidates[0]
    content = first_cand.get('content', {})
    parts = content.get('parts', [])

    image_saved = False
    for part in parts:
        inline = part.get('inlineData', {})
        img_data = inline.get('data', '')
        if img_data:
            img_bytes = base64.b64decode(img_data)
            
            # 生成文件名
            ts = time.strftime('%Y%m%d_%H%M%S')
            filepath = output_dir / f"img_{ts}.png"
            with open(filepath, 'wb') as f:
                f.write(img_bytes)
            print(f"Saved: {filepath}")
            image_saved = True
            break
    
    if not image_saved:
        print(f"No image in response")
        sys.exit(1)

    # 保存结果信息
    result_info = {
        "prompt": prompt,
        "api_used": "packy",
        "model": "gemini-2.5-flash-image",
        "timestamp": ts,
        "output_file": str(filepath.name) if 'filepath' in locals() else None
    }
    
    with open(ROOT / "output" / "result.json", 'w', encoding='utf-8') as f:
        json.dump(result_info, f, ensure_ascii=False, indent=2)
    print('Done. Saved to result.json')

except Exception as e:
    print(f"Error occurred: {str(e)}")
    sys.exit(1)
