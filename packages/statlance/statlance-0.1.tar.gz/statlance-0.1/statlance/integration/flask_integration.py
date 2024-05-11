
# statlance/integration/flask_integration.py
from flask import Flask, render_template_string
from statlance.core.dashboarding import main as flask_main

app = Flask(__name__)

@app.route('/')
def index():
    # Render the main content of the Flask app
    content = flask_main()
    return render_template_string(content)

if __name__ == '__main__':
    app.run(debug=True)
