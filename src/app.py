"""The flask app responsible for serving the application"""
from flask import Flask
from roadmap_generator import generate_roadmap
from image_generator import generate_image


app = Flask(__name__)


@app.route('/')
def main():
    return generate_image()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
