# part 1 example is not working
"""
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install beautifulsoup4
pip install sentence-transformers
"""

import os
os.environ["USER_AGENT"] = "MyLangChainApp/1.0"

# from langchain.document_loaders import WebBaseLoader  # deprecated
from langchain_community.document_loaders import WebBaseLoader
from langchain.indexes import VectorstoreIndexCreator
# from langchain.embeddings import OpenAIEmbeddings # deprecated
# from langchain_openai import OpenAIEmbeddings   # Insufficient quota

# Set up loader and embedding
loader = WebBaseLoader("https://www.promptingguide.ai/techniques/rag")
# embedding = OpenAIEmbeddings()    # insufficient quota
from langchain.embeddings import HuggingFaceEmbeddings
embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# index = VectorstoreIndexCreator().from_loaders([loader])
index = VectorstoreIndexCreator(embedding=embedding).from_loaders([loader])
index.query("What is RAG?")
