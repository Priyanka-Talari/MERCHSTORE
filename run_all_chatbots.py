import sys
from threading import Thread
import subprocess
import time

# Get the correct Python interpreter path
python_path = sys.executable  # Gets the correct Python running this script

# Define chatbot scripts and their ports
chatbots = [
    {"script": "app_jasmine.py", "port": 5000},
    {"script": "app_doraemon.py", "port": 5001},
    {"script": "app_peter.py", "port": 5002},
]

# Function to start a chatbot script
def run_chatbot(script, port):
    while True:
        print(f"Starting {script} on port {port}...")
        process = subprocess.Popen([python_path, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = process.communicate()

        if stderr:
            print(f"{script} crashed! Restarting in 5 seconds...\nError:\n{stderr.decode()}")
            time.sleep(5)  # Wait before restarting

# Start all chatbots in separate threads
threads = []
for chatbot in chatbots:
    thread = Thread(target=run_chatbot, args=(chatbot["script"], chatbot["port"]), daemon=True)
    thread.start()
    threads.append(thread)

# Keep the main thread alive
while True:
    time.sleep(1)
