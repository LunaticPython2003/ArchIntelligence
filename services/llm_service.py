from langchain_core.runnables import RunnablePassthrough
from langchain.memory import ConversationBufferMemory, StreamlitChatMessageHistory
from model.configuration import InstallationRecommendation

class LLMService:
    def __init__(self, retriever, prompt, llm, output_parser):
        self.runnable = RunnablePassthrough()
        self.retriever = retriever
        self.prompt = prompt
        self.llm = llm
        self.parser = output_parser
        # Initialize Streamlit chat message history
        self.msgs = StreamlitChatMessageHistory(key="chat_history")
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            chat_memory=self.msgs,
            memory_key="chat_history",
            return_messages=True
        )

    def create_chain(self):
        chain = (
            {
                "context": self.retriever,
                "input": self.runnable,
                "format_instructions": lambda _: InstallationRecommendation.model_json_schema(),
                "chat_history": lambda _: self.memory.load_memory_variables({})["chat_history"]
            }
            | self.prompt
            | self.llm
            | self.parser
        )
        return chain

    def add_message(self, message, is_user=True):
        """Add a message to the conversation history"""
        if is_user:
            self.msgs.add_user_message(message)
        else:
            self.msgs.add_ai_message(message)