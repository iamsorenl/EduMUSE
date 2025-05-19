# main.py

from orchestrator import run_pipeline

if __name__ == "__main__":
    # Mock input text
    mock_input = """
    Artificial Intelligence (AI) is the simulation of human intelligence in machines.
    It is used in education, healthcare, finance, and entertainment. Subfields include 
    machine learning, computer vision, and natural language processing. AI systems 
    learn from data and make predictions or decisions.
    """

    # User profile 
    user_level = "novice"

    print("Running EduMUSE Orchestrator Pipeline...\n")
    final_state = run_pipeline(mock_input, user_level)

    print("\n🎯 Final Output Bundle Path:", final_state.get("bundle_path", "[NOT GENERATED]"))