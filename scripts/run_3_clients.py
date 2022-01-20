import os
import subprocess
import threading
import time

processes = []


def thread(num):
    print(os.getcwd())
    process = subprocess.run(
        ['../venv/Scripts/python.exe',
         '../client/main.py', f'user{num}',
         'pass'],
        capture_output=True)
    print(process.stderr)


for i in range(2, 5):
    print(i)
    a = threading.Thread(target=thread, args=(i,))
    a.start()
    time.sleep(2)
