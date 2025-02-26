import streamlit as st
from chains.system_extraction_chain import ExtractSystem
from services.data_loader import DataLoader
from services.document_splitter import DocumentSplitter
from services.vector_store import VectorStore
from services.prompt_service import PromptService
from services.llm_service import LLMService
from model.configuration import InstallationRecommendation
import json
from environments import *
from langchain_groq import ChatGroq
import torch

torch.classes.__path__ = [] # Fix for torch classes not found in streamlit sharing

st.title("ArchIntelligence Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "services" not in st.session_state:
    # Extracting system configuration is still buggy, for now manually edit the system_info.json file
    # extract_system = ExtractSystem()
    # output_path = extract_system.output_json()
    config_load = {
        'config': {
            'file': 'model/configDatabase.json',
            'schema': 'model/schema.jq'
        },
        'system': {
            'file': 'assets/system_info.json',
            'schema': 'model/SystemSchema.jq'
        }
    }

    prompt_service = PromptService()
    document_splitter = DocumentSplitter()
    vector_store_service = VectorStore("sentence-transformers/all-MiniLM-L6-v2")
    llm = ChatGroq(api_key=GROQ_API_KEY, model="deepseek-r1-distill-qwen-32b")

    data_loader = DataLoader(config_load)
    documents = data_loader.load()
    split_docs = document_splitter.split(documents)
    vector_store = vector_store_service.create(split_docs)
    retriever = vector_store.as_retriever()
    prompt_template = prompt_service.create_prompt_template()
    output_parser = prompt_service.create_parser()

    st.session_state.llm_service = LLMService(
        retriever, prompt_template, llm, output_parser
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What would you like to know about your system configuration?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.llm_service.add_message(prompt, is_user=True)

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response_dict = st.session_state.llm_service.create_chain().invoke(prompt)
            recommendation = InstallationRecommendation.model_validate(response_dict)
            json_string = json.dumps(recommendation.model_dump(), indent=2)

            st.session_state.messages.append({"role": "assistant", "content": json_string})
            st.session_state.llm_service.add_message(json_string, is_user=False)

            st.json(json_string)
        except Exception as e:
            error_message = f"Error processing request: {e}"
            st.error(error_message)
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.session_state.llm_service.add_message(error_message, is_user=False)
