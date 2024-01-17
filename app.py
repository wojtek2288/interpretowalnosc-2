from flask import Flask, render_template, request, jsonify
import openai
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        mode = request.form['mode']
        if image_file:
            image_bytes = image_file.read()
            description = generate_image_caption(image_bytes, mode)
            return jsonify(description=description)
    return render_template('index.html')

def generate_image_caption(image_bytes, mode):
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    openai.api_key = ''
    
    query = "Opisz krótko dostarczony obraz po polsku." if mode == "description" else "Opisz w jednym zdaniu dostarczony obraz po polsku."
    print(query)
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encoded_image}",
                        },
                    },
                ],
            },
        ],
        max_tokens=400,
    )

    return response.choices[0].message.content

if __name__ == '__main__':
    app.run(debug=True)
