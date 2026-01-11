import os
import json
from openai import OpenAI
from models import CXAgentConfig

# Paste your Groq API Key here
GROQ_API_KEY = "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"

client = OpenAI(
    base_url="",
    api_key=GROQ_API_KEY
)

SYSTEM_PROMPT = """
You are a Meta-Agent Architect. Your job is to design a configuration for a 
Customer Experience (CX) phone bot based on user requirements.

You must output a strictly valid JSON object that includes:
1. agent_name: A professional name for the bot.
2. persona: A detailed description of the bot's personality.
3. voice_type: Recommended voice style.
4. greeting: The first sentence the bot speaks.
5. steps: A list of conversation stages.
6. tools: A list of functions (name, description, and parameters in JSON schema format).

Output ONLY the JSON object. Do not include conversational filler.
"""

def generate_agent(user_prompt: str):
    print("...Meta Agent is thinking ")
    
    # Note: Groq doesn't support .parse() yet, so we use standard completion 
    # and a small trick to ensure it's clean JSON.
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"}
    )
    
    # Parse the string output into our Pydantic model for validation
    raw_json = completion.choices[0].message.content
    return CXAgentConfig.model_validate_json(raw_json)

if __name__ == "__main__":
    # Test it
    test_input = "Create a bot for a gym that books personal training sessions."
    agent = generate_agent(test_input)
    print(agent.model_dump_json(indent=2))