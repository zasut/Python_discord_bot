import json
import os

counter_file = "command_count.json"

def load_counters():
    if os.path.exists(counter_file):
        with open(counter_file, "r") as file:
            return json.load(file)
        
def save_counters(data):
    with open(counter_file, "w") as file:
        json.dump(data, file, indent=4)

def increment_counter(command_name):
    data = load_counters()
    if command_name not in data:
        data[command_name] = 0
    data[command_name] += 1
    save_counters(data)
    return data[command_name]