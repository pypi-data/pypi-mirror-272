from mdpython.datautils import jsonutil
import json

json_data = {
    "name": "John",
    "age": 30,
    "car": {
        "make": "Toyota",
        "model": "Camry"
    },
    "colors": ["red", "blue", "green"],
    "nested_list": [
        [1, 2, 3],
        {"hello": "world"},
        [[7, 8], [9, 10]],
        [[[11, 12], [13, 14]], [[], [17, 18]]]
    ],
    "nested_dict": {
        "info1": {"key1": "value1"},
        "info2": {"key2": "value2"}
    },
    "list_of_dicts": [
        {"item1": "value1"},
        {"item2": "value2"}
    ]
}

flattened_data = jsonutil.flatten_json(json_data)
print(json.dumps(flattened_data, indent=2))
