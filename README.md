# Gemini-3-Pro-AI-Agent

A powerful AI agent built with Google's Agent Development Kit (ADK) using Gemini 2.0 Flash model.

## Prerequisites

- Python 3.13+
- Google Cloud Project with Gemini API access
- UV package manager (recommended) or pip

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd Gemini-3-Pro-AI-Agent

# Install dependencies with UV
uv sync

# Or with pip
pip install -e .
```

### 2. Environment Configuration

```bash
# Create .env file in my_agent directory
echo "GOOGLE_API_KEY=your_api_key_here" > my_agent/.env
```

### 3. Run the Agent

```bash
# Run the main application
python main.py

# Or run the agent directly
python my_agent/agent.py
```

## ADK Commands Reference

### Agent Creation

```python
from google.adk.agents.llm_agent import Agent

# Create a new agent
agent = Agent(
    model='gemini-2.0-flash-exp',
    name='your_agent_name',
    description="Agent description",
    instruction="System instructions for the agent",
    tools=[your_tools_list]
)
```

### Running Agents

```python
# Single query
response = agent.run("Your question here")

# Interactive mode
agent.chat()
```

### Tool Integration

```python
# Define a tool function
def your_tool(param: str) -> dict:
    """Tool description"""
    return {"result": "tool output"}

# Add to agent
agent = Agent(
    tools=[your_tool],
    # ... other parameters
)
```

## Development Commands

### Project Management

```bash
# Install new dependencies
uv add package_name

# Update dependencies
uv sync

# Run tests
python -m pytest

# Format code
black .
ruff check .
```

### Agent Development

```bash
# Create new agent module
mkdir agents/new_agent
touch agents/new_agent/__init__.py
touch agents/new_agent/agent.py
```

## Project Structure

```
Gemini-3-Pro-AI-Agent/
├── my_agent/
│   ├── __init__.py
│   ├── agent.py          # Main agent implementation
│   └── .env             # Environment variables
├── main.py              # Entry point
├── pyproject.toml       # Project configuration
├── README.md           # This file
└── uv.lock            # Dependency lock file
```

## Configuration

### Environment Variables

Create `my_agent/.env`:

```env
GOOGLE_API_KEY=your_google_api_key
MODEL_NAME=gemini-2.0-flash-exp
AGENT_NAME=root_agent
```

### Model Options

- `gemini-2.0-flash-exp` (recommended)
- `gemini-1.5-pro`
- `gemini-1.5-flash`

## Usage Examples

### Basic Agent

```python
from google.adk.agents.llm_agent import Agent

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='helper_agent',
    description="A helpful assistant",
    instruction="You are a helpful AI assistant."
)

response = agent.run("Hello, how are you?")
print(response)
```

### Agent with Tools

```python
def get_weather(city: str) -> dict:
    """Get weather for a city"""
    return {"city": city, "weather": "sunny", "temp": "25°C"}

agent = Agent(
    model='gemini-2.0-flash-exp',
    name='weather_agent',
    tools=[get_weather]
)

response = agent.run("What's the weather in London?")
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   ```bash
   # Verify API key is set
   echo $GOOGLE_API_KEY
   ```

2. **Import Errors**
   ```bash
   # Reinstall dependencies
   uv sync --force
   ```

3. **Model Access**
   ```bash
   # Check model availability
   python -c "from google.genai import Client; print('API accessible')"
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

See LICENSE file for details.