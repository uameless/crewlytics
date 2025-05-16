import pandas as pd
import os

def data_ingestion_agent(file_path: str) -> pd.DataFrame:

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_extension = os.path.splitext(file_path)[1].lower()

    try:
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
        elif file_extension in ['.xls', '.xlsx']:
            df = pd.read_excel(file_path)
        elif file_extension == '.json':
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")

        print(f"✅ Data loaded successfully. Shape: {df.shape}")
        return df

    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        raise e

if __name__ == "__main__":
    test_file = "data/products.csv"
    try:
        df = data_ingestion_agent(test_file)
        print(df.head())
    except Exception as e:
        print(e)
