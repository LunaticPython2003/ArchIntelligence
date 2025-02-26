from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from model.configuration import InstallationRecommendation

class PromptService:
    def __init__(self):
        self.system_prompt = """You are an intelligent Arch Linux recommendation system that provides the best system configuration based on user needs.
        Use the following retrieved context to generate your recommendation.
        Your response MUST be a valid JSON object strictly following the given schema.
        Description is not needed when providing recommendations, just the values will work.

        Retrieved Context:
        {context}

        Human Question: {input}

        Important: Return a JSON object with ALL fields populated. This will be used for installation.
        """

    def create_prompt_template(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Previous conversation:\n{chat_history}\n\nNew question: {input}"),
            ("human", "Please provide recommendations following this schema: {format_instructions}")
        ])
        return prompt

    def create_parser(self):
        output_parser = JsonOutputParser(pydantic_object=InstallationRecommendation)
        return output_parser