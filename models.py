from pydantic import BaseModel, Field
from typing import List, Optional

class ToolDefinition(BaseModel):
    name: str = Field(description="Name of the function, e.g., get_availability")
    description: str = Field(description="What this tool does for the agent")
    parameters: dict = Field(description="JSON schema of arguments needed")

class CXAgentConfig(BaseModel):
    agent_name: str
    persona: str = Field(description="The personality and instructions for the bot")
    voice_type: str = Field(description="Suggested voice style (e.g., Professional, Warm)")
    greeting: str = Field(description="The very first thing the bot says")
    steps: List[str] = Field(description="Step-by-step logic the bot follows")
    tools: List[ToolDefinition]