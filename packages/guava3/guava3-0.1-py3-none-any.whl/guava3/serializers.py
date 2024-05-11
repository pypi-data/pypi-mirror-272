from guava3.entities import Interaction, ChatOpenAI, Agent, User, Tool, ChatAnthropic, ChatAzureOpenAI, ChatBedrockAnthropic
from guava3.function_library import FUNCTION_MAP
import re
from copy import deepcopy


def deserialize_chatopenai(data):
    return ChatOpenAI(**data)

def deserialize_chatazureopenai(data):
    return ChatAzureOpenAI(**data)

def deserialize_chatoanthropic(data):
    return ChatAnthropic(**data)

def deserialize_chatbedrockanthropic(data):
    return ChatBedrockAnthropic(**data)

providers_deserializors = {"openai": deserialize_chatopenai, "azureopenai":deserialize_chatazureopenai, "anthropic": deserialize_chatoanthropic, "bedrockanthropic": deserialize_chatbedrockanthropic}

def deserialize_interaction(data, agent_dict, user_dict, tool_dict):
    entity_str = data['entity']
    entity = agent_dict.get(entity_str) or user_dict.get(entity_str) or tool_dict.get(entity_str)
    
    data['entity'] = entity
    if 'listen_regex' in data:
        data['listen_regex'] = re.compile(data['listen_regex'])
    if 'call_regex' in data:
        data['call_regex'] = re.compile(data['call_regex'])
    return Interaction(**data)

def deserialize_messages(messages_data):
    return [(item['role'], item['message']) for item in messages_data]

def deserialize_from_json(data):
    data = deepcopy(data)
    # First, create Agent, User, and Tool objects without interactions
    agents = [Agent(**{k: v for k, v in agent_data.items() if k not in ('interactions', 'llm', 'chat_history', 'prompt')}) for agent_data in data.get('agents', [])]
    users = [User(**{k: v for k, v in user_data.items() if k not in ('interactions', 'chat_history')}) for user_data in data.get('users', [])]
    tools = [Tool(**{k: v for k, v in tool_data.items() if k not in ('interactions', 'chat_history')}) for tool_data in data.get('tools', [])]

    # Create dictionaries for Agent, User, and Tool based on their names
    agent_dict = {agent.name: agent for agent in agents}
    user_dict = {user.name: user for user in users}
    tool_dict = {tool.name: tool for tool in tools}

    # Identify the first_speaker
    first_speaker_name = data.get('first_speaker')
    first_speaker = agent_dict.get(first_speaker_name) or user_dict.get(first_speaker_name) or tool_dict.get(first_speaker_name)
    
    # Deserialize additional fields using helper functions
    for agent_data in data.get('agents', []):
        agent = agent_dict[agent_data['name']]
        if 'llm' in agent_data:
            provider = agent_data['llm'].get('provider', 'openai')
            agent_data['llm'].pop('provider', None)
            agent.llm = providers_deserializors[provider](agent_data['llm'])
        if 'prompt' in agent_data:
            agent.prompt = deserialize_messages(agent_data['prompt'])
        if 'chat_history' in agent_data:
            agent.chat_history = deserialize_messages(agent_data['chat_history'])
        if 'interactions' in agent_data:
            agent.interactions = [deserialize_interaction(interaction_data, agent_dict, user_dict, tool_dict) for interaction_data in agent_data.get('interactions', [])]
    for user_data in data.get('users', []):
        user = user_dict[user_data['name']]
        if 'chat_history' in user_data:
            user.chat_history = deserialize_messages(user_data['chat_history'])
        if 'interactions' in user_data:
            user.interactions = [deserialize_interaction(interaction_data, agent_dict, user_dict, tool_dict) for interaction_data in user_data.get('interactions', [])]
    for tool_data in data.get('tools', []):
        tool = tool_dict[tool_data['name']]
        if 'chat_history' in tool_data:
            tool.chat_history = deserialize_messages(tool_data['chat_history'])
        if 'interactions' in tool_data:
            tool.interactions = [deserialize_interaction(interaction_data, agent_dict, user_dict, tool_dict) for interaction_data in tool_data.get('interactions', [])]
        if 'function' in tool_data:
            tool.function = FUNCTION_MAP.get(tool_data['function'])

    return {"agents": agents, "users": users, "tools": tools, "first_speaker": first_speaker}

