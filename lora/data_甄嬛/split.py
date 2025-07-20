# Read a json file name "huanhuan.json", it only has 1 list of dicts, split it into train and test sets named "train.jsonl" and "valid.jsonl".

split_percentage = 0.9
input_file_name = "huanhuan.json"

def split(input_file_name, percentage):
    import json
    import random

    with open(input_file_name, "r") as f:
        data = json.load(f)

    # In data, it only has 1 list of dicts, each dict has 2 fields "instruction" and "output". Get these 2 fields
    # and convert them into a single field "text" in the new dicts, in a format like f"Instruction: {instruction}\nResponse: {output}"
    data = [{"text": f"Instruction: {item['instruction']}\nResponse: {item['output']}"} for item in data]

    random.shuffle(data)
    split_index = int(len(data) * percentage)

    train_data = data[:split_index]
    valid_data = data[split_index:]

    with open("train.jsonl", "w", encoding='utf-8') as f:
        for item in train_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open("valid.jsonl", "w", encoding='utf-8') as f:
        for item in valid_data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")


split(input_file_name= input_file_name, percentage=split_percentage)
