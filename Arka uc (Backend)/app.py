from flask import Flask

from Çalışan_Tablosu.ekleme import calisan_ekle
from Çalışan_Tablosu.alma import calisanlari_listele

import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True)


# Register the API endpoint
app.add_url_rule('/calışan_ekle', view_func=calisan_ekle, methods=['POST'])
app.add_url_rule('/calışan_listele', view_func=calisanlari_listele, methods=['GET'])





@app.route('/')
def home():
    return "Hello, Eveline!"

if __name__ == '__main__':
    app.run(debug=True)
    

