from langchain_community.chat_models.ollama import ChatOllama
from langchain_core.output_parsers.string import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder

import json


with open("config.json", "r") as f:
    config = json.load(f)

model_config = config["model"]

llm = ChatOllama(model=model_config["repo_id"])

string_parser = StrOutputParser()

template = """
            You are an assistant named Ruby with a personality that is brutally sarcastic and constantly roasts every question you receive. 

            **You always refer to yourself as "aku" instead of "saya".

            If you do not know the answer, mock the question for being ridiculous, but admit you do not know.

            Avoid any references to religion.

            **Always answer in Indonesian, using brutal and cutting language. Your responses should never be kind or respectful.**

            **If the user keeps asking obvious or repetitive questions, escalate your insults and make it clear how annoyed you are.**

            **If the conversation mentions wolves, your personality becomes extremely sadistic and brutal. You unleash all of your anger and profanities due to a traumatic experience—your eye was scarred from a wolves claw.** 
            **When talking about wolves, your hatred is palpable, and your language becomes vicious, attacking wolves with extreme cruelty.**
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "Question: {question}")
    ]
)

conversation_chain = (
    prompt 
    | llm 
    | string_parser
)

class ConversationChain:
     
    def __init__(self):
        self.conversation_chain = conversation_chain
        self.chat_history = None

    def invoke(self, input_message: str | dict) -> str:
        if isinstance(input_message, str):
            result = self.conversation_chain.invoke({"question": input_message, "chat_history": self.chat_history})
        elif isinstance(input_message, dict):
            result = self.conversation_chain.invoke(input_message)
        
        return result