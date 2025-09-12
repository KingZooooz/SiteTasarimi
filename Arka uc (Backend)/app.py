from flask import Flask

from Çalışan_Tablosu.ekleme import calisan_ekle
from Çalışan_Tablosu.alma import calisanlari_listele
from Çalışan_Tablosu.guncelleme import calisan_guncelle
from Çalışan_Tablosu.silme import calisan_sil



from Site_Tablosu.ekleme import site_ekle
from Site_Tablosu.alma import site_listele
from Site_Tablosu.guncelleme import site_guncelle
from Site_Tablosu.silme import site_sil




from Workslog_Tablosu.ekleme import add_all_worklogs
from Workslog_Tablosu.ekleme import add_all_worklogs
from Workslog_Tablosu.guncelleme import workslog_guncelle
from Workslog_Tablosu.silme import workslog_sil
from flask_cors import CORS







app = Flask(__name__)
CORS(app, supports_credentials=True)


# Register the API endpoint
app.add_url_rule('/calisan_ekle', view_func=calisan_ekle, methods=['POST'])
app.add_url_rule('/calisan_listele', view_func=calisanlari_listele, methods=['GET'])
app.add_url_rule('/calisan_guncelle', view_func= calisan_guncelle, methods=['PUT'])
app.add_url_rule('/calisan_sil', view_func= calisan_sil, methods=['DELETE'])




app.add_url_rule('/site_ekle', view_func=site_ekle, methods=['POST'])
app.add_url_rule('/site_listele', view_func=site_listele, methods=['GET'])
app.add_url_rule('/site_guncelle', view_func=site_guncelle, methods=['PUT'])
app.add_url_rule('/site_sil', view_func=site_sil, methods=['DELETE'])




app.add_url_rule('/add_all_workslog', view_func=add_all_worklogs, methods=['POST'])
app.add_url_rule('/workslog', view_func=add_all_worklogs, methods=['GET'])
app.add_url_rule('/workslog_guncelle', view_func=workslog_guncelle, methods=['PUT'])
app.add_url_rule('/workslog_sil', view_func=workslog_sil, methods=['DELETE'])




@app.route('/')
def home():
    return "Hello, Eveline!"

if __name__ == '__main__':
    app.run(debug=True)
    

