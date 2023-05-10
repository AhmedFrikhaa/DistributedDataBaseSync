import json
from datetime import date


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)


class CustomJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.custom_decoder, *args, **kwargs)

    def custom_decoder(self, obj):
        for key, value in obj.items():
            # Check if the value is a string and can be parsed as a date
            if isinstance(value, str):
                try:
                    obj[key] = date.fromisoformat(value)
                except ValueError:
                    pass  # value is not a date string
        return obj
