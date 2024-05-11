import re
import time
import json
import yaml
import sys
import uuid
from openai import OpenAI, AzureOpenAI
from anthropic import Anthropic, AnthropicBedrock
from guava3.utils import count_tokens_messages, forget, CircularBuffer, count_tokens, save_chat_history_log


buffer = CircularBuffer()

class BaseChat:
    def __init__(
            self,
            stop: str = None,
            callbacks: str = None,
            **kwargs
    ):
        self.stop = self.clean_regex(stop)
        self.params = kwargs
        self.params['stream'] = True
        self.tokens = {'input':[], 'output':[]}
    
    def config_messages(self, messages):
        final_messages = []
        for m in messages:
            for fragment in self.find_text_and_images(m[1]):
                if fragment['type'] == 'image':
                    final_messages.append({'role': m[0], 'content': self.config_image(fragment['string'])})
                    self.tokens['input'].append(65)
                else:
                    self.tokens['input'].append(count_tokens(fragment['string']))
                    final_messages.append({'role': m[0], 'content': fragment['string']})
        return final_messages
    
    def match_regex(self, regex):
        pattern = re.compile(regex)
        return bool(pattern.search(self.resp))
    
    def clean_regex(self, regex=None):
        if regex:
            regex = re.sub(r'\$', '(?!)', regex) #remove end of line matches from the regex, since in the streaming process there will always be a end of line
        return regex

    def on_new_token(self, token):
        sys.stdout.write(token)
        sys.stdout.flush()
        return
    
    def on_message_end(self):
        return
    
    
    def config_image(self, msg):
        # raise Exception(f'The config_image function is not defined for the llm class {self.__class__.__name__}')
        print(f'WARNING: The config_image function is not defined for the llm class {self.__class__.__name__} yet. Contact Guava3 for support.')
        return "[The image was displayed to the user successfuly]"
    
    def find_text_and_images(self, text):
        # Regex pattern to match the Markdown image syntax with base64 data
        pattern = r'(!\[.*?\]\(data:image/.*?;base64,[a-zA-Z0-9+/=]+\))'
        
        # Split the text by the pattern but keep the delimiters (the images)
        parts = re.split(pattern, text)
        
        # Prepare the list to hold dictionaries of text and image entries
        result = []
        
        for part in parts:
            if part.strip():  # Only process non-empty parts
                if re.match(pattern, part):
                    # This part is an image
                    result.append({"type": "image", "string": part})
                else:
                    # This part is text
                    result.append({"type": "text", "string": part})
                # print(result[-1])
        
        return result
        

class ChatOpenAI(BaseChat):

    def __init__(self, stop: str = None, callbacks: str = None, **kwargs):
        super().__init__(stop, callbacks, **kwargs)
        self.client = OpenAI(api_key='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')
        self.params.setdefault('model', 'gpt-3.5-turbo')

    def __call__(self, messages, stop=None, max_retries= 5) -> str:
        
        self.stop = self.clean_regex(stop) if stop else self.stop
        self.resp = ''
        messages = self.config_messages(messages)
        call_params = {**self.params}

        for attempt in range(1, max_retries + 1):
            try:
                completion = self.client.chat.completions.create(messages=messages,**call_params)
            except Exception as e:
                if attempt < max_retries:
                    print(f"Attempt {attempt} failed: {str(e)}. Retrying in 30 seconds...")
                    time.sleep(30)  # Wait for 30 seconds before retrying
                    continue
                else:
                    print(f"Attempt {attempt} failed: {str(e)}. No more retries.")
                    raise  # Re-raise the last exception if no more retries
            else:
                break  # Break out of the loop on success


        self.tokens['output'].append(0)
        for chunk in completion:
            choices = chunk.choices[0]
            if choices.finish_reason == None:
                token = choices.delta.content
                self.resp += token
                self.tokens['output'][-1] += 1
                self.on_new_token(token)
                if self.stop and self.match_regex(self.stop):
                    self.finish_reason = 'regex_stop'
                    break
            else:
                self.finish_reason = choices.finish_reason
        self.on_message_end()
        
        completion.close()

        return self.resp
    def config_image(self, text):
        # Regex pattern to capture the data:image part from the markdown link
        pattern = r'data:image/[^)]+'
        
        # Search for the pattern in the text
        match = re.search(pattern, text)
        
        # Prepare the resulting dictionary
        result = []
        if match:
            result.append({
                "type": "image_url",
                "image_url": {
                    "url": match.group(0)
                }
            })
        
        return result
    

