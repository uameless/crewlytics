import pandas as pd

def data_cleaning_agent(df: pd.DataFrame) -> pd.DataFrame:

    print(f"➡️ Starting data cleaning. Original shape: {df.shape}")

    # Remove duplicate rows
    df = df.drop_duplicates()
    
    # Drop columns with >50% missing values (you can adjust this threshold)
    threshold = len(df) * 0.5
    df = df.dropna(axis=1, thresh=threshold)

    # Fill missing numeric columns with median
    numeric_cols = df.select_dtypes(include=['number']).columns
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())

    # Fill missing categorical columns with mode
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in categorical_cols:
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    # (Optional) Normalize column names to lowercase & replace spaces
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    print(f"✅ Data cleaned successfully. New shape: {df.shape}")
    return df

if __name__ == "__main__":
    from agents.data_ingestion_agent import data_ingestion_agent
    
    test_file = "data/products.csv"
    try:
        raw_df = data_ingestion_agent(test_file)
        cleaned_df = data_cleaning_agent(raw_df)
        print(cleaned_df.head()) 
    except Exception as e:
        print(e)
