import time
from flask import stream_with_context, request, Flask
import random
import json
import tiktoken
import tiktoken

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """
    Renvoie le nombre de tokens dans une chaîne de texte.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    print(num_tokens)
    return num_tokens

def truncate_text(text: str, max_tokens: int, encoding_name: str) -> str:
    """
    Coupe le début du texte si le nombre de tokens dépasse max_tokens.
    """
    num_tokens = num_tokens_from_string(text, encoding_name)
    if num_tokens <= max_tokens:
        return text
    else:
        tokens_to_remove = num_tokens - max_tokens
        tokens_removed = 0
        truncated_text = ""
        for token in text.split():
            tokens_removed += len(token.split())
            if tokens_removed > tokens_to_remove:
                truncated_text += token + " "
                break
            truncated_text += token + " "
        return truncated_text.strip()

# Exemple d'utilisation :
my_text = "Votre texte ici..."
max_tokens = 4000
truncated_text = truncate_text(my_text, max_tokens, "cl100k_base")
print(truncated_text)

app = Flask(__name__)

templatesNormalAnswer = {
    "id": "chatcmpl-xhupa2rchg83b24moow73w",
    "object": "chat.completion",
    "created": 1710920536,
    "model": "ChatGPT-3.5-Turbo",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hello, I'm a bot, programmed for fun,\nTo chat in rhymes, from dusk till done.\nSo welcome to my world of verse,\nWhere every word is a rehearse.\nLet's embark on this poetic course,\nThrough the labyrinth of rhythm and lore.",
            },
            "finish_reason": "stop",
        }
    ],
    "usage": {"prompt_tokens": 71, "completion_tokens": 70, "total_tokens": 141},
}


templatesStreamAnswer = {
    "id": "chatcmpl-[UUID]",
    "object": "chat.completion.chunk",
    "created": 1710920504,
    "model": "ChatGPT-3.5-Turbo",
    "choices": [
        {
            "index": 0,
            "delta": {"role": "assistant", "content": ""},
            "finish_reason": None,
        }
    ],
}


@app.route("/api/info", methods=["POST"])
def post():
    f = open("inst.json", "r")
    content = f.read()
    f.close()
    return content
    return "Success"


@app.route("/api/set", methods=["POST"])
def get():
    data = json.loads(request.data)
    if data["type"] == "first":
        f = open("inst.json", "w")
        f.write(json.dumps({"isActive": False, "message": ""}))
        f.close()
        f = open("tmp.txt", "w")
        f.write(data["content"])
        f.close()
    elif data["type"] == "update":
        f = open("tmp.txt", "w")
        f.write(data["content"])
        f.close()
    elif data["type"] == "end":
        f = open("tmp.txt", "w")
        f.write(data["content"] + "END")
        f.close()
    return "Success"


@app.route("/v1/chat/completions", methods=["POST"])
def streamed_response():
    def generateOneLine():
        while True:
            with open("tmp.txt", "r") as f:
                content = f.read().strip()
                time.sleep(0.5)

                if content.endswith("END"):
                    current = templatesNormalAnswer
                    current["choices"][0]["message"]["content"] = content[:-3]
                    current["id"] = "chatcmpl-" + str(random.randint(0, 10000000))
                    current["created"] = time.time()
                    return json.dumps(current)

    def generate():
        currentText = ""
        while True:
            with open("tmp.txt", "r") as f:
                content = f.read().strip()
                time.sleep(0.5)
                currentAnswer = templatesStreamAnswer
                currentAnswer["id"] = "chatcmpl-" + str(random.randint(0, 10000000))
                currentAnswer["created"] = time.time()

                if content.endswith("END"):
                    currentAnswer["choices"][0]["delta"]["content"] = content[
                        :-3
                    ].replace(currentText, "")
                    currentAnswer["choices"][0]["finish_reason"] = "stop"
                    yield "data: " + json.dumps(currentAnswer) + "\n\n"
                    time.sleep(0.5)
                    yield "data: [DONE]"
                    break
                else:
                    currentAnswer["choices"][0]["delta"]["content"] = content.replace(
                        currentText, ""
                    )
                    yield "data: " + json.dumps(currentAnswer) + "\n\n"
                currentText = content

    data = json.loads(request.data)
    messagesText = ""
    for message in data["messages"]:
        if message["role"] == "system":
            messagesText += (
                "\n An global instruction has been defined: " + message["content"]
            )
        elif message["role"] == "user":
            messagesText += "\n IMPORTANT: The user asked/says: " + message["content"]
        elif message["role"] == "assistant":
            messagesText += "\n You answered: " + message["content"]
    print(messagesText)
    f = open("tmp.txt", "w")
    f.write("")
    f.close()
    f = open("inst.json", "w")
    f.write(json.dumps({"isActive": True, "message": truncate_text(messagesText, 4000, "cl100k_base")}))
    f.close()
    if data.get("stream"):
        print("Stream!")
        return app.response_class(
            stream_with_context(generate()), content_type="application/json"
        )
    else:
        return generateOneLine()
