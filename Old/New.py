from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer

loader = TextLoader("C:/Users/chandrs4/PycharmProjects/WelcomeScreen/sample.txt")
docs = loader.load()

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="./chroma_db"
)

print("Vector DB created successfully")