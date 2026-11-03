from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
import re


BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data"

def read_pdf_file(filename: str) -> Path:
    file_path = FILE_PATH / filename

    if not file_path.is_file():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {file_path}"
        )

    return file_path


def load_pdf_file():
    file_path = read_pdf_file("políticas_da_loja.pdf")
    loader = PyPDFLoader(file_path)
    document = loader.load()

    for doc in document:
        text = doc.page_content

        # Junta palavras separadas por quebras de linha
        text = re.sub(r'\n+', ' ', text)

        # Remove espaços duplicados
        text = re.sub(r'\s+', ' ', text)

        doc.page_content = text.strip()

    return document

if __name__ == "__main__":
    document = load_pdf_file()
    