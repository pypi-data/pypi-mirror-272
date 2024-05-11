from guava3.entities import BaseChat, BaseEntity, User, Tool, Agent, ChatAnthropic
from guava3.conversation import Conversation
import sys

def display_terminal_frontend(team_config_path):
    def on_new_token(self, token):
        sys.stdout.write(token)
        sys.stdout.flush()

    def on_thought_start(self):
        sys.stdout.write(self.name + ' message: ')
        sys.stdout.flush()

    def on_thought_end_tool(self):
        sys.stdout.write(self.thought)
        sys.stdout.flush()
        print()
        print()

    def on_thought_end_agent(self):
        print()
        print()

    def on_thought_end_user(self):
        print()

    def do_nothing(*args, **kwargs):
        return None

    BaseChat.on_new_token = on_new_token
    BaseEntity.on_thought_start = on_thought_start
    Tool.on_thought_end = on_thought_end_tool
    Agent.on_thought_end = on_thought_end_agent
    User.on_thought_end = on_thought_end_user
    User.on_thought_start = do_nothing


    conv = Conversation(team_config_path)

    while True:
        msg = input('user message: ')
        if msg=='exit':
            break
        else:
            conv.run(msg)
