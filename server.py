from flask import Flask, request, jsonify
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
    return '''
<!DOCTYPE html>
<html>
<body style="font-family:Arial;padding:20px">
<h1>🧠 CV Test</h1>
<hr>

<h3>📤 1. PDF Yükle</h3>
<form id="yukle_form">
  <input type="file" id="pdf_dosya" accept=".pdf">
  <button type="button" onclick="pdfYukle()">Yükle</button>
</form>
<div id="yukle_sonuc"></div>

<hr>

<h3>🎯 2. Esles</h3>
CV ID: <input id="esles_id" placeholder="abc123" style="width:200px;padding:5px">
<br><br>
Is ilani:<br>
<textarea id="is_ilani" rows="4" style="width:400px;padding:5px">JavaScript, HTML, CSS, Git bilen developer ariyoruz</textarea>
<br><br>
<button type="button" onclick="eslesmeYap()" style="padding:10px;background:blue;color:white;cursor:pointer">
  Esles
</button>
<div id="esles_sonuc" style="margin-top:20px;padding:20px;background:#f0f0f0"></div>

<script>
function pdfYukle() {
  var dosya = document.getElementById("pdf_dosya").files[0];
  if(!dosya) { alert("PDF sec!"); return; }
  var form = new FormData();
  form.append("file", dosya);
  fetch("/yukle", {method:"POST", body:form})
    .then(function(r) { return r.json(); })
    .then(function(data) {
      document.getElementById("yukle_sonuc").innerHTML = "✅ ID: <b>" + data.id + "</b>";
      document.getElementById("esles_id").value = data.id;
    });
}

function eslesmeYap() {
  var id = document.getElementById("esles_id").value;
  var ilan = document.getElementById("is_ilani").value;
  if(!id) { alert("CV ID gir!"); return; }
  if(!ilan) { alert("Is ilani gir!"); return; }
  
  document.getElementById("esles_sonuc").innerHTML = "⏳ Yukleniyor...";
  
  fetch("/esles", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({cv_id: id, is_ilani: ilan})
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    var s = data.sonuc;
    document.getElementById("esles_sonuc").innerHTML =
      "<h2>" + s.yorum + "</h2>" +
      "<h1 style='color:blue'>%" + s.skor + " Uyum</h1>" +
      "<p><b>✅ Eslesen:</b> " + s.eslesen_skills.join(", ") + "</p>" +
      "<p><b>❌ Eksik:</b> " + s.eksik_skills.join(", ") + "</p>";
  })
  .catch(function(e) {
    document.getElementById("esles_sonuc").innerHTML = "❌ Hata: " + e;
  });
}
</script>
</body>
</html>
'''

@app.route('/yukle', methods=['POST'])
def yukle():
    dosya = request.files['file']
    dosya_id = str(uuid.uuid4())[:8]
    dosya_adi = f"uploads/{dosya_id}_{dosya.filename}"
    dosya.save(dosya_adi)
    return jsonify({
        "id": dosya_id,
        "dosya": dosya.filename,
        "mesaj": "✅ Yuklendi!"
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
        return jsonify({"hata": "PDF bulunamadi"})
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
        return jsonify({"hata": "PDF bulunamadi"})
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
        return jsonify({"hata": "PDF bulunamadi"})
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    