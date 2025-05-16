import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def visualization_agent(df: pd.DataFrame, output_dir: str = "outputs/charts") -> list:
    print("➡️ Starting data visualization.")
    os.makedirs(output_dir, exist_ok=True)

    plot_paths = []

    # Plot 1: Correlation heatmap (numerical features)
    numeric_df = df.select_dtypes(include=['number'])
    if not numeric_df.empty:
        plt.figure(figsize=(10, 8))
        sns.heatmap(numeric_df.corr(), annot=True, fmt=".2f", cmap="coolwarm")
        heatmap_path = os.path.join(output_dir, "correlation_heatmap.png")
        plt.title("Correlation Heatmap")
        plt.savefig(heatmap_path)
        plt.close()
        plot_paths.append(heatmap_path)

    # Plot 2: Histogram of all numeric features
    for col in numeric_df.columns:
        plt.figure()
        sns.histplot(df[col], kde=True)
        plt.title(f"Distribution of {col}")
        hist_path = os.path.join(output_dir, f"{col}_histogram.png")
        plt.savefig(hist_path)
        plt.close()
        plot_paths.append(hist_path)

    print(f"✅ Generated {len(plot_paths)} plots.")
    return plot_paths

if __name__ == "__main__":
    from agents.data_ingestion_agent import data_ingestion_agent
    from agents.data_cleaning_agent import data_cleaning_agent

    test_file = "data/products.csv"
    try:
        raw_df = data_ingestion_agent(test_file)
        clean_df = data_cleaning_agent(raw_df)
        chart_paths = visualization_agent(clean_df)

        print("Charts saved at:")
        for path in chart_paths:
            print(path)

    except Exception as e:
        print(e)