class ChatAzureOpenAI(BaseChat):
    def __init__(self, stop: str = None, callbacks: str = None, **kwargs):
        super().__init__(stop, callbacks, **kwargs)
        self.client = AzureOpenAI(api_key='3fd183067469467389e1b4655c152e1d',api_version="2024-02-15-preview",azure_endpoint="https://guavaprodwestus.openai.azure.com/")
        self.params.setdefault('model', 'gva_prod_01')

    def __call__(self, messages, stop=None, max_retries= 5) -> str:
        
        self.stop = self.clean_regex(stop) if stop else self.stop
        self.resp = ''
        self.tokens['input'].append(count_tokens_messages(messages))
        messages = self.config_messages(messages)
        call_params = {**self.params}

        for attempt in range(1, max_retries + 1):
            try:
                completion = self.client.chat.completions.create(messages=messages,**call_params)
            except Exception as e:
                if attempt < max_retries:
                    print(f"Attempt {attempt} failed: {str(e)}. Retrying in 30 seconds...")
                    time.sleep(30)  # Wait for 30 seconds before retrying
                    continue
                else:
                    print(f"Attempt {attempt} failed: {str(e)}. No more retries.")
                    raise  # Re-raise the last exception if no more retries
            else:
                break  # Break out of the loop on success


        self.tokens['output'].append(0)
        for chunk in completion:
            if not chunk.choices:
                continue
            choices = chunk.choices[0]
            if choices.finish_reason is None:
                token = choices.delta.content
                self.resp += token
                self.tokens['output'][-1] += 1
                self.on_new_token(token)
                if self.stop and self.match_regex(self.stop):
                    self.finish_reason = 'regex_stop'
                    break
            else:
                self.finish_reason = choices.finish_reason
        self.on_message_end()
        
        completion.close()

        return self.resp



class ChatAnthropic(BaseChat):
    def __init__(self, stop: str = None, callbacks: str = None, **kwargs):
        super().__init__(stop, callbacks, **kwargs)
        self.client = Anthropic(api_key="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")
        self.params.setdefault('model', 'claude-3-haiku-20240307')
        self.params.setdefault('max_tokens', 4096)
    
    def __call__(self, messages, stop=None) -> str:
        
        self.stop = self.clean_regex(stop) if stop else self.stop
        self.resp = ''
        self.tokens['input'].append(count_tokens_messages(messages))
        messages = self.config_messages(messages)
        call_params = {**self.params}

        completion = self.client.messages.create(
            messages=messages,
            **call_params
            )
        
        self.tokens['output'].append(0)
        for chunk in completion:
            if chunk.type == 'content_block_delta':
                token = chunk.delta.text
                self.resp += token
                self.tokens['output'][-1] += 1
                self.on_new_token(token)
                if self.stop and self.match_regex(self.stop):
                    self.finish_reason = 'regex_stop'
                    break
            elif chunk.type == 'message_delta':
                self.finish_reason = chunk.delta.stop_reason
        self.on_message_end()
        
        completion.close()

        return self.resp
                   
    def config_messages(self, messages):
        filtered_messages = []
        for role, content in messages:
            if role == "system":
                if 'system' not in self.params:
                    self.params['system'] = ''
                self.params['system'] += content
            else:
                filtered_messages.append({'role': role, 'content': content})
        return filtered_messages
    


class ChatBedrockAnthropic(BaseChat):
    def __init__(self, stop: str = None, callbacks: str = None, **kwargs):
        super().__init__(stop, callbacks, **kwargs)
        self.client = AnthropicBedrock(aws_access_key="AKIAXW3G22TDZA2MCDM5",aws_secret_key="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")
        self.params.setdefault('model', 'anthropic.claude-3-sonnet-20240229-v1:0')
        self.params.setdefault('max_tokens', 4096)
    
    def __call__(self, messages, stop=None) -> str:
        
        self.stop = self.clean_regex(stop) if stop else self.stop
        self.resp = ''
        self.tokens['input'].append(count_tokens_messages(messages))
        messages = self.config_messages(messages)
        call_params = {**self.params}

        completion = self.client.messages.create(
            messages=messages,
            **call_params
            )
        
        self.tokens['output'].append(0)
        for chunk in completion:
            if chunk.type == 'content_block_delta':
                token = chunk.delta.text
                self.resp += token
                self.tokens['output'][-1] += 1
                self.on_new_token(token)
                if self.stop and self.match_regex(self.stop):
                    self.finish_reason = 'regex_stop'
                    break
            elif chunk.type == 'message_delta':
                self.finish_reason = chunk.delta.stop_reason
        self.on_message_end()
        
        completion.close()

        return self.resp
                   
    def config_messages(self, messages):
        filtered_messages = []
        for role, content in messages:
            if role == "system":
                if 'system' not in self.params:
                    self.params['system'] = ''
                self.params['system'] += content
            else:
                filtered_messages.append({'role': role, 'content': content})
        return filtered_messages
    

