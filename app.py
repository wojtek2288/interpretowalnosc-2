from flask import Flask, render_template, request, jsonify
import openai
import base64
import cv2
import numpy as np

app = Flask(__name__)

def detect_edges(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image, 100, 200)
    return edges

def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image_file = request.files['image']
        mode = request.form['mode']
        if image_file:
            image_bytes = image_file.read()

            np_img = np.frombuffer(image_bytes, np.uint8)
            image = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

            edges = detect_edges(image)
            cv2.imwrite('edges.jpg', edges)

            faces_image = detect_faces(image)
            cv2.imwrite('faces.jpg', faces_image)

            description = generate_image_caption(image_bytes, mode)

            return jsonify(description=description)
    return render_template('index.html')

def generate_image_caption(image_bytes, mode):
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    openai.api_key = 'INSERT API KEY'

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
