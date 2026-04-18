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

@app.route('/test')
def test():
    return '''
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CV Job Matcher</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: "Segoe UI", Arial, sans-serif;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  background-size: 400% 400%;
  animation: gradientBG 8s ease infinite;
}

@keyframes gradientBG {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.container {
  max-width: 850px;
  margin: 0 auto;
  padding: 30px 20px;
}

h1 {
  text-align: center;
  color: white;
  font-size: 2.5em;
  margin-bottom: 10px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  animation: fadeInDown 0.8s ease;
}

.subtitle {
  text-align: center;
  color: rgba(255,255,255,0.8);
  margin-bottom: 30px;
  font-size: 1.1em;
  animation: fadeInDown 1s ease;
}

@keyframes fadeInDown {
  from { opacity:0; transform:translateY(-20px); }
  to { opacity:1; transform:translateY(0); }
}

@keyframes fadeInUp {
  from { opacity:0; transform:translateY(20px); }
  to { opacity:1; transform:translateY(0); }
}

.card {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 20px;
  padding: 30px;
  margin: 20px 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  animation: fadeInUp 0.8s ease;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-3px);
}

.card h3 {
  color: white;
  font-size: 1.3em;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.upload-area {
  border: 2px dashed rgba(255,255,255,0.5);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}

.upload-area:hover {
  border-color: white;
  background: rgba(255,255,255,0.1);
}

.upload-area input {
  display: none;
}

.upload-icon { font-size: 3em; margin-bottom: 10px; }
.upload-text { font-size: 1.1em; opacity: 0.9; }

textarea {
  width: 100%;
  padding: 15px;
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 12px;
  font-size: 14px;
  resize: vertical;
  background: rgba(255,255,255,0.1);
  color: white;
  outline: none;
  transition: all 0.3s;
}

textarea::placeholder { color: rgba(255,255,255,0.6); }
textarea:focus { border-color: white; background: rgba(255,255,255,0.2); }

.btn {
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  color: #764ba2;
  border: none;
  padding: 15px 30px;
  border-radius: 12px;
  cursor: pointer;
  font-size: 1.1em;
  font-weight: bold;
  width: 100%;
  margin-top: 15px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

.btn:active { transform: translateY(0); }

.id-box {
  background: rgba(255,255,255,0.2);
  border: 1px solid rgba(255,255,255,0.4);
  border-radius: 10px;
  padding: 12px 15px;
  color: white;
  margin-top: 15px;
  font-weight: bold;
  display: flex;
  align-items: center;
  gap: 10px;
}

.score-box {
  text-align: center;
  padding: 40px;
  border-radius: 20px;
  color: white;
  margin: 20px 0;
  animation: fadeInUp 0.5s ease;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.score-emoji { font-size: 3em; margin-bottom: 10px; }

.score-number {
  font-size: 5em;
  font-weight: bold;
  line-height: 1;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.score-label {
  font-size: 1.3em;
  opacity: 0.9;
  margin-top: 10px;
}

.progress-bar {
  background: rgba(255,255,255,0.2);
  border-radius: 50px;
  height: 25px;
  margin: 15px 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  border-radius: 50px;
  background: linear-gradient(135deg, #fff, rgba(255,255,255,0.7));
  transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
  width: 0%;
}

.progress-text {
  text-align: center;
  color: rgba(255,255,255,0.9);
  font-size: 0.95em;
}

.skill-tag {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 50px;
  margin: 5px;
  font-size: 14px;
  font-weight: bold;
  animation: popIn 0.3s ease;
}

@keyframes popIn {
  from { transform: scale(0); opacity: 0; }
  to { transform: scale(1); opacity: 1; }
}

.skill-match {
  background: rgba(46, 213, 115, 0.3);
  border: 1px solid rgba(46, 213, 115, 0.6);
  color: white;
}

.skill-missing {
  background: rgba(255, 71, 87, 0.3);
  border: 1px solid rgba(255, 71, 87, 0.6);
  color: white;
}

.rapor-box {
  background: rgba(255,255,255,0.1);
  border-left: 4px solid rgba(255,255,255,0.6);
  border-radius: 0 12px 12px 0;
  padding: 15px 20px;
  margin: 10px 0;
  color: white;
}

.rapor-box a {
  color: #f0f0f0;
  text-decoration: underline;
}

.loading-spinner {
  display: inline-block;
  width: 30px;
  height: 30px;
  border: 3px solid rgba(255,255,255,0.3);
  border-top: 3px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.confetti {
  position: fixed;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  animation: confettiFall 3s ease-in forwards;
  pointer-events: none;
}

@keyframes confettiFall {
  0% { transform: translateY(-100px) rotate(0deg); opacity: 1; }
  100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
}

.stat-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
  margin: 15px 0;
}

.stat-item {
  background: rgba(255,255,255,0.1);
  border-radius: 12px;
  padding: 15px;
  text-align: center;
  color: white;
}

.stat-number { font-size: 2em; font-weight: bold; }
.stat-label { font-size: 0.85em; opacity: 0.8; margin-top: 5px; }

@media (max-width: 600px) {
  h1 { font-size: 1.8em; }
  .score-number { font-size: 3.5em; }
  .stat-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>

<div class="container">
  <h1>🧠 CV Job Matcher</h1>
  <p class="subtitle">AI destekli CV ve iş ilanı eşleştirme sistemi</p>

  <!-- CV Yükle -->
  <div class="card">
    <h3>📤 CV Yükle</h3>
    <div class="upload-area" onclick="document.getElementById('pdf_input').click()">
      <input type="file" id="pdf_input" accept=".pdf" onchange="pdfYukle()">
      <div class="upload-icon">📄</div>
      <div class="upload-text">PDF CV yüklemek için tıkla</div>
      <div style="color:rgba(255,255,255,0.6);font-size:0.85em;margin-top:5px">veya sürükle bırak</div>
    </div>
    <div id="yukle_sonuc"></div>
  </div>

  <!-- İş İlanı -->
  <div class="card">
    <h3>💼 İş İlanı Gir</h3>
    <textarea id="is_ilani" rows="6" placeholder="İş ilanını buraya yapıştır...
Örnek: Python, Docker, AWS bilen backend developer arıyoruz. 3+ yıl deneyim gereklidir."></textarea>
    <input type="hidden" id="esles_id">
    <button class="btn" onclick="eslesmeYap()">🎯 Analiz Et</button>
  </div>

  <!-- Sonuç -->
  <div id="sonuc_bolum" style="display:none">

    <!-- Skor -->
    <div class="score-box" id="score_box">
      <div class="score-emoji" id="score_emoji">🎯</div>
      <div class="score-number" id="score_number">0%</div>
      <div class="score-label" id="score_label">Analiz ediliyor...</div>
    </div>

    <!-- Progress -->
    <div class="card">
      <h3>📊 Uyum Oranı</h3>
      <div class="progress-bar">
        <div class="progress-fill" id="progress_fill"></div>
      </div>
      <div class="progress-text" id="progress_text"></div>

      <!-- Stats -->
      <div class="stat-grid" id="stat_grid"></div>
    </div>

    <!-- Eşleşen -->
    <div class="card">
      <h3>✅ Eşleşen Skill\'ler</h3>
      <div id="eslesen_div"></div>
    </div>

    <!-- Eksik -->
    <div class="card">
      <h3>❌ Eksik Skill\'ler</h3>
      <div id="eksik_div"></div>
    </div>

    <!-- Rapor -->
    <div class="card">
      <h3>📋 Detaylı Rapor</h3>
      <div id="rapor_div"></div>
    </div>

  </div>
</div>

<script>
var cv_id = "";

function pdfYukle() {
  var dosya = document.getElementById("pdf_input").files[0];
  if(!dosya) return;

  document.getElementById("yukle_sonuc").innerHTML = 
    "<div style=text-align:center;padding:20px;color:white><div class=loading-spinner></div><p style=margin-top:10px>Yükleniyor...</p></div>";

  var form = new FormData();
  form.append("file", dosya);

  fetch("/yukle", {method:"POST", body:form})
    .then(function(r) { return r.json(); })
    .then(function(data) {
      cv_id = data.id;
      document.getElementById("esles_id").value = data.id;
      document.getElementById("yukle_sonuc").innerHTML =
        "<div class=id-box>✅ " + dosya.name + " yüklendi! ID: " + data.id + "</div>";
    })
    .catch(function(e) {
      document.getElementById("yukle_sonuc").innerHTML = 
        "<div class=id-box style=background:rgba(255,71,87,0.3)>❌ Hata: " + e + "</div>";
    });
}

function eslesmeYap() {
  var id = document.getElementById("esles_id").value;
  var ilan = document.getElementById("is_ilani").value;

  if(!id) { alert("Önce CV yükle!"); return; }
  if(!ilan) { alert("İş ilanı gir!"); return; }

  document.getElementById("sonuc_bolum").style.display = "block";
  document.getElementById("score_number").innerHTML = "<div class=loading-spinner></div>";
  document.getElementById("score_label").innerHTML = "Analiz ediliyor...";

  fetch("/esles", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({cv_id: id, is_ilani: ilan})
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    var s = data.sonuc;
    var skor = s.skor;

    // Renk ve emoji
    var renk, emoji;
    if(skor >= 80) { renk = "linear-gradient(135deg,#2ecc71,#27ae60)";
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
