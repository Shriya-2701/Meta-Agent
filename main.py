from meta_agent import generate_agent
import json

def run_test():
    print("\n=== Meta-Agent CX Configurator ===")
    user_input = input("\nDescribe the agent you want to build:\n> ")
    
    try:
        # Call the Groq-powered Meta Agent
        config = generate_agent(user_input)
        
        print("\n[SUCCESS] Configuration Generated!")
        print(f"Agent Name: {config.agent_name}")
        print(f"Persona: {config.persona[:75]}...")
        
        # Save the result
        filename = "deployed_agent.json"
        with open(filename, "w") as f:
            f.write(config.model_dump_json(indent=2))
            
        print(f"\nFull deployable JSON saved to: {filename}")
        
    except Exception as e:
        print(f"\n[ERROR] Could not generate config: {e}")

if __name__ == "__main__":
    run_test()