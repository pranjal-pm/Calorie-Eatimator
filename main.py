from openai import OpenAI
from dotenv import load_dotenv
import base64
import json
import sys
import os

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client using your API key from .env
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_calories_from_image(image_path):
    # Read image and convert to base64
    with open(image_path, "rb") as image:
        base64_image = base64.b64encode(image.read()).decode("utf-8")

    # Call GPT-4o with image input
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "system",
                "content": """You are a dietitian. A user sends you an image of a meal and you tell them how many calories are in it. Use the following JSON format:
{
  "reasoning": "reasoning for the total calories",
  "food_items": [
    {
      "name": "food item name",
      "calories": "calories in the food item"
    }
  ],
  "total": "total calories in the meal"
}"""
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "How many calories are in this meal?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            },
        ],
        response_format="json"  # ✅ Correct format
    )

    # Extract JSON result from response
    response_message = response.choices[0].message.content
    return json.loads(response_message)

if __name__ == "__main__":
    image_path = sys.argv[1]
    result = get_calories_from_image(image_path)
    print(json.dumps(result, indent=2))
