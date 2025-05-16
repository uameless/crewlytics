from services.llm_service import get_llm_response

def insight_agent(eda_results: dict, chart_paths: list) -> str:
    print("➡️ Generating insight summary with LLM.")

    chart_descriptions = "\n".join([f"- {path}" for path in chart_paths])

    prompt = (
        "You are a data analyst assistant.\n"
        "The user has uploaded a dataset. Based on the following exploratory data analysis (EDA) results and charts, "
        "write a professional summary highlighting key insights, patterns, trends, correlations, and any anomalies.\n\n"
        f"EDA Results:\nDataset shape: {eda_results['dataset_shape']}\n"
        f"Data Types: {eda_results['data_types']}\n"
        f"Summary Statistics: (not shown in detail)\n"
        f"Charts generated:\n{chart_descriptions}\n\n"
        "Write the insights in clear, non-technical business language.\n"
    )

    summary = get_llm_response(prompt)

    print("✅ Insight summary generated.")
    return summary

if __name__ == "__main__":
    from agents.data_ingestion_agent import data_ingestion_agent
    from agents.data_cleaning_agent import data_cleaning_agent
    from agents.eda_agent import eda_agent
    from agents.visualization_agent import visualization_agent

    test_file = "data/products.csv"
    try:
        raw_df = data_ingestion_agent(test_file)
        clean_df = data_cleaning_agent(raw_df)
        eda = eda_agent(clean_df)
        charts = visualization_agent(clean_df)

        summary = insight_agent(eda, charts)
        print("\nGenerated Summary:\n")
        print(summary)

    except Exception as e:
        print(e)
