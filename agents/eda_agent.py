import pandas as pd

def eda_agent(df: pd.DataFrame) -> dict:
    print("➡️ Starting exploratory data analysis (EDA).")

    # Dataset shape
    dataset_shape = df.shape

    # Data types
    data_types = df.dtypes.apply(lambda x: str(x)).to_dict()

    # Summary statistics
    summary_stats = df.describe(include='all').to_dict()

    # Correlation matrix (only numeric columns)
    correlation_matrix = df.select_dtypes(include=['number']).corr().to_dict()

    # descriptive KPIs for report table
    descriptive_stats = {}
    try:
        descriptive_stats["total_sales"] = round(df["sales"].sum(), 2)
    except KeyError:
        descriptive_stats["total_sales"] = "N/A"
    try:
        descriptive_stats["average_unit_price"] = round(df["unit_price"].mean(), 2)
    except KeyError:
        descriptive_stats["average_unit_price"] = "N/A"
    try:
        descriptive_stats["top_branch"] = df["branch"].mode()[0]
    except (KeyError, IndexError):
        descriptive_stats["top_branch"] = "N/A"
    try:
        descriptive_stats["average_rating"] = round(df["rating"].mean(), 2)
    except KeyError:
        descriptive_stats["average_rating"] = "N/A"

    eda_results = {
        "dataset_shape": dataset_shape,
        "data_types": data_types,
        "summary_statistics": summary_stats,
        "correlation_matrix": correlation_matrix,
        "descriptive_stats": descriptive_stats
    }

    print("✅ EDA completed successfully.")
    return eda_results

if __name__ == "__main__":
    from agents.data_ingestion_agent import data_ingestion_agent
    from agents.data_cleaning_agent import data_cleaning_agent

    test_file = "data/products.csv"
    try:
        raw_df = data_ingestion_agent(test_file)
        clean_df = data_cleaning_agent(raw_df)
        eda_results = eda_agent(clean_df)

        print(f"Dataset shape: {eda_results['dataset_shape']}")
        print(f"Data types: {eda_results['data_types']}")
        print(f"Descriptive KPIs: {eda_results['descriptive_stats']}")
        print(f"Correlation matrix sample: {list(eda_results['correlation_matrix'].items())[:3]}")

    except Exception as e:
        print(e)
