import json
import os

class ModelScope:
    def __init__(self, state_file='agent_state.json'):
        self.state_file = state_file
        self.memory = self.load_state()

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {'history': [], 'context': 'stable'}

    def save_state(self):
        with open(self.state_file, 'w') as f:
            json.dump(self.memory, f)

    def update_memory(self, new_data):
        self.memory['history'].append(new_data)
        self.save_state()

    def run(self):
        print('Agent initialized with state: ' + str(self.memory['context']))