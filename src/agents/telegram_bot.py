import json
import os

class TelegramAgent:
    def __init__(self, config_path='agent_data.json'):
        self.config_path = config_path
        self.memory = self.load_state()

    def load_state(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {'context': [], 'history': []}

    def save_state(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.memory, f)

    def update_memory(self, new_data):
        self.memory['context'].append(new_data)
        self.save_state()

    def run(self, message):
        self.update_memory(message)
        return f'Processed: {message}'