from flask import Flask, request, jsonify, send_file
import os
import uuid
import PyPDF2
import pdfplumber
import glob
from skill_bulucu import skill_bul
from eslestirici import esles

app = Flask(__name__)
os.makedirs("uploads", exist_ok=True)

@app.route('/')
def ana():
    return jsonify({"message": "✅ Çalışıyor!"})

@app.route('/test')
def test():
    return send_file('C:/Users/Eylül/Desktop/CVAPI/test.html')

@app.route('/yukle', methods=['POST'])
def yukle():
    dosya = request.files['file']
    dosya_id = str(uuid.uuid4())[:8]
    dosya_adi = f"uploads/{dosya_id}_{dosya.filename}"
    dosya.save(dosya_adi)
    return jsonify({
        "id": dosya_id,
        "dosya": dosya.filename,
        "mesaj": "✅ Yüklendi!"
    })

def pdf_oku(yol):
    metin = ""
    try:
        with open(yol, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for sayfa in pdf.pages:
                metin += sayfa.extract_text() + "\n"
    except:
        pass
    try:
        with pdfplumber.open(yol) as pdf:
            for sayfa in pdf.pages:
                metin += sayfa.extract_text() + "\n"
    except:
        pass
    return metin.strip()

@app.route('/metin/<cv_id>')
def metin_getir(cv_id):
    pdfler = glob.glob(f"uploads/{cv_id}*.pdf")
    if not pdfler:
        return jsonify({"hata": "PDF bulunamadı"})
    metin = pdf_oku(pdfler[0])
    return jsonify({
        "cv_id": cv_id,
        "uzunluk": len(metin),
        "kelime": len(metin.split()),
        "metin": metin[:1000]
    })

@app.route('/skills/<cv_id>')
def skill_getir(cv_id):
    pdfler = glob.glob(f"uploads/{cv_id}*.pdf")
    if not pdfler:
        return jsonify({"hata": "PDF bulunamadı"})
    metin = pdf_oku(pdfler[0])
    skills = skill_bul(metin)
    return jsonify({
        "cv_id": cv_id,
        "skills": skills["bulunan_skills"],
        "toplam": skills["toplam"]
    })

@app.route('/esles', methods=['POST'])
def eslesme():
    veri = request.json
    cv_id = veri.get('cv_id')
    is_ilani = veri.get('is_ilani')
    pdfler = glob.glob(f"uploads/{cv_id}*.pdf")
    if not pdfler:
        return jsonify({"hata": "PDF bulunamadı"})
    metin = pdf_oku(pdfler[0])
    cv_skills = skill_bul(metin)["bulunan_skills"]
    is_skills = skill_bul(is_ilani)["bulunan_skills"]
    sonuc = esles(cv_skills, is_skills)
    return jsonify({
        "cv_id": cv_id,
        "cv_skills": cv_skills,
        "is_skills": is_skills,
        "sonuc": sonuc
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    