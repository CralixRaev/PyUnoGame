import os
import threading
import time
import subprocess

processes = []


def thread(num):
    processes.append(subprocess.run(
        ['D:\\PyUnoGame\\venv\\Scripts\\python.exe', 'D:\\PyUnoGame\\client\\main.py', f'user{num}',
         'pass'],
        capture_output=True))


for i in range(1, 5):
    print(i)
    a = threading.Thread(target=thread, args=(i,))
    a.start()
    time.sleep(2)
