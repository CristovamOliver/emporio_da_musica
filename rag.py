from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from pdf_loader import load_pdf_file


def create_retriever():

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vector_store = Chroma(
        collection_name="politicas_loja",
        embedding_function=embeddings,
        persist_directory="./chroma_db",
    )

    if vector_store._collection.count() == 0:

        documents = load_pdf_file()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )

        chunks = text_splitter.split_documents(documents)

        vector_store.add_documents(chunks)

    return vector_store.as_retriever(search_kwargs={"k": 3})
