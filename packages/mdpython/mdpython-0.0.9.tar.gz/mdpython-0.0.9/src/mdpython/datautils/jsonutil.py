def flatten_json(json_data, parent_key='', separator='.'):
    items = {}
    for key, value in json_data.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else key
        if isinstance(value, dict):
            items.update(flatten_json(value, new_key, separator=separator))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    items.update(flatten_json(item, f"{new_key}{separator}{i}", separator=separator))
                elif isinstance(item, list):
                    items.update(flatten_json({"sublist": item}, f"{new_key}{separator}{i}", separator=separator))
                else:
                    items[f"{new_key}{separator}{i}"] = item
        else:
            items[new_key] = value
    return items