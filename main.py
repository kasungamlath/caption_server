import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

client = OpenAI()

# PROMPT = "you’re a professional photographer with a large follower base in Instagram. you want to increase the number of your followers. you are going to post the following photo in instagram. now take your time and think of a good instagram caption for this photo. don't include any emojis. don't be cheesy. try to maintain a professional tone. make the first sentence title. no need for special markup for title or newline."
PROMPT = "Create a short, catchy, and engaging Instagram caption for this photo. The caption should reflect the mood of the photo and include an element of humor, inspiration, or a relatable statement. Incorporate relevant hashtags where necessary. don't include any emojis. don't enclose the caption in quotes."


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def get_caption_from_openai(base64_image):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"{base64_image}",
                            "detail": "low",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content


app = Flask(__name__)
CORS(app)


@app.route('/caption', methods=['POST'])
def upload_image():
    if not request.data:
        return jsonify({'error': 'No payload in the request'}), 400

    if "image" not in request.json:
        return jsonify({'error': 'No image in the payload'}), 400

    # Get the image file from the request
    image_file = request.json['image']

    # Open the image using PIL
    caption = get_caption_from_openai(image_file)

    response = jsonify({'caption': caption})

    return response


if __name__ == '__main__':
    app.run(debug=True)
