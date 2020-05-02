import os
import time

from worker import WorkerQueue
import database

def startApp():
    queue = WorkerQueue()

    while True:
        try:
            source = input('\nEnter file directory: ')
            results = getFiles(source)

            for item in results:
                queue.insert(item)

            print('Directory found.')
            time.sleep(1)
            break

        except FileNotFoundError:
            print('File not found. Try again')
            time.sleep(1)

    while queue.length > 0:
        database.enterData(queue)
        print('Entering data...')
        time.sleep(2)

    print('Successful Import')


def getFiles(directory):
    files = []

    def traverse(current_dir):
        current_files = os.listdir(current_dir)

        for filename in current_files:
            path = current_dir + '/' + filename
            if os.path.isfile(path):
                files.append(path)
            elif os.path.isdir(path):
                traverse(path)

        return

    traverse(directory)
    return files

startApp()

