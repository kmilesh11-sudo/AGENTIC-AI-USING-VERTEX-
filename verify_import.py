import importlib

# Match exactly what ADK fast_api.py does (line 773-775):
# agent_module = importlib.import_module(app_name)
# if getattr(agent_module.agent, "root_agent"):
#     root_agent = agent_module.agent.root_agent

agent_module = importlib.import_module("rag_agent")
print("rag_agent imported OK")
print("agent submodule:", agent_module.agent)
root_agent = agent_module.agent.root_agent
print("root_agent name:", root_agent.name)
print("root_agent model:", root_agent.model)
print("All tools:", [t.__name__ for t in root_agent.tools])
print("\n✅ ADK import pattern works correctly!")
