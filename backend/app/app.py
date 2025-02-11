from flask import Flask
from .routes.routes import main

app = Flask(__name__, template_folder='../../frontend/templates')
app.register_blueprint(main)

if __name__ == '__main__':
    app.run(debug=True) 