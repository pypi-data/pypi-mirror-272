import sys
import os
import tiktoken
import time
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def save_chat_history_log(chat_history, session_id, file_path='resources/chat_history_log.json'):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    timestamp = int(time.time())
    data_to_save = [{
        "session_id": session_id,
        "role": message[0],  # 'user' ou 'assistant'
        "text": message[1],  # texto da mensagem
        "timestamp": timestamp
    } for message in chat_history]

    try:
        with open(file_path, 'a', encoding='utf-8') as f:  # Usando 'a' para anexar a cada salvamento
            for entry in data_to_save:
                f.write(json.dumps(entry) + "\n")  # Salva cada entrada como uma linha JSON
    except Exception as e:
        print(f"Erro ao salvar o log do chat_history: {e}")

def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4")
    return len(encoding.encode(text))
    
def count_tokens_messages(msgs):
    # Check if msgs is a list and all elements are tuples with exactly two string elements
    if not all(isinstance(msg, tuple) and len(msg) == 2 and all(isinstance(field, str) for field in msg) for msg in msgs):
        raise ValueError("Input must be a list of tuples, each with exactly two string elements.")

    t = 0
    for msg in msgs:
        for field in msg:
            t += count_tokens(field)
    return t

def forget(messages, token_limit):
    """
    This function returns the most recent messages (from the end of the list) such that their total token count 
    is less than or equal to a specified limit.
    
    Parameters:
        messages (list): A list of tuples in the format [('user', 'message 1'), ('assistant', 'message 2'), ...]
        token_limit (int): The maximum allowable total token count for the returned messages
    
    Returns:
        list: A list of tuples representing the messages that fit within the token limit.
    """
    recent_messages = []
    total_tokens = 0
    
    # Iterating through the messages in reverse order to get the most recent messages first.
    for sender, message in reversed(messages):
        message_tokens = count_tokens(message)
        
        # If adding the current message doesn't exceed the token limit, add it to the list.
        if total_tokens + message_tokens <= token_limit:
            recent_messages.append((sender, message))
            total_tokens += message_tokens
        # If adding the current message would exceed the token limit, skip it.
        else:
            print('forgot something')
            break
        
    # Returning the messages in their original order.
    return list(reversed(recent_messages))

initial_globals = set(globals().keys())

def show_global_variables():
    global_vars = globals().copy()
    filtered_globals = {
        k: v for k, v in global_vars.items()
        if not k.startswith('__') and not hasattr(v, '__call__') and not isinstance(v, type(sys))
    }
    return filtered_globals

class CircularBuffer:

    def __init__(self, capacity = 3):
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0
        self.similarities = [None] * capacity

    def append(self, item):
        self.buffer[self.tail] = item
        self.tail = (self.tail + 1) % len(self.buffer)
        if self.count < len(self.buffer):
            self.count += 1
        else:
            self.head = (self.head + 1) % len(self.buffer)
        self.update_similarities()

    def get(self):
        if self.count == 0:
            return []
        result = []
        index = self.head
        for _ in range(self.count):
            result.append(self.buffer[index])
            index = (index + 1) % len(self.buffer)
        return result
    
    def compare_paragraph_similarity(self, para1, para2):
        # Initialize the vectorizer
        vectorizer = TfidfVectorizer()

        # Fit and transform the paragraphs
        tfidf_matrix = vectorizer.fit_transform([para1, para2])

        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

        return similarity[0][0]

    def update_similarities(self):
        if self.count < 2:
            return None

        for i in range(self.count):
            message1 = self.buffer[(self.head + i) % len(self.buffer)]
            message2 = self.buffer[(self.head + (i + 1) % self.count) % len(self.buffer)]
            similarity = self.compare_paragraph_similarity(message1, message2)
            self.similarities[(self.head + i) % len(self.buffer)] = similarity

        return self.similarities
    
    def get_similarities(self):
        if self.count < 2:
            return None
        result = []
        index = self.head
        for _ in range(self.count):
            if self.similarities[index] is not None:
                result.append(self.similarities[index])
            index = (index + 1) % len(self.buffer)
        return result

    def get_latest_similarity(self):
        if self.count < 2:
            return None
        return self.similarities[(self.tail - 1) % len(self.buffer)]
        
    def clear(self, capacity = 3):
        self.buffer = [None] * capacity
        self.head = 0
        self.tail = 0
        self.count = 0
        self.similarities = [None] * capacity

