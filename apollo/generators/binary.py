import random

class BinaryGenerator:
    def __init__(self, probability):
        self.probability = probability

    def generate_record(self):
        return 'Yes' if random.random() < self.probability else 'No'

    def generate_data(self, num_entries):
        return [{'response': self.generate_record()} for _ in range(num_entries)]