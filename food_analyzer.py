import os
from openai import OpenAI
from PIL import Image
import base64
from io import BytesIO
import json

def get_openai_client():
    """Initialize and return OpenAI client with proper error handling."""
    try:
        # Read API key from config file
        with open('config.json', 'r') as f:
            config = json.load(f)
            api_key = config.get('openai_api_key')
        
        if not api_key or api_key == "your-api-key-here":
            raise ValueError("Please update the API key in config.json with your actual OpenAI API key.")
        
        return OpenAI(api_key=api_key)
    except FileNotFoundError:
        raise ValueError("config.json file not found. Please create it with your OpenAI API key.")
    except json.JSONDecodeError:
        raise ValueError("Invalid config.json file format. Please check the file structure.")

def analyze_food_image(image_path):
    """
    Analyze a food image using OpenAI's Vision API and return nutritional information.
    """
    try:
        # Initialize OpenAI client
        client = get_openai_client()
        
        # Open and encode the image
        with Image.open(image_path) as img:
            # Convert image to base64
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this food image and provide:
                            1. List of food items visible
                            2. Estimated calories for each item
                            3. Portion sizes
                            4. Nutritional value
                            5. Health recommendations
                            6. Meal balance suggestions
                            Format the response in a structured way."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_str}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000
        )

        # Extract the analysis from the response
        analysis = response.choices[0].message.content

        # Format the result
        result = {
            "reasoning": analysis,
            "food_items": [{"name": "Analyzed food", "calories": "See analysis", "portion": "See analysis"}],
            "total": "See analysis",
            "nutritional_value": analysis,
            "health_recommendation": analysis,
            "meal_balance": analysis,
            "suggestions": analysis
        }

        return result

    except ValueError as e:
        return {
            "error": str(e),
            "reasoning": "API Key Error",
            "food_items": [],
            "total": "N/A",
            "nutritional_value": "API Key not set",
            "health_recommendation": "Please update config.json with your API key",
            "meal_balance": "N/A",
            "suggestions": "Update your OpenAI API key in config.json and try again"
        }
    except Exception as e:
        return {
            "error": str(e),
            "reasoning": "Analysis Error",
            "food_items": [],
            "total": "N/A",
            "nutritional_value": "Analysis failed",
            "health_recommendation": "Unable to provide recommendations",
            "meal_balance": "Analysis failed",
            "suggestions": "Please try again with a different image"
        }

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        result = analyze_food_image(image_path)
        print(json.dumps(result, indent=2)) 
