
import os
import json
import base64
from openai import OpenAI
from PIL import Image
import io

# Initialize OpenAI client
client = OpenAI(api_key='')

def encode_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        return base64.b64encode(img_buffer.getvalue()).decode('utf-8')

def caption_image(image_path):
    base64_image = encode_image(image_path)
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image. Wtite in phrase, Do not write in sentence. Always start with 'aideatelineart style, pencil sketch'"},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ],
            }
        ],
        max_tokens=300,
    )
    
    return response.choices[0].message.content

def main(folder_path, output_file):
    results = []
    
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            image_path = os.path.join(folder_path, filename)
            caption = caption_image(image_path)
            results.append({"file_name": filename, "text": caption})
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    folder_path = "/Users/patarapoom/Downloads/birme-1024xauto"
    output_file = "captions.json"
    main(folder_path, output_file)
