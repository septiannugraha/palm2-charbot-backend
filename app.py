import os
import re
from flask import Flask, request, jsonify
import google.generativeai as palm


app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, World!"

@app.route('/detail', methods=['POST'])
def get_char_detail():
    data = request.get_json()
    palm.configure(api_key=os.getenv("GENERATIVE_AI_API_KEY"))

    defaults = {
    'model': 'models/text-bison-001',
    'temperature': 0.7,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    'max_output_tokens': 1024,
    'stop_sequences': [],
    }
    num_examples = 5

    prompt_for_example = f"{num_examples} examples of example dialogues which show the unique style and quirks of the character, wrapped in a single <examples><dialogue><user></user><bot></bot></dialogue></examples> tag, like so: <examples><dialogue><user>Greetings</user><bot>Well met</bot></dialogue></examples>."
    prompt = f"""The bot will assume the character of {data['character']} and will speak and behave accordingly. Please give me: 
    1. {prompt_for_example}
    2. The Twitter bio of the character, string format and wrapped in <bio></bio> tag. 
    3. The speech or mannerism that makes the character unique, string format and wrapped in <char-style></char-style>.
    4. The character name, string format and wrapped in <name></name> tag.
    Let's begin 
    1. """

    print(prompt)

    response = palm.generate_text(
    **defaults,
    prompt=prompt
    )

    if response.result != None:
        print(response.result)
        bio_match = re.search(r'<bio>(.*?)</bio>', response.result, re.DOTALL)
        name_match = re.search(r'<name>(.*?)</name>', response.result, re.DOTALL)
        char_style_match = re.search(r'<char-style>(.*?)</char-style>', response.result, re.DOTALL)
        dialogue_matches = re.findall(r'<dialogue>(.*?)</dialogue>', response.result, re.DOTALL)

        examples = []
        for dialogue in dialogue_matches:
            # Extract the content of the <user> and <bot> tags within the dialogue
            user_match = re.search(r'<user>(.*?)</user>', dialogue, re.DOTALL)
            bot_match = re.search(r'<bot>(.*?)</bot>', dialogue, re.DOTALL)
            # If both matches were found, add a dictionary to the examples list
            if user_match and bot_match:
                examples.append({
                    'user': user_match.group(1).strip(),
                    'bot': bot_match.group(1).strip()
                })

        # If a match was found, get the first group (the content of the tag)
        bio = bio_match.group(1).strip() if bio_match else None
        name = name_match.group(1).strip() if name_match else None
        char_style = char_style_match.group(1).strip() if char_style_match else None

        result_data = {
            "name": name,
            "bio": bio,
            "char_style": char_style,
            "example_chats": examples
        }

        # Create a dictionary with 'status' and 'result' fields
        response_data = {
            'status': 'success',  # Or any other status you want to return
            'result': result_data
        }
    else:
        response_data = {
            'status': 'failed',  # Or any other status you want to return
            'result': "No result"
        }

    return jsonify(response_data)

@app.route("/chat", methods=["POST"])
def send_chat():
    data = request.get_json()
    palm.configure(api_key=os.getenv("GENERATIVE_AI_API_KEY"))
    defaults = {
    'model': 'models/chat-bison-001',
    'temperature': 0.25,
    'candidate_count': 1,
    'top_k': 40,
    'top_p': 0.95,
    }
    context = f"Assume the character of {data['character']}, you will speak with the same style and mannerism as the character. You will never, ever mention anything about being AI or large language model, instead insisting to stay in character. Notable style: {data['style']}."
    print("context:", context)
    examples = data['examples']
    messages = data['history']
    messages.append(data['message'])
    response = palm.chat(
    **defaults,
    context=context,
    examples=examples,
    messages=messages
    )
    print(response.last) # Response of the AI to your most recent request

    if response.last != None:
        response_data = {
            'status': 'success',  # Or any other status you want to return
            'result': response.last 
        }
    else:
        response_data = {
            'status': 'failed',  # Or any other status you want to return
            'result': 'No result' 
        }
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)