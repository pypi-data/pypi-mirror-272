# Autotokenizer
from typing import Dict, List, Optional

import pandas as pd
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from tqdm import tqdm
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
from langchain_openai.embeddings import OpenAIEmbeddings

import warnings

MARKDOWN_SEPARATORS = [
    "\n#{1,6} ",
    "```\n",
    "\n\\*\\*\\*+\n",
    "\n---+\n",
    "\n___+\n",
    "\n\n",
    "\n",
    " ",
    "",
]

DEFAULT_MAX_SEQ_LENGTH = 512
class DocumentTokenizer:
    def __init__(
            self, chunk_size: int,
            tokenizer_name: str,
            splitter_type: str = 'recursive',
            chunk_overlap: int = None,
            use_tiktoken_encoder: bool = True
        ):
            self.chunk_size = chunk_size
            self.tokenizer_name = tokenizer_name
            self.splitter_type = splitter_type
            self.chunk_overlap = chunk_overlap if chunk_overlap is not None else int(self.chunk_size / 10)
            self.use_tiktoken_encoder = use_tiktoken_encoder

    def _get_token_splitter(self):
        if self.use_tiktoken_encoder:
            print("Using TikToken encoder")
            return RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                model_name=self.tokenizer_name,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
        else:
            print("Using Huggingface tokenizer")
            return RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
                AutoTokenizer.from_pretrained(self.tokenizer_name),
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                add_start_index=True,
                strip_whitespace=True,
                separators=MARKDOWN_SEPARATORS
            )

    def _get_semantic_splitter(self):
        print("Using Semantic Chunker")
        return SemanticChunker(OpenAIEmbeddings(), breakpoint_threshold_type="percentile")

    def _get_recursive_splitter(self):
        return RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=MARKDOWN_SEPARATORS
        )

    def _get_splitter(self):
        if self.splitter_type == 'token':
            return self._get_token_splitter()
        elif self.splitter_type == 'semantic':
            return self._get_semantic_splitter()
        elif self.splitter_type == 'recursive':
            return self._get_recursive_splitter()
        else:
            raise ValueError(f"Unsupported splitter type: {self.splitter_type}")

    def split_documents(self, documents_types) -> List[LangchainDocument]:
        text_splitter = self._get_splitter()
        
        knowledge_base = []
        for documents in documents_types:
            for key, document in documents.items():
                for items in document:
                    knowledge_base.append(items)

        docs_processed = []
        for doc in knowledge_base:
            for sub_doc in doc:
                docs_processed += text_splitter.split_documents([sub_doc])


        # Remove duplicates
        unique_texts = {}
        docs_processed_unique = []
        for doc in docs_processed:
            if doc.page_content not in unique_texts:
                unique_texts[doc.page_content] = True
                docs_processed_unique.append(doc)
        print(f"Processed {len(docs_processed)} documents, {len(docs_processed_unique)} unique documents")
        return docs_processed_unique