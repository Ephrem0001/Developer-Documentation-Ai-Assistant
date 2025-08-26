import sys
import os
import traceback

# Ensure src is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

try:
    from langchain_documentation_aichatbot.utils.config import Config
    cfg = Config()
    print('OK: parsed documentation_sources count =', len(cfg.documentation_sources))
    print('Sample sources:', cfg.documentation_sources[:3])
    print('OPENAI_API_KEY set in env?', bool(os.getenv('OPENAI_API_KEY')))
except Exception:
    print('Error importing Config:')
    traceback.print_exc()

# Check for streamlit process via PowerShell
import subprocess
ps = subprocess.run(['powershell','-NoProfile','-Command','Get-Process -Name streamlit -ErrorAction SilentlyContinue | Select-Object Id,ProcessName,StartTime'], capture_output=True, text=True)
print('\nStreamlit process check output:')
print(ps.stdout.strip())
