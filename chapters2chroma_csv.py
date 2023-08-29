from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.document_loaders import CSVLoader

openai_api_key = 'YOUR_OPENAI_API'

material_path = "YOUR_DATASET_FROM_COLD"
loader = CSVLoader(material_path)
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
docs = text_splitter.split_documents(documents)
db_path = 'YOUR_VECTORE_DATABASE'
embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

presist_directory = db_path
vectordb = Chroma.from_documents(docs, embeddings, persist_directory=presist_directory)
vectordb.persist()
