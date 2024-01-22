import json

class ListToJson:
    def __init__(self, data):
        self.data = data

    def to_json(self):
        json_data = {
            "items": self.data
        }
        return json_data