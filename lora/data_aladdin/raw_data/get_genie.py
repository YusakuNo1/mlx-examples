# Read file "all.jsonl", get all the rows of either the next speaker is genie or the speaker is genie
import json
import re

def filter_genie_messages(file_path: str) -> list[dict]:
    """
    Reads a JSONL file and filters messages where the speaker is 'GENIE' or the next speaker is 'GENIE'.

    Args:
        file_path: Path to the JSONL file.

    Returns:
        A list of dictionaries containing the filtered messages.
    """
    filtered_messages = []

    with open(file_path, 'r') as file:
        for line in file:
            message = json.loads(line.strip())
            if message['speaker'] == 'GENIE':
                filtered_messages.append(message)
            elif filtered_messages and filtered_messages[-1]['speaker'] == 'GENIE':
                filtered_messages.append(message)

    return filtered_messages

messages = filter_genie_messages('all.jsonl')
train_messages = []
valid_messages = []

# Get first 10% of message for validation
num_validation = len(messages) // 10
for i, message in enumerate(messages):
    if i < num_validation:
        valid_messages.append(message)
    else:
        train_messages.append(message)

# Write train_messages to train.jsonl and valid_messages to valid.jsonl
with open('../train.jsonl', 'w') as file:
    for message in train_messages:
        output_json = { "text": f"{message['speaker']} : {message['text']}" }
        file.write(json.dumps(output_json) + '\n')

with open('../valid.jsonl', 'w') as file:
    for message in valid_messages:
        output_json = { "text": f"{message['speaker']} : {message['text']}" }
        file.write(json.dumps(output_json) + '\n')
