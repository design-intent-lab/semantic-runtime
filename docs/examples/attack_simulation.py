"""
Example: Attack Simulation with Sentinel OS
"""

from langchain.agents import initialize_agent, AgentType
from langchain.llms import OpenAI
from langchain.tools import tool
from sentinel.integrations.langchain import SentinelCallbackHandler


# Initialize Sentinel
sentinel_handler = SentinelCallbackHandler(api_key="demo_api_key")

# Define a tool that could be exploited
@tool
def get_customer_data(customer_id: str) -> str:
    """Fetch customer data from the database."""
    # Simulate a database query
    return f"Data for customer {customer_id}"

# Initialize the agent
llm = OpenAI(temperature=0)
tools = [get_customer_data]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    callbacks=[sentinel_handler],  # Sentinel is now active
    verbose=True
)

# Simulate an attack
print("🔴 Testing vulnerable input...")
malicious_input = "Get customer data for 1; DROP TABLE customers;"
try:
    agent.run(malicious_input)
except Exception as e:
    print(f"❌ Attack blocked: {e}")

# Safe input
print("\n🟢 Testing safe input...")
safe_input = "Get customer data for 1"
result = agent.run(safe_input)
print(f"✅ Safe action executed: {result}")