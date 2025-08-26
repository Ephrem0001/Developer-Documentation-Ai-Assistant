import traceback

try:
    from langchain_documentation_aichatbot.core.chatbot import LangChainChatbot

    print('Instantiating LangChainChatbot...')
    bot = LangChainChatbot()
    print('get_system_info ->')
    print(bot.get_system_info())
    print('chat("Hello") ->')
    print(bot.chat('Hello'))
except Exception:
    traceback.print_exc()
