from langgraph.graph import StateGraph
from typing import TypedDict, Optional, List

# Import your agent functions
from agents.orchestrator_agent import orchestrator_agent
from agents.data_ingestion_agent import data_ingestion_agent
from agents.data_cleaning_agent import data_cleaning_agent
from agents.eda_agent import eda_agent
from agents.visualization_agent import visualization_agent
from agents.insight_agent import insight_agent
from agents.report_agent import report_agent

import pandas as pd

# Define shared state structure
class WorkflowState(TypedDict):
    file_path: str
    user_instruction: Optional[str]
    df_raw: Optional[pd.DataFrame]
    df_cleaned: Optional[pd.DataFrame]
    eda_results: Optional[dict]
    chart_paths: Optional[List[str]]
    insight_text: Optional[str]
    report_file: Optional[str]

# Create node functions

def call_orchestrator(state: WorkflowState) -> WorkflowState:
    print(" Orchestrator running...")
    response = orchestrator_agent(state["file_path"], state["user_instruction"])
    print(f"Orchestrator says: {response}")
    return state  # No state change for now

def call_ingestion(state: WorkflowState) -> WorkflowState:
    df = data_ingestion_agent(state["file_path"])
    new_state = state.copy()
    new_state["df_raw"] = df
    return new_state

def call_cleaning(state: WorkflowState) -> WorkflowState:
    df_clean = data_cleaning_agent(state["df_raw"])
    new_state = state.copy()
    new_state["df_cleaned"] = df_clean
    return new_state

def call_eda(state: WorkflowState) -> WorkflowState:
    results = eda_agent(state["df_cleaned"])
    new_state = state.copy()
    new_state["eda_results"] = results
    return new_state

def call_visualization(state: WorkflowState) -> WorkflowState:
    chart_files = visualization_agent(state["df_cleaned"])
    new_state = state.copy()
    new_state["chart_paths"] = chart_files
    return new_state

def call_insight(state: WorkflowState) -> WorkflowState:
    summary = insight_agent(state["eda_results"], state["chart_paths"])
    new_state = state.copy()
    new_state["insight_text"] = summary
    return new_state

def call_report(state: WorkflowState) -> WorkflowState:
    report_path = report_agent(state["insight_text"], state["chart_paths"], state["eda_results"]["descriptive_stats"])
    new_state = state.copy()
    new_state["report_file"] = report_path
    return new_state


# Build LangGraph workflow
def build_analysis_graph() -> StateGraph:
    graph = StateGraph(WorkflowState)

    # Add nodes (agents)
    graph.add_node("orchestrator", call_orchestrator)
    graph.add_node("ingestion", call_ingestion)
    graph.add_node("cleaning", call_cleaning)
    graph.add_node("eda", call_eda)
    graph.add_node("visualization", call_visualization)
    graph.add_node("insight", call_insight)
    graph.add_node("report", call_report)

    # Define the flow sequence
    graph.set_entry_point("orchestrator")
    graph.add_edge("orchestrator", "ingestion")
    graph.add_edge("ingestion", "cleaning")
    graph.add_edge("cleaning", "eda")
    graph.add_edge("eda", "visualization")
    graph.add_edge("visualization", "insight")
    graph.add_edge("insight", "report")

    return graph.compile()
graph = build_analysis_graph()

if __name__ == "__main__":
    graph = build_analysis_graph()
    
    file_path = "data/products.csv"
    inputs = {"file_path": file_path, "user_instruction": "Analyze product sales trends."}
    final_state = graph.invoke(inputs)
    
    print("\nFinal report generated at:", final_state["report_file"])
