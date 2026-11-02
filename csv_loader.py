from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent
FILE_PATH = BASE_DIR / "data"


def read_csv_file(filename: str) -> list[dict]:
    file_path = FILE_PATH / filename

    if not file_path.is_file():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    df = pd.read_csv(file_path)

    return df.to_dict(orient="records")