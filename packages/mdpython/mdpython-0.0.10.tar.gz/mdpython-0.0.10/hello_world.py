from mdpython.datautils import jsonutil

out_fl = r"C:\Users\Dell\Onedrive\Desktop\out.csv"

json_data = [
    {
        "name": "John",
        "age": 30,
        "car": {
            "make": "Toyota",
            "model": "Camry"
        },
        "colors": ["red", "blue", "green"]
    }, {
        "name": "Sheema",
        "age": 25,
        "car": {
            "make": "Audi",
            "model": "a4",
            "dimension": [5000, 1850, 1433]
        },
        "colors": ["blue", "yellow"]
    }, {
        "name": "Bruce",
        "car": {
            "make": "Ford"
        }
    }
]

jsonutil.list_to_csv(json_data, out_fl)
