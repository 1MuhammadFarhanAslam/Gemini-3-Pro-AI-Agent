from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent
from google.adk.agents import agent_tool
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.core.invocation_context import InvocationContext
from google.adk.core.events import Event, Content, Part
from google.adk.agents.base_agent import BaseAgent
from google.adk.core.agent import AgentConfig
# Step 1: Define specialized agents

# # Mock tool implementation
# def get_current_time(city: str) -> dict:
#     """Returns the current time in a specified city."""
#     return {"status": "success", "city": city, "time": "10:30 AM"}

# my_agent = Agent(
#     model='gemini-2.0-flash-exp',
#     name='root_agent',
#     description="Tells the current time in a specified city.",
#     instruction="You are a helpful assistant that tells the current time in cities. Use the 'get_current_time' tool for this purpose.",
#     tools=[get_current_time],

# )

# Flight Agent: Specializes in flight booking and information
flight_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="FlightAgent",
    description="Flight booking agent",
    instruction=f"""You are a flight booking agent... You always return a valid JSON...""")

# Hotel Agent: Specializes in hotel booking and information
hotel_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="HotelAgent",
    description="Hotel booking agent",
    instruction=f"""You are a hotel booking agent... You always return a valid JSON...""")

# Sightseeing Agent: Specializes in providing sightseeing recommendations
sightseeing_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="SightseeingAgent",
    description="Sightseeing information agent",
    instruction=f"""You are a sightseeing information agent... You always return a valid JSON...""")

# Root agent acting as a Trip Planner coordinator
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="TripPlanner",
    instruction=f"""
    Acts as a comprehensive trip planner.
    - Use the FlightAgent to find and book flights
    - Use the HotelAgent to find and book accommodation
    - Use the SightSeeingAgent to find information on places to visit
    ...
    """,
    sub_agents=[flight_agent, hotel_agent, sightseeing_agent] # The coordinator manages these sub-agents
)

# Step 2: Give your coordinator tools 

# Convert specialized agents into AgentTools
flight_tool = agent_tool.AgentTool(agent=flight_agent)
hotel_tool = agent_tool.AgentTool(agent=hotel_agent)
sightseeing_tool = agent_tool.AgentTool(agent=sightseeing_agent)

# Root agent now uses these agents as tools
root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name="TripPlanner",
    instruction=f"""Acts as a comprehensive trip planner...
    Based on the user request, sequentially invoke the tools to gather all necessary trip details...""",
    tools=[flight_tool, hotel_tool, sightseeing_tool] # The root agent can use these tools
)

# Step 3: Implement parallel execution 

# 1. Create a parallel agent for concurrent tasks
plan_parallel = ParallelAgent(
    name="ParallelTripPlanner",
    sub_agents=[flight_agent, hotel_agent], # These run in parallel
)

# 2. Create a summary agent to gather results
trip_summary = LlmAgent(
    name="TripSummaryAgent",
    instruction="Summarize the trip details from the flight, hotel, and sightseeing agents...",
    output_key="trip_summary")

# 3. Create a sequential agent to orchestrate the full workflow
root_agent = SequentialAgent(
    name="PlanTripWorkflow",
    # Run tasks in a specific order, including the parallel step
    sub_agents=[sightseeing_agent, plan_parallel, trip_summary])

# Step 4: Create feedback loops 
# Agent to check if the trip summary meets quality standards
trip_summary_reviewer = LlmAgent(
    name="TripSummaryReviewer",
    instruction=f"""Review the trip summary in {{trip_summary}}.
    If the summary meets quality standards, output 'pass'. If not, output 'fail'""",
    output_key="review_status", # Writes its verdict to a new key
)

# Custom agent to check the status and provide feedback

class ValidateTripSummary(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        status = ctx.session.state.get("review_status", "fail")
        review = ctx.session.state.get("trip_summary", None)
        if status == "pass":
            yield Event(author=self.name, content=Content(parts=[Part(text=f"Trip summary review passed: {review}")]))
        else:
            yield Event(
                content=Content(parts=[Part(author=self.name,
  text="Trip summary review failed. Please provide a valid requirements")]))
ValidateTripSummaryAgent = ValidateTripSummary(
    name="ValidateTripSummary",
    description="Validates the trip summary review status and provides feedback based on the review outcome.",)

# The final, self-regulating workflow
root_agent = SequentialAgent(
    name="PlanTripWorkflow",
    sub_agents=[
        sightseeing_agent,
        plan_parallel,
        trip_summary,
        trip_summary_reviewer,
        ValidateTripSummaryAgent() # The final validation step 
])


if __name__ == "__main__":
    respose = root_agent.run("Plan a trip to Paris including flight, hotel, and sightseeing.")
    print(respose)