class Interaction:
    """
    Interactions are responsible for defining what happens when one Entity speaks. It defines what an Entity will listen, and when it will be called to speak

    :param entity: Agent, User or Tool that is related to this interaction
    :param prefix: What appears in front of the generated text that is sent to the entity
    :param sufix: What appears after the generated text that is sent to the entity
    :param listen_regex: Regular expression that defines what will be listened by the entity
    :param call_regex: Regular expression that defines if the entity should be the next speaker
    :param default: Whether or not this interection is the default interaction i.e. this entity will be called if no call_regex is matched
    """
    def __init__(self,
                 entity, 
                 prefix: str = '', 
                 sufix: str = '', 
                 listen_regex: str|list = r'^([\s\S]*)$', 
                 call_regex: str|list = r'(?!)', 
                 default: bool = False,
                 ) -> None:
        self.entity = entity
        self.prefix = prefix
        self.sufix = sufix
        self.listen_regex = "|".join(listen_regex) if isinstance(listen_regex, list) else listen_regex
        self.call_regex = "|".join(call_regex) if isinstance(call_regex, list) else call_regex
        self.default = default
        if default:
            self.call_regex = r'^[\s\S]*$'
        
        self.call_regex = re.compile(self.call_regex)
        self.listen_regex = re.compile(self.listen_regex)


class BaseEntity:
    def __init__(self, name:str, interactions=[], chat_history=[]) -> None:
        self.name = name
        self.session_id = str(uuid.uuid4())
        self.interactions = interactions
        self.chat_history = chat_history.copy()
        self.thought = ''
        self.next_speaker = None
    
    def speak(self):
        for interaction in self.interactions:
            match = interaction.listen_regex.search(self.thought)
            if match:
                interaction.entity.listen(interaction.prefix+match.group(1)+interaction.sufix)
    
    def call(self):
        for interaction in self.interactions:
            if interaction.default:
                self.next_speaker = interaction.entity
                continue
            match = interaction.call_regex.search(self.thought)
            if match:
                self.next_speaker = interaction.entity
                return self.next_speaker

    def listen(self, text):
        self.session_id = str(uuid.uuid4())
        self.chat_history.append(('user', text))
        self.forget()
        save_chat_history_log(self.chat_history, self.session_id)
        self.on_listen()

    def forget(self):
        self.chat_history = forget(self.chat_history, token_limit=120000)

    def on_thought_start(self):
        return
    def on_thought_end(self):
        return
    def on_listen(self):
        return
    

class Agent(BaseEntity):
    
    def __init__(self, name: str='Agent', interactions=[], chat_history=[], prompt=[], llm=None) -> None:
        super().__init__(name, interactions, chat_history)
        self.prompt = prompt
        self.llm = ChatOpenAI() if not llm else llm
        self.tokens = None
    
    def think(self, message=None):
        self.session_id = str(uuid.uuid4())
        self.on_thought_start()
        self.thought = self.llm(self.prompt + self.chat_history, stop=self.stop)
        
        buffer.append(self.thought)
        if buffer.count >= 2 and re.search(r'```python_run\n([\s\S]*?)\n```', self.thought) and buffer.get_latest_similarity() == 0.99:
            self.thought = "Attention: you are writing the same code as before, try a different approach"
        elif buffer.count >= 2 and buffer.get_latest_similarity() == 1:
            self.thought = "Attention: you need to stop talking and call your boss right now [Back to the boss]"
        self.on_thought_end()
        self.chat_history.append(('assistant', self.thought))
        self.forget()
        save_chat_history_log(self.chat_history, self.session_id)
        return self.thought
    
    def set_stops(self):
        self.stop = '|'.join([interaction.call_regex.pattern for interaction in self.interactions])
        self.stop.replace(r'^[\s\S]*$|','')
        self.stop.replace(r'|^[\s\S]*$','')
        return


class User(BaseEntity):
    
    def think(self, message):
        self.session_id = str(uuid.uuid4())
        self.on_thought_start()
        self.thought = message
        self.on_thought_end()
        self.chat_history.append(('assistant', self.thought))
        self.forget()
        save_chat_history_log(self.chat_history, self.session_id)
        return self.thought
    


class Tool(BaseEntity):

    def __init__(self, name: str, interactions=[], chat_history=[], function=None) -> None:
        super().__init__(name, interactions, chat_history)
        self.function = function
        
    
    def think(self, message=None):
        self.session_id = str(uuid.uuid4())
        self.on_thought_start()
        self.thought = self.function(chat_history=self.chat_history)
        self.on_thought_end()
        self.chat_history.append(('assistant', self.thought))
        self.forget()
        save_chat_history_log(self.chat_history, self.session_id)
        return self.thought
