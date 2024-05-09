import os

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import time
from pymongo import MongoClient
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_postgres import PGVector
from langchain_postgres.vectorstores import PGVector

class VectorDB:
    def __init__(self, db_path="./db", db_type="chroma", embedding_function=None):
        self.db_path = db_path
        self.db_type = db_type
        self.vectordb = None
        if embedding_function is None:
            self.embedding_function = OpenAIEmbeddings()
        else:
            self.embedding_function = embedding_function

    def get_similar_documents(self, query, k=5):
        if self.vectordb is None:
            print(
                "DB is not loaded or created. Please load or create the database first."
            )
            return []
        similar_docs = self.vectordb.similarity_search(query, k)
        return similar_docs

    def create_db(self, tokenized_chunks):
        raise NotImplementedError("create_db method must be implemented in subclasses.")

    def load_db(self):
        raise NotImplementedError("load_db method must be implemented in subclasses.")


class ChromaVectorDB(VectorDB):
    def create_db(self, tokenized_chunks, batch_size=100):
        """Create the vector database by processing tokenized chunks in batches."""
        self.batch_size = batch_size
        if tokenized_chunks is None:
            print("No documents found to create DB.")
            return self

        print("Creating Chroma DB")
        if os.path.exists(self.db_path):
            print(f"DB already exists at {self.db_path}. Loading existing DB.")
            self.vectordb = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embedding_function,
            )
        else:
            # Initialize an empty database
            self.vectordb = Chroma(
                persist_directory=self.db_path,
                embedding_function=self.embedding_function,
            )
            # Process batches
            print(f"Processing {len(tokenized_chunks)} documents in batches of {self.batch_size}")
            for i in range(0, len(tokenized_chunks), self.batch_size):
                batch = tokenized_chunks[i:i + self.batch_size]
                # print(f"Adding batch {i // self.batch_size + 1}: {len(batch)} documents")
                self.vectordb.add_documents(
                    documents=batch,
                    embedding=self.embedding_function
                )
                time.sleep(0.5)
        return self

    def load_db(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(
                f"DB does not exist at {self.db_path}. Please create DB first."
            )

        print("Loading Chroma DB...")
        self.vectordb = Chroma(
            persist_directory=self.db_path, embedding_function=self.embedding_function
        )
        return self

class MongoDBVectorDB(VectorDB):
    def __init__(self, db_uri, db_name, collection_name, index_name, embedding_function=None):
        try:
            client = MongoClient(db_uri)
            print("Connected to MongoDB")
        except Exception as e:
            raise ValueError(f"Failed to connect to MongoDB: {str(e)}")

        self.db = client[db_name]
        self.collection_name = collection_name
        self.index_name = index_name
        self.embedding_function = OpenAIEmbeddings() if embedding_function is None else embedding_function
        self.collection = self.db[self.collection_name]
        self.mongoDB_vectorstore = MongoDBAtlasVectorSearch(self.collection, self.embedding_function)

    def collection_exists(self):
        return self.collection_name in self.db.list_collection_names()

    def user_confirmation(self):
        if self.collection_exists():
            user_input = input("Collection exists. Do you want to proceed with adding documents? (y/n): ")
            return user_input.strip().lower() == 'y'
        return True  # Proceed if the collection doesn't exist

    def create_db(self, tokenized_chunks):
        if tokenized_chunks is None:
            print("No documents found to create DB.")
            return self

        if not self.user_confirmation():
            print("Operation cancelled.")
            
            return self.load_db()

        print("Creating MongoDB Vector Store")
        self.vectordb = self.mongoDB_vectorstore.from_documents(
            documents=tokenized_chunks,
            embedding=self.embedding_function,
            collection=self.collection,
            index_name=self.index_name,
        )
        return self

    def load_db(self):
        print("Loading MongoDB Vector Store...")
        self.vectordb = MongoDBAtlasVectorSearch(
            embedding=self.embedding_function,
            collection=self.collection,
            index_name=self.index_name,
        )
        return self

class PGVectorDB(VectorDB):
    def __init__(self, db_uri, collection_name, embedding_function=None, use_jsonb=True):
        super().__init__(db_type="pgvector", embedding_function=embedding_function)
        self.connection = db_uri
        self.collection_name = collection_name
        self.use_jsonb = use_jsonb

    def create_db(self, tokenized_chunks, batch_size=100):
        if not tokenized_chunks:
            print("No documents found to create DB.")
            return self
        
        self.vectordb = PGVector(
            embeddings=self.embedding_function,
            collection_name=self.collection_name,
            connection=self.connection,
            use_jsonb=self.use_jsonb,
        )
        # time.sleep(5)

        print("Creating PGVector Store")

        print(f"Processing {len(tokenized_chunks)} documents in batches of {batch_size}")
        for i in range(0, len(tokenized_chunks), batch_size):
            batch = tokenized_chunks[i:i + batch_size]
            # print(f"Adding batch {i // batch_size + 1}: {len(batch)} documents")
        
            self.vectordb.add_documents(batch)
            time.sleep(0.5)

        return self

    def load_db(self):
        print("Loading PGVector DB...")
        self.vectordb = PGVector(
            embeddings=self.embedding_function,
            collection_name=self.collection_name,
            connection=self.db_uri,
            use_jsonb=self.use_jsonb,
        )
        return self
    
    def delete_db(self, pgvector_instance):
        print("Dropping PGVector DB tables...")
        pgvector_instance.drop_tables()
        print("Tables dropped.")