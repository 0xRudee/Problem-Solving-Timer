import time
import json
import threading
from pynput import keyboard

# Storage functions
def save_data(data, filename="task_data.json"):
    with open(filename, "w") as f:
        json.dump(data, f)

def load_data(filename="task_data.json"):
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

class TaskTracker:
    def __init__(self):
        self.current_task = None
        self.task_times = load_data()
        self.start_time = None

    def switch_task(self, new_task):
        if self.current_task:
            elapsed_time = time.time() - self.start_time
            self.task_times[self.current_task] = self.task_times.get(self.current_task, 0) + elapsed_time
        
        self.current_task = new_task
        self.start_time = time.time()
        print(f"Switched to {new_task}")

    def save(self):
        if self.current_task:
            elapsed_time = time.time() - self.start_time
            self.task_times[self.current_task] = self.task_times.get(self.current_task, 0) + elapsed_time
        save_data(self.task_times)

    def load(self):
        self.task_times = load_data()

tracker = TaskTracker()

COMBINATION = {keyboard.Key.shift}
current_keys = set()
activities = {'~!': 'Reading', '~@': 'Thinking', '~#': 'Coding', '~$': 'Debugging'}

def on_press(key):
    try:
        current_keys.add(key)
        if COMBINATION.issubset(current_keys) and hasattr(key, 'char') and key.char in activities:
            tracker.switch_task(activities[key.char])
    except AttributeError:
        pass

def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    tracker.load()
    
    listener_thread = threading.Thread(target=start_listener, daemon=True)
    listener_thread.start()
    
    print("Task Tracker Running... Press Ctrl + Shift + [1-4] to switch tasks.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Saving data and exiting...")
        tracker.save()
