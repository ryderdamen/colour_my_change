"""The flask app responsible for serving the application"""
import os
from flask import Flask, render_template, request, send_file, session
from backend.helpers import build_pdf_output
from backend.node_generator import NodeGenerator


app = Flask(__name__)


MIN_INPUT_WEIGHT = 30
MAX_INPUT_WEIGHT = 500


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
    # session.clear()
    current_weight = int(request.form.get("currentWeight"))
    target_weight = int(request.form.get("targetWeight"))
    if current_weight < MIN_INPUT_WEIGHT or current_weight > MAX_INPUT_WEIGHT:
        return 'Error - Minimums'
    if target_weight < MIN_INPUT_WEIGHT or target_weight > MAX_INPUT_WEIGHT:
        return 'Error - Maximums'
    generator = NodeGenerator(current_weight, target_weight)
    node_list = generator.get_node_list()
    pdf_bytes = build_pdf_output(node_list)
    return send_file(
        pdf_bytes,
        as_attachment=True,
        attachment_filename='colour-my-change.pdf',
        mimetype='application/pdf'
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
