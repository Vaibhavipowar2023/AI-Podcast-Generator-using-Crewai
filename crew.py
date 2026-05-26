from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import CrewBase, agent, task, crew
from tools.tts_tool import generate_podcast_audio
from tavily import TavilyClient
from crewai.tools import tool
from dotenv import load_dotenv
import os
import time

load_dotenv()
BASE_DIR =os.path.dirname(os.path.abspath(__file__))


small_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.3,
    max_retries=5,
    timeout=120,
)

big_llm = LLM(
    model="gemini/gemini-2.5-flash",        # ← free, fast, generous
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7,
    max_retries=5,
    timeout=120,
)
# Search tool
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
@tool("Web Search Tool")
def search_tool(query: str) -> str:
    """Search the web for current information about a topic."""
    try:
        results = tavily_client.search(query=query, max_results=3)
        output = ""
        for r in results.get("results", []):
            content = r['content'][:300]
            output += f"Title: {r['title']}\nContent: {content}\n\n"
        return output[:1000]
    except Exception as e:
        return f"Search failed: {str(e)}"

@CrewBase
class PodcastCrew:
    agents_config = os.path.join(BASE_DIR, "config", "agents.yaml")
    tasks_config = os.path.join(BASE_DIR, "config", "tasks.yaml")

    # Research Agents
    @agent
    def topic_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["topic_researcher"],
            tools=[search_tool],
            llm=small_llm ,
        )

    @agent
    def news_gatherer(self) -> Agent:
        return Agent(
            config=self.agents_config["news_gatherer"],
            tools=[search_tool],
            llm=small_llm ,
        )

    # Creative Agents

    @agent
    def script_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["script_writer"],
            llm=big_llm,
        )

    @agent
    def dialogue_polisher(self) -> Agent:
        return Agent(
            config=self.agents_config["dialogue_polisher"],
            llm=big_llm,
        )

    @agent
    def audio_producer(self) -> Agent:
        return Agent(
            config=self.agents_config["audio_producer"],
            tools=[generate_podcast_audio],
            llm=big_llm,
        )

    # Tasks
    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def news_task(self) -> Task:
        return Task(config=self.tasks_config["news_task"])

    @task
    def script_task(self) -> Task:
        return Task(config=self.tasks_config["script_task"])

    @task
    def polish_task(self) -> Task:
        return Task(config=self.tasks_config["polish_task"])

    @task
    def audio_task(self) -> Task:
        return Task(
            config=self.tasks_config["audio_task"],
            output_file="output/scripts/podcast_script.md",
        )

    # Crew
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents= self.agents,
            tasks= self.tasks,
            process= Process.sequential,
            verbose= True
        )


# Entry point
def run(topic: str):
    inputs = {"topic": topic}
    for attempt in range(3):
        try:
            result = PodcastCrew().crew().kickoff(inputs=inputs)
            return result
        except Exception as e:
            if "rate_limit" in str(e).lower() or "429" in str(e):
                wait = 60 * (attempt + 1)
                print(f"\n Rate limit hit. Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise e
    return None


if __name__ == "__main__":
    import sys
    topic = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Artificial Intelligence"
    print(f"\n Generating podcast on: {topic}\n")
    result = run(topic)
    if result:
        print("\nDone! Check output/audio/podcast.mp3")

