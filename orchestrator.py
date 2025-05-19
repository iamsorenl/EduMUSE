from crewai import Agent, Task, Crew
from state_utils import update_state, validate_state_keys, save_state_to_json, print_final_state

from agents import summarizer, pacer, keywords, assessment, podcast, bundler

def define_agents():
    return {
        "summarizer": summarizer.create_agent(),
        "pacer": pacer.create_agent(),
        "keywords": keywords.create_agent(),
        "assessment": assessment.create_agent(),
        "podcast": podcast.create_agent(),
        "bundler": bundler.create_agent()
    }

def define_tasks(agents):
    return [
        Task(
            agent=agents["summarizer"],
            description="Summarize the raw input text into structured topic-wise segments.",
            expected_output="summary",
            context_variables=["raw_text"],
            output_key="summary"
        ),
        Task(
            agent=agents["pacer"],
            description="Adapt the summary based on user expertise level (novice/normal/expert).",
            expected_output="adjusted_summary",
            context_variables=["summary", "expertise_level"],
            output_key="adjusted_summary"
        ),
        Task(
            agent=agents["keywords"],
            description="Extract key terms and recommend linked resources.",
            expected_output="recommendations",
            context_variables=["adjusted_summary"],
            output_key="recommendations"
        ),
        Task(
            agent=agents["assessment"],
            description="Generate 5-10 practice questions based on adjusted summary.",
            expected_output="assessment_questions",
            context_variables=["adjusted_summary"],
            output_key="assessment_questions"
        ),
        Task(
            agent=agents["podcast"],
            description="Generate a podcast-style audio from the adjusted summary.",
            expected_output="podcast_audio",
            context_variables=["adjusted_summary"],
            output_key="podcast_audio"
        ),
        Task(
            agent=agents["bundler"],
            description="Compile all outputs into a downloadable bundle.",
            expected_output="bundle_path",
            context_variables=[
                "adjusted_summary",
                "recommendations",
                "assessment_questions",
                "podcast_audio"
            ],
            output_key="bundle_path"
        )
    ]

def create_initial_state(raw_text, user_level="normal"):
    state = {
        "raw_text": raw_text,
        "expertise_level": user_level
    }
    print("🧠 Initialized state:")
    print(state)
    return state

def run_pipeline(raw_text, user_level="normal"):
    state = create_initial_state(raw_text, user_level)
    agents = define_agents()
    tasks = define_tasks(agents)
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=True
    )

    print("\nStarting Crew Run...\n")
    result = crew.run(
        input={"raw_text": raw_text},
        context=state  
    )

    print("\n Crew Run Complete.")
    print_final_state(state)
    save_state_to_json(state)

    return state