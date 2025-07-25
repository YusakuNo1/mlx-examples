import re, json

def parse_conversation(conversation_text: str) -> list[dict]:
    """
    Parses a multi-line conversation string into a list of dictionaries,
    where each dictionary represents a chat message with a 'speaker' and 'text'.

    The format expected is:
    - Each new message starts with a speaker's name (uppercase letters)
      followed by a colon and the first line of the message.
    - Subsequent lines of the same chat message are indented (start with whitespace)
      and are appended to the previous message's text.

    Args:
        conversation_text: A string containing the entire conversation.

    Returns:
        A list of dictionaries, each with 'speaker' and 'text' keys.
        Example: [{'speaker': 'ALADDIN', 'text': 'Uh, Al--uh--Aladdin.'}, ...]
    """
    parsed_messages = []
    current_speaker = None
    current_message_lines = []

    # Split the conversation into individual lines
    lines = conversation_text.splitlines()

    # Flag to track if we're currently inside a parenthetical block to ignore
    ignoring_parenthetical = False

    for line in lines:
        # Check if this line starts a parenthetical block to ignore
        if line.lstrip().startswith('('):
            ignoring_parenthetical = True
            continue  # Skip this line
        
        # If we're ignoring a parenthetical block, check if this line is indented or empty
        if ignoring_parenthetical:
            if line.strip() == "" or line.startswith(' ') or line.startswith('\t'):
                continue  # Skip indented or empty lines following the parenthetical
            else:
                # Non-indented, non-empty line - end of parenthetical block
                ignoring_parenthetical = False
                # Fall through to normal processing

        # Regex to find a speaker name (uppercase letters) followed by a colon
        # and capture the rest of the line as the message content.
        # r"^([A-Z]+):\s*(.*)" matches:
        # ^          - start of the line
        # ([A-Z]+)   - captures one or more uppercase letters (speaker name)
        # :          - literal colon
        # \s* - zero or more whitespace characters
        # (.*)       - captures the rest of the line (message content)
        match = re.match(r"^([A-Z]+):\s*(.*)", line)

        if match:
            # If a match is found, this line signifies the start of a new message.
            # First, check if there was a previous message being built.
            if current_speaker is not None:
                # If so, join its lines and add it to the parsed_messages list.
                parsed_messages.append({
                    "speaker": current_speaker,
                    "text": " ".join(line.strip() for line in current_message_lines)
                })

            # Update the current speaker and start a new list for the message lines.
            current_speaker = match.group(1)  # The captured speaker name
            current_message_lines = [match.group(2)] # The first line of the message
        elif current_speaker is not None and (line.startswith(' ') or line.startswith('\t')):
            # If no speaker match, but a message is currently active (current_speaker is not None),
            # and the line starts with whitespace (indicating indentation),
            # then it's a continuation of the current message.
            # Append the line, preserving its leading whitespace as per the sample format.
            current_message_lines.append(line)
        elif line.strip() == "" and current_speaker is not None:
            # Handle empty lines that might appear within a message.
            # If a message is active, include the empty line to preserve spacing.
            current_message_lines.append("")
        else:
            # This handles cases where a line doesn't start with a speaker, isn't indented,
            # and isn't empty, but a message is still active. This implies it's a
            # continuation line that might not have explicit indentation, but
            # still belongs to the previous speaker. This is a fallback to ensure
            # all content is captured if the indentation is inconsistent.
            if current_speaker is not None:
                current_message_lines.append(line)
            else:
                # This case would occur if the conversation starts with non-message text
                # or if there's a block of unidentifiable text between messages.
                # For this problem, we assume conversations start with a speaker.
                print(f"Warning: Line skipped or unhandled before first speaker or unexpected format: '{line}'")


    # After iterating through all lines, add the very last message to the list.
    if current_speaker is not None:
        parsed_messages.append({
            "speaker": current_speaker,
            "text": " ".join(line.strip() for line in current_message_lines)
        })

    return parsed_messages

# Parse the sample conversation
with open("Aladdin.txt", "r") as file:
    sample_conversation = file.read()
    parsed_data = parse_conversation(sample_conversation)

with open('all.jsonl', 'w') as file:
    for message in parsed_data:
        # output_json = { "text": f"{message['speaker']} : {message['text']}" }
        # file.write(json.dumps(output_json) + '\n')
        file.write(json.dumps(message) + '\n')
