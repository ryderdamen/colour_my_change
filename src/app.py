"""The flask app responsible for serving the application"""
import os
from flask import Flask, render_template, request, send_from_directory
from backend.helpers import save_multipage_output
from backend.node_generator import NodeGenerator


app = Flask(__name__)


MIN_INPUT_WEIGHT = 80
MAX_INPUT_WEIGHT = 400


@app.route('/')
def index():
    """View for the index page of the site"""
    return render_template(
        "index.html",
        MIN_INPUT_WEIGHT=MIN_INPUT_WEIGHT,
        MAX_INPUT_WEIGHT=MAX_INPUT_WEIGHT
    )


@app.route('/chart/', methods=['POST'])
def render_chart():
    """Renders the chart and downloads it to the user"""
    current_weight = int(request.form.get("currentWeight"))
    target_weight = int(request.form.get("targetWeight"))
    if current_weight < MIN_INPUT_WEIGHT or current_weight > MAX_INPUT_WEIGHT:
        return 'Error - Minimums'
    if target_weight < MIN_INPUT_WEIGHT or target_weight > MAX_INPUT_WEIGHT:
        return 'Error - Maximums'
    generator = NodeGenerator(current_weight, target_weight)
    node_list = generator.get_node_list()
    save_multipage_output(node_list, './testing.pdf')
    return send_from_directory(os.path.dirname(__file__), './testing.pdf')

    @after_this_request
    def cleanup(response):
        os.remove(os.path.join(os.path.dirname(__file__), 'testing.pdf'))
        return response


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
