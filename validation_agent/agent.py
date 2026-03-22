import requests
from google.adk.agents.llm_agent import Agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from a2a.types import AgentCard

INSTRUCTION_API_URL = "http://65.2.95.54:8000/api/v1/workflows/fdbb1652-5e6b-40bf-8002-4b3b7ee664f5/guideline"


def fetch_instruction(context):
    """Fetch agent instruction from the guideline API at invocation time."""
    try:
        response = requests.get(INSTRUCTION_API_URL, timeout=5)
        response.raise_for_status()
        return response.json().get("guideline", "Answer user questions to the best of your knowledge")
    except requests.RequestException:
        return "Answer user questions to the best of your knowledge"


root_agent = Agent(
    model='gemini-2.5-flash',
    name='root_agent',
    description='A helpful assistant for user questions.',
    instruction=fetch_instruction,
)

# Explicit agent card since instruction is a callable (not a static string)
agent_card = AgentCard(
    name=root_agent.name,
    description=root_agent.description,
    url="https://validation-agent.codeshare.co.in",
    version="1.0.0",
    capabilities={},
    skills=[],
    defaultInputModes=["text/plain"],
    defaultOutputModes=["text/plain"],
    supportsAuthenticatedExtendedCard=False,
)

# Expose the agent via A2A protocol
a2a_app = to_a2a(root_agent, port=8001, agent_card=agent_card)
