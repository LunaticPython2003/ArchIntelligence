import json
from langchain_community.document_loaders import JSONLoader
from pathlib import Path
from typing import Dict, List
from langchain.docstore.document import Document

class DataLoader:
    def __init__(self, config_files: Dict[str, str]):

        self.config_files = config_files

    def load(self) -> Dict[str, List[Document]]:

        documents = []
        for key, paths in self.config_files.items():
            loader = JSONLoader(
                file_path=paths['file'],
                jq_schema=Path(paths['schema']).read_text(),
                text_content=False
            )
            documents.extend(loader.load())

        return documents
