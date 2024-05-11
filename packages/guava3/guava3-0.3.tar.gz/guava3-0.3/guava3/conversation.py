from guava3.serializers import deserialize_from_json
from guava3.entities import User
import yaml
import json


class Conversation:
    def __init__(self, team_config: str) -> None:
        self.team_config = team_config
        self.team = deserialize_from_json(self.load_team_config(team_config))
        self.is_running = False
        self.speaker = self.team['first_speaker']
        for agent in self.team['agents']:
            agent.set_stops()
    
    def load_team_config(self, filepath: str = 'resources/team_configs/gpt-4.yaml'):
        if filepath.endswith('.json'):
            with open(filepath, 'r') as file:
                return json.load(file)
        elif filepath.endswith(('.yml', '.yaml')):
            with open(filepath, 'r') as file:
                return yaml.safe_load(file)
        else:
            raise ValueError("Unsupported file format. Please use JSON or YAML.")
    
    def run(self, message):

        while self.speaker:
            if isinstance(self.speaker, User):
                self.speaker.think(message)
            else:
                self.speaker.think()
            self.speaker.speak()
            self.speaker.call()
            self.speaker = self.speaker.next_speaker
            if isinstance(self.speaker, User):
                break
        
        return self.speaker.chat_history[-1][1]
    
    def get_tokens(self):
        input_tokens = 0
        output_tokens = 0

        for agent in self.team['agents']:
            input_tokens += sum(agent.llm.tokens['input'])
            output_tokens += sum(agent.llm.tokens['output'])
        
        return {'input': input_tokens, 'output': output_tokens}