import json
import os

class TelegramAgent:
    def __init__(self, config_file='agent_config.json'):
        self.config_file = config_file
        self.data = self.load_state()

    def load_state(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {'token': None, 'active': False}

    def save_state(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.data, f)

    def set_token(self, token):
        self.data['token'] = token
        self.save_state()

    def run(self):
        print('Agent pornit cu starea:', self.data)