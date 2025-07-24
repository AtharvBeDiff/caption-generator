import requests

API_KEY = ""  # Put your OpenRouter API key here
API_URL = ""

def generate_caption(topic):
    if not topic.strip():
        return "Please enter a valid topic."

    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "openai/gpt-3.5-turbo",  # Free, powerful model
            "messages": [
                {"role": "system", "content": "You are a fun social media caption generator."},
                {"role": "user", "content": f"Generate a cool Instagram caption about: {topic}"}
            ],
            "temperature": 0.7,
            "max_tokens": 100
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content'].strip()
        else:
            return f"Something went wrong: {response.status_code} - {response.text}"

    except Exception as e:
        return f"Error: {str(e)}"


# Simple interface
if __name__ == "__main__":
    topic = input("Enter the caption topic: ")
    caption = generate_caption(topic)
    print("\nGenerated Caption:\n", caption)