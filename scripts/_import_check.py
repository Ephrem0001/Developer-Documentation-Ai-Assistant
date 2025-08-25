import sys
sys.path.insert(0, 'src')
modules = [
    'langchain_documentation_aichatbot.utils.helpers',
    'langchain_documentation_aichatbot.utils.config',
    'langchain_documentation_aichatbot.core.vector_store',
]
for m in modules:
    try:
        __import__(m)
        print(f'OK: imported {m}')
    except Exception as e:
        print(f'ERROR importing {m}: {e}')
