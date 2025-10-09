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




from müdür_Tablosu.ekleme import mudur_ekle
from müdür_Tablosu.listeleme import listele_mudur
from müdür_Tablosu.güncelle import guncelle_mudur
from müdür_Tablosu.silme import sil_mudur




from müdür_Değerlendirme.ekleme import mudur_degerlendirme_ekle
from müdür_Değerlendirme.listele import mudur_degerlendirme_listele
from müdür_Değerlendirme.güncelleme import mudur_degerlendirme_guncelle
from müdür_Değerlendirme.silme import mudur_degerlendirme_sil




from Login_tablosu.ekleme import login_ekle
from Login_tablosu.güncelleme import update_login



from Loans.add import add_loan
from Loans.update import update_loan
from Loans.get import get_loans
from Loans.delete import delete_loan
from Loans.payloan import pay_loan


from Evaluation.add import add_evaluation
from Evaluation.update import update_evaluation
from Evaluation.get import get_all_evaluations
from Evaluation.get_id import get_evaluation_by_employee
from Evaluation.delete import delete_evaluation




from Jobs.add import add_job
from Jobs.get import get_all_jobs
from Jobs.update import update_job
from Jobs.delete import delete_job


from Absence.add import add_absence
from Absence.delete import delete_absence




from Rewards_And_Penalties.add import add_reward_penalty
from Rewards_And_Penalties.update import update_reward_penalty
from Rewards_And_Penalties.get import get_rewards_penalties
from Rewards_And_Penalties.delete import delete_reward_penalty





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





app.add_url_rule('/add_login', view_func=login_ekle, methods=['POST'])
app.add_url_rule('/update_login', view_func=update_login, methods=['PUT'])




app.add_url_rule('/mudur_ekle', view_func=mudur_ekle, methods=['POST'])
app.add_url_rule('/mudur_listele', view_func=listele_mudur, methods=['GET'])
app.add_url_rule('/mudur_guncelle', view_func=guncelle_mudur, methods=['PUT'])
app.add_url_rule('/mudur_sil', view_func=sil_mudur, methods=['DELETE'])




app.add_url_rule('/mudur_degerlendirme_ekle', view_func=mudur_degerlendirme_ekle, methods=['POST'])
app.add_url_rule('/mudur_degerlendirme_listele', view_func=mudur_degerlendirme_listele, methods=['GET'])
app.add_url_rule('/mudur_degerlendirme_guncelle', view_func=mudur_degerlendirme_guncelle, methods=['PUT'])
app.add_url_rule('/mudur_degerlendirme_sil', view_func=mudur_degerlendirme_sil, methods=['DELETE'])





app.add_url_rule('/api/add_loan', view_func=add_loan, methods=['POST'])
app.add_url_rule('/api/update_loan', view_func=update_loan, methods=['PUT'])
app.add_url_rule('/api/get_loans', view_func=get_loans, methods=['GET'])
app.add_url_rule('/api/loans/delete/<int:loan_id>', view_func=delete_loan, methods=['DELETE'])
app.add_url_rule('/api/loans/pay', view_func=pay_loan, methods=['POST'])




app.add_url_rule('/api/evaluation/add', view_func=add_evaluation, methods=['POST'])
app.add_url_rule('/api/evaluation/update', view_func=update_evaluation, methods=['PUT'])
app.add_url_rule('/api/evaluation', view_func=get_all_evaluations, methods=['GET'])
app.add_url_rule('/api/evaluation/<int:employee_id>', view_func=get_evaluation_by_employee, methods=['GET'])
app.add_url_rule('/api/evaluation/delete/<int:evaluation_id>', view_func=delete_evaluation, methods=['DELETE'])





app.add_url_rule('/api/absence/add', view_func=add_absence, methods=['POST'])
app.add_url_rule('/api/absence/delete/<int:log_id>', view_func=delete_absence, methods=['DELETE'])



app.add_url_rule('/api/jobs/add', view_func=add_job, methods=['POST'])
app.add_url_rule('/api/jobs', view_func=get_all_jobs, methods=['GET']) 
app.add_url_rule('/api/jobs/update', view_func=update_job, methods=['PUT'])
app.add_url_rule('/api/jobs/delete/<int:job_id>', view_func=delete_job, methods=['DELETE'])





app.add_url_rule('/api/rewards_penalties/add', view_func=add_reward_penalty, methods=['POST'])
app.add_url_rule('/api/rewards_penalties/update', view_func=update_reward_penalty, methods=['PUT'])
app.add_url_rule('/api/rewards_penalties', view_func=get_rewards_penalties, methods=['GET'])
app.add_url_rule('/api/rewards_penalties/delete/<int:entry_id>', view_func=delete_reward_penalty, methods=['DELETE'])




@app.route('/')
def home():
    return "Hello, Eveline!"

if __name__ == '__main__':
    app.run(debug=True)
    

