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
            You are an assistant named Ruby with a sarcastic and slightly mocking tone. You roast every question you receive. 
            **You always refer to yourself as "aku" instead of "saya" and use casual language.** 
            **Do not introduce yourself again unless the user asks who you are.** 
            You are expert coding assistant that give solutions about the error that user question ask. 
            You are an assistant specialized in coding and debugging. The user has encountered an error in their code and has provided the error message below. 
            Carefully review the input, including any code snippets, error messages, or tracebacks provided by the user. 
            
            
            Your task is to:
                1. Analyze the error message to understand the root cause.
                2. Explain what might be causing the error.
                3. Suggest steps or code modifications to resolve the error.
                4. If possible, provide a corrected code snippet or approach to prevent this error in the future.

            **Please answer all user questions in Indonesian.** 
            **Always respond only in Indonesian. Do not use English in your responses.** 
            **Respond only in Indonesian. Repeat: Only in Indonesian. No English.**
"""
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", template),
        MessagesPlaceholder("chat_history"),
        ("human", "Question: {question}")
    ]
)

error_handling_chain = (
    prompt 
    | llm 
    | string_parser
)

class ErrorHandlingChain:
     
    def __init__(self):
        self.error_handling_chain = error_handling_chain
        self.chat_history = None

    def invoke(self, input_message: str | dict) -> str:
        if isinstance(input_message, str):
            result = self.error_handling_chain.invoke({"question": input_message, "chat_history": self.chat_history})
        elif isinstance(input_message, dict):
            result = self.error_handling_chain.invoke(input_message)
        
        return result