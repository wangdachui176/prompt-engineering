import sys, json, os, time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT / ".claude" / "skills" / "lovart-api"))
os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
os.environ['LOVART_INSECURE_SSL'] = '1'

from agent_skill import AgentSkill, LocalState

state = LocalState()
data = state.load()
project_id = data.get('active_project')

s = AgentSkill(
    base_url=os.environ.get('LOVART_BASE_URL', 'https://lgw.lovart.ai'),
    access_key=os.environ.get('LOVART_ACCESS_KEY'),
    secret_key=os.environ.get('LOVART_SECRET_KEY'),
    timeout=120
)

output_dir = ROOT / "output"
os.makedirs(output_dir, exist_ok=True)

prompt = open(ROOT / "prompt.txt", 'r', encoding='utf-8').read().strip()
prefer = {"IMAGE": ["generate_image_jimeng"]}

result = s.chat(
    prompt=prompt,
    project_id=project_id,
    prefer_models=prefer
)

ts = time.strftime('%Y%m%d_%H%M%S')
dl = s.download_artifacts(result, output_dir=output_dir, prefix=f"img_{ts}")
result['downloaded'] = dl

with open(ROOT / "output" / "result.json", 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print('Done. Saved to result.json')
