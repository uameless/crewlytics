from services.llm_service import get_llm_response

def orchestrator_agent(data_file_path: str, user_instruction: str = "") -> str:

    prompt = f"You are an AI assistant. The user uploaded a dataset at '{data_file_path}'. Instruction: '{user_instruction}'. What should we do next?"
    
    response = get_llm_response(prompt)
    return response

if __name__ == "__main__":
    result = orchestrator_agent("data/sample_data.csv", "Analyze product sales trends.")
    print(result)
