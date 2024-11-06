from enum import Enum
from langchain_core.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate
)
from datetime import datetime
from templates.chatbot import DATABASE_SYSTEM_TEMPLATE



def get_database_chat_template() -> ChatPromptTemplate:
    system_template = SystemMessagePromptTemplate.from_template(DATABASE_SYSTEM_TEMPLATE)
    response = ChatPromptTemplate.from_messages([system_template])
    return response
    
    