import requests

# Konfigurasi Gemini API
gemini_api_key = 'AIzaSyCE1AGLlCHoC3T4zC69osT4-xGZng8XAEM'
gemini_url = 'https://generativelanguage.googleapis.com/v1/models/gemini-pro:generateContent'

def fetch_mitigation_from_gemini(rule_name):
    headers = {'Content-Type': 'application/json'}
    data = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    {
                        'text': (f"Provide mitigation steps and details for the following rule:\n"
                                 f"Rule Name: {rule_name}\n"
                                 f"Please include a detailed explanation of the attack and steps to mitigate it.")
                    }
                ]
            }
        ]
    }
    params = {'key': gemini_api_key}
    response = requests.post(gemini_url, headers=headers, json=data, params=params)
    
    if response.status_code == 200:
        json_response = response.json()
        if 'candidates' in json_response and len(json_response['candidates']) > 0:
            candidate = json_response['candidates'][0]
            if 'content' in candidate and 'parts' in candidate['content'] and len(candidate['content']['parts']) > 0:
                return candidate['content']['parts'][0]['text']
            else:
                return "Tidak ada detail mitigasi yang ditemukan dalam respons."
        else:
            return "Tidak ada kandidat yang ditemukan dalam respons."
    else:
        return f"Error: {response.status_code}"
