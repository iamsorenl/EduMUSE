from crewai import Flow, start, listen
from orchestrator.models import OrchestratorState
from orchestrator.crews.content_crew.content_crew import ContentCrew

class OrchestratorFlow(Flow[OrchestratorState]):
    """OrchestratorFlow: runs each crew task in sequence based on state changes."""

    @start()
    def get_user_input(self, state: OrchestratorState) -> OrchestratorState:
        # Initialize with the raw user question
        state.user_input = self.input  # CLI/UI input is available as self.input
        return state

    @listen("state.user_input")
    def run_user_profile(self, state: OrchestratorState) -> OrchestratorState:
        # Track or update user profile from raw input
        result = ContentCrew().run_task("user_profile_task", inputs={"text": state.user_input})
        state.user_profile = result
        return state

    @listen("state.user_profile")
    def run_parse_query(self, state: OrchestratorState) -> OrchestratorState:
        # Parse the question into structured tasks
        result = ContentCrew().run_task("parse_query_task", inputs=state.user_profile)
        state.parsed_query = result
        return state

    @listen("state.parsed_query")
    def run_retrieval(self, state: OrchestratorState) -> OrchestratorState:
        # Fetch relevant facts/documents
        result = ContentCrew().run_task("retrieve_facts_task", inputs=state.parsed_query)
        state.retrieval_results = result
        return state

    @listen("state.retrieval_results")
    def run_planning(self, state: OrchestratorState) -> OrchestratorState:
        # Create an execution plan
        result = ContentCrew().run_task("plan_execution_task", inputs=state.retrieval_results)
        state.execution_plan = result
        return state

    @listen("state.execution_plan")
    def run_execution(self, state: OrchestratorState) -> OrchestratorState:
        # Execute each step of the plan
        result = ContentCrew().run_task("execute_plan_task", inputs=state.execution_plan)
        state.execution_outputs = result
        return state

    @listen("state.execution_outputs")
    def run_evaluation_and_feedback(self, state: OrchestratorState) -> OrchestratorState:
        # Evaluate execution outputs
        eval_result = ContentCrew().run_task("evaluate_output_task", inputs=state.execution_outputs)
        # Assemble final response
        feedback = ContentCrew().run_task("assemble_feedback_task", inputs=eval_result)
        state.final_response = feedback
        return state
