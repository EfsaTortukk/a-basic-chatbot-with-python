from flask import Flask, render_template, request, jsonify
import pandas as pd
from difflib import SequenceMatcher
from datetime import datetime, timedelta


app = Flask(__name__)

excel_dosya_adi = "dataset.xlsx"
dataset = pd.read_excel(excel_dosya_adi)

def benzerlik_orani(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

def cevap_bul(soru):
    max_benzerlik = 0
    en_uygun_cevap = "Üzgünüm, sorunuza uygun bir cevap bulamadım."

    if 'saat' in soru.lower():
        su_an_ki_saat = datetime.now().strftime("%H:%M")
        return f"Şu anki saat: {su_an_ki_saat}"
    
    elif 'tarih' in soru.lower():
        su_anki_tarih = datetime.now().strftime("%d %B %Y")
        return f"Bugün tarih itibariyle {su_anki_tarih}."
    
    elif 'yarın' in soru.lower():
        yarin_tarih = (datetime.now() + timedelta(days=1)).strftime("%d %B %Y")
        return f"Yarın tarih itibariyle {yarin_tarih}."

    elif 'dün' in soru.lower():
        dun_tarih = (datetime.now() - timedelta(days=1)).strftime("%d %B %Y")
        return f"Dün tarih itibariyle {dun_tarih}."
    
    for index, row in dataset.iterrows():
        benzerlik = benzerlik_orani(soru.lower(), row['sorular'].lower())
        if benzerlik > max_benzerlik:
            max_benzerlik = benzerlik
            en_uygun_cevap = row['cevaplar']

    return en_uygun_cevap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['userInput']
    bot_response = cevap_bul(user_input)

    return jsonify({"user_input": user_input, "bot_response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
