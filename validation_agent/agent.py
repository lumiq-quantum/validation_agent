import requests
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

INSTRUCTION_API_URL = "https://your-api.example.com/agent/instruction"


def fetch_instruction(context):
    """Fetch agent instruction from an API at invocation time."""
    try:
        response = requests.get(INSTRUCTION_API_URL, timeout=5)
        response.raise_for_status()
        return response.json().get("instruction", "Answer user questions to the best of your knowledge")
    except requests.RequestException:
        return "Answer user questions to the best of your knowledge"


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=fetch_instruction,
)

# Expose the agent via A2A protocol
a2a_app = to_a2a(root_agent, port=8001)
