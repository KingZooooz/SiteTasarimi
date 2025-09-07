from flask import Flask

from calisan_tablosu_ekle import calisan_ekle 


import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


# Register the API endpoint
app.add_url_rule('/add_employee', view_func=calisan_ekle, methods=['POST'])





@app.route('/')
def home():
    return "Hello, ATSystem!"

if __name__ == '__main__':
    app.run(debug=True)
    

