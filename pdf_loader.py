from pathlib import Path
from pypdf import PdfReader



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
    reader = PdfReader(file_path)

    documents = [
        {
            "page_number": page_number,
            "text": page.extract_text() or ""
        }
        for page_number, page in enumerate(reader.pages, start=1)
    ]

    print(f"Total de páginas do pdf: {len(documents)}")

    return documents


if __name__ == "__main__":
    documents = load_pdf_file()