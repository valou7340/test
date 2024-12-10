import requests  
import json

class NetworkManager:
    def __init__(self):
        self.server_url = ""

    def get_response(self, model, message, data):
        accumulated_response = ""
        try:
            request_data = {
                "model": model,
                "messages": [{"role": "user", "content": message}],
                "temperature": data["temperature"],
                "max_tokens": data["max_tokens"],
                "stream": True  
            }
            response = requests.post(f"{self.server_url}/v1/chat/completions", json=request_data, stream=True)

            for line in response.iter_lines():
                if line:
                    line = line.decode('utf-8')
                    if line.startswith("data: "):
                        json_data = line[6:]
                        if json_data == "[DONE]":
                            break  
                        try:
                            response_json = json.loads(json_data)
                            content = response_json['choices'][0]['delta'].get('content', '')
                            if content:
                                accumulated_response += content  
                        except json.JSONDecodeError:
                            print("Erreur de décodage JSON:", json_data)

            return accumulated_response

        except requests.exceptions.RequestException as e:
            return f"Erreur : {str(e)}"