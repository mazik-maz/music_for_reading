import requests
key = 'AIzaSyBLTJ5eRS-kd3f12agjhwIsVvs4M_WCaA0'

def get_features_from_text(text):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}'
    headers = {
        "Content-Type": "application/json"
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Analyze text: {text}\n\n and give only 3 numbers without text, separated by a space:\n"
                         f"first: from 60 to 190, which will represent tempo of text like in music, for example 100-130 most common values.\n"
                         f"second: from 0 to 1000, which will describe its energy. Energy is a measure which represents a perceptual measure of intensity and activity. Typically, energetic texts feel fast, loud, and noisy;\n"
                         f"third: from 0 to 1000, which will describe its valence, where 0 is the most sad text, and 100 is the happiest;"
                    }
                ]
            }
        ],
        "safetySettings": [
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        result = [int(elem) for elem in result['candidates'][0]['content']['parts'][0]['text'].split()]
        result[1] = result[1] / 1000
        result[2] = result[2] / 1000 
        return tuple(result)
    else:
        raise Exception(f"API call failed with status code {response}")
    
text = '''The monster was running right behind me, I could feel its breath on my back, the wind from its claws, I didn't know where to run next, as there was a dead end ahead of me'''
answer = get_features_from_text(text)

print(answer)