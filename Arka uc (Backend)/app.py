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



from kullanıcılar_Tablosu.ekleme import kullanici_ekle
from kullanıcılar_Tablosu.listeleme import kullanici_listele
from kullanıcılar_Tablosu.güncelleme import kullanici_guncelle
from kullanıcılar_Tablosu.silme import kullanici_sil



from forman_Tablosu.ekleme import forman_ekle
from forman_Tablosu.listeleme import forman_listele
from forman_Tablosu.guncelle import forman_guncelle
from forman_Tablosu.silme import forman_sil



from overtime_Tablosu.ekleme import overtime_ekle
from overtime_Tablosu.listeleme import overtime_listele
from overtime_Tablosu.guncelleme import overtime_guncelle
from overtime_Tablosu.silme import overtime_sil




from ceza_Tablosu.ekleme import ekle_ceza




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




app.add_url_rule('/kullanici_ekle', view_func=kullanici_ekle, methods=['POST'])
app.add_url_rule('/kullanici_listele', view_func=kullanici_listele, methods=['GET'])
app.add_url_rule('/kullanici_guncelle', view_func=kullanici_guncelle, methods=['PUT'])
app.add_url_rule('/kullanici_sil', view_func=kullanici_sil, methods=['DELETE'])




app.add_url_rule('/forman_ekle', view_func=forman_ekle, methods=['POST'])
app.add_url_rule('/forman_listele', view_func=forman_listele, methods=['GET'])
app.add_url_rule('/forman_guncelle', view_func=forman_guncelle, methods=['PUT'])
app.add_url_rule('/forman_sil', view_func=forman_sil, methods=['DELETE'])




app.add_url_rule('/overtime_ekle', view_func=overtime_ekle, methods=['POST'])
app.add_url_rule('/overtime_listele', view_func=overtime_listele, methods=['GET'])
app.add_url_rule('/overtime_guncelle', view_func=overtime_guncelle, methods=['PUT'])
app.add_url_rule('/overtime_sil', view_func=overtime_sil, methods=['DELETE'])





app.add_url_rule('/ceza_ekle', view_func=ekle_ceza, methods=['POST'])


@app.route('/')
def home():
    return "Hello, Eveline!"

if __name__ == '__main__':
    app.run(debug=True)
    

