from import_file import parse_data

class WorkerQueue:
    def __init__(self):
        self.queue = []
        self.length = 0

    def insert(self, value):
        data_results = parse_data(value)
        self.queue.append(data_results)
        self.length += 1

    def remove(self):
        if self.length == 0:
            return 'No items in queue'
        else:
            self.length -= 1
            return self.queue.pop()

    def search(data_type, key, value):
        pass
            






