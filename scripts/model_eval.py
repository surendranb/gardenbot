import base64
import requests
import json
import os

# Configuration
# Using the key from env: OPENROUTER_API_KEY=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
API_KEY = "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"
IMAGE_PATH = "/Users/surendran/.openclaw/workspace/gardenbot/media/latest.jpg"
MODELS = [
    "nvidia/nemotron-3-super-120b-a12b:free",
    "arcee-ai/trinity-large-preview:free",
    "liquid/lfm-2.5-1.2b-thinking:free",
    "openai/gpt-oss-120b:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-27b-it:free"
]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def test_model(model_id, base64_image):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://openclaw.ai",
        "X-Title": "GardenWarden-Eval"
    }
    
    payload = {
        "model": model_id,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this garden image. IDENTIFY: 1. Any non-plant objects (figurines, wires). 2. Plant health (turgidity/wilting). 3. Soil appearance. Be concise but specific."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    }
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=35)
        if response.status_code != 200:
             return {"error": response.text, "status_code": response.status_code}
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def main():
    if not os.path.exists(IMAGE_PATH):
        print(f"Error: Image not found at {IMAGE_PATH}")
        return

    base64_image = encode_image(IMAGE_PATH)
    results = {}

    for model in MODELS:
        print(f"Testing {model}...")
        res = test_model(model, base64_image)
        results[model] = res
        
    with open("logs/model_eval_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    print("\nEvaluation complete. Results saved to logs/model_eval_results.json")

if __name__ == "__main__":
    main()
