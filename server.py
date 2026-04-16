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
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CV Job Matcher</title>
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:Arial; background:#f5f7fa; color:#333; }
.container { max-width:800px; margin:0 auto; padding:20px; }
h1 { text-align:center; color:#2c3e50; padding:30px 0; font-size:2em; }
.card { background:white; border-radius:15px; padding:25px; margin:20px 0; box-shadow:0 2px 10px rgba(0,0,0,0.1); }
.card h3 { color:#2c3e50; margin-bottom:15px; font-size:1.2em; }
input[type=file] { padding:10px; border:2px dashed #3498db; border-radius:8px; width:100%; cursor:pointer; }
textarea { width:100%; padding:12px; border:2px solid #e0e0e0; border-radius:8px; font-size:14px; resize:vertical; }
.btn { background:linear-gradient(135deg,#3498db,#2980b9); color:white; border:none; padding:12px 30px; border-radius:8px; cursor:pointer; font-size:16px; width:100%; margin-top:10px; }
.btn:hover { opacity:0.9; }
.score-box { text-align:center; padding:30px; background:linear-gradient(135deg,#667eea,#764ba2); border-radius:15px; color:white; margin:20px 0; }
.score-number { font-size:4em; font-weight:bold; }
.score-label { font-size:1.2em; opacity:0.9; }
.skill-tag { display:inline-block; padding:6px 12px; border-radius:20px; margin:4px; font-size:14px; }
.skill-match { background:#2ecc71; color:white; }
.skill-missing { background:#e74c3c; color:white; }
.category-box { background:#f8f9fa; border-left:4px solid #3498db; padding:15px; margin:10px 0; border-radius:0 8px 8px 0; }
.progress-bar { background:#e0e0e0; border-radius:10px; height:20px; margin:10px 0; overflow:hidden; }
.progress-fill { height:100%; border-radius:10px; background:linear-gradient(135deg,#3498db,#2980b9); transition:width 1s; }
.id-box { background:#e8f4fd; padding:10px; border-radius:8px; margin:10px 0; font-weight:bold; color:#2980b9; }
</style>
</head>
<body>
<div class="container">
<h1>🧠 CV Job Matcher</h1>

<div class="card">
<h3>📤 1. CV Yukle</h3>
<input type="file" id="pdf_dosya" accept=".pdf">
<button class="btn" onclick="pdfYukle()">📤 CV Yukle</button>
<div id="yukle_sonuc"></div>
</div>

<div class="card">
<h3>💼 2. Is Ilani Gir</h3>
<textarea id="is_ilani" rows="5" placeholder="Is ilanini buraya yapistir..."></textarea>
<button class="btn" onclick="eslesmeYap()">🎯 Analiz Et</button>
<input type="hidden" id="esles_id">
</div>

<div id="sonuc_bolum" style="display:none">

<div class="score-box">
<div id="sonuc_emoji" style="font-size:2em">🎯</div>
<div class="score-number" id="skor_sayi">0%</div>
<div class="score-label" id="skor_yorum">Analiz ediliyor...</div>
</div>

<div class="card">
<h3>📊 Uyum Orani</h3>
<div class="progress-bar">
<div class="progress-fill" id="progress" style="width:0%"></div>
</div>
<p id="progress_text" style="text-align:center;color:#666;margin-top:5px"></p>
</div>

<div class="card">
<h3>✅ Eslesen Skilllar</h3>
<div id="eslesen_skills"></div>
</div>

<div class="card">
<h3>❌ Eksik Skilllar</h3>
<div id="eksik_skills"></div>
<div id="eksik_oneri" style="margin-top:15px"></div>
</div>

<div class="card">
<h3>📋 Detayli Rapor</h3>
<div id="detayli_rapor"></div>
</div>

</div>
</div>

<script>
var cv_id = "";

function pdfYukle() {
  var dosya = document.getElementById("pdf_dosya").files[0];
  if(!dosya) { alert("PDF sec!"); return; }
  document.getElementById("yukle_sonuc").innerHTML = "<p>⏳ Yukleniyor...</p>";
  var form = new FormData();
  form.append("file", dosya);
  fetch("/yukle", {method:"POST", body:form})
    .then(function(r) { return r.json(); })
    .then(function(data) {
      cv_id = data.id;
      document.getElementById("esles_id").value = data.id;
      document.getElementById("yukle_sonuc").innerHTML = 
        "<div class=id-box>✅ CV Yuklendi! ID: " + data.id + "</div>";
    })
    .catch(function(e) {
      document.getElementById("yukle_sonuc").innerHTML = "❌ Hata: " + e;
    });
}

function eslesmeYap() {
  var id = document.getElementById("esles_id").value;
  var ilan = document.getElementById("is_ilani").value;
  if(!id) { alert("Once CV yukle!"); return; }
  if(!ilan) { alert("Is ilani gir!"); return; }
  document.getElementById("sonuc_bolum").style.display = "block";
  document.getElementById("skor_sayi").innerHTML = "⏳";
  document.getElementById("skor_yorum").innerHTML = "Analiz ediliyor...";
  fetch("/esles", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({cv_id: id, is_ilani: ilan})
  })
  .then(function(r) { return r.json(); })
  .then(function(data) {
    var s = data.sonuc;
    var skor = s.skor;
    var renk = skor >= 80 ? "#2ecc71" : skor >= 60 ? "#f39c12" : skor >= 40 ? "#e67e22" : "#e74c3c";
    var emoji = skor >= 80 ? "🌟" : skor >= 60 ? "👍" : skor >= 40 ? "🤔" : "😟";
    document.getElementById("sonuc_emoji").innerHTML = emoji;
    document.getElementById("skor_sayi").innerHTML = "%" + skor;
    document.getElementById("skor_yorum").innerHTML = s.yorum;
    document.querySelector(".score-box").style.background = "linear-gradient(135deg," + renk + "," + renk + "99)";
    document.getElementById("progress").style.width = skor + "%";
    document.getElementById("progress_text").innerHTML = 
      s.eslesen_skills.length + " / " + (s.eslesen_skills.length + s.eksik_skills.length) + " skill eslesti";
    var eslesen = "";
    s.eslesen_skills.forEach(function(skill) {
      eslesen += "<span class='skill-tag skill-match'>✅ " + skill + "</span>";
    });
    document.getElementById("eslesen_skills").innerHTML = eslesen || "<p style='color:#999'>Eslesen skill bulunamadi</p>";
    var eksik = "";
    s.eksik_skills.forEach(function(skill) {
      eksik += "<span class='skill-tag skill-missing'>❌ " + skill + "</span>";
    });
    document.getElementById("eksik_skills").innerHTML = eksik || "<p style='color:#2ecc71'>🎉 Tum skilllar eslesti!</p>";
    var oneri = "";
    if(s.eksik_skills.length > 0) {
      oneri = "<div class='category-box'><b>💡 Oneriler:</b><ul style='margin-top:10px;padding-left:20px'>";
      s.eksik_skills.forEach(function(skill) {
        oneri += "<li>" + skill + " icin: <a href='https://www.google.com/search?q=" + skill + "+tutorial' target='_blank'>Google ara</a></li>";
      });
      oneri += "</ul></div>";
    }
    document.getElementById("eksik_oneri").innerHTML = oneri;
    var rapor = "";
    rapor += "<div class='category-box'><b>📊 CV Analizi:</b><br>";
    rapor += "CV Skill: <b>" + data.cv_skills.length + "</b><br>";
    rapor += "Is Ilani Skill: <b>" + data.is_skills.length + "</b><br>";
    rapor += "Eslesen: <b>" + s.eslesen_skills.length + "</b><br>";
    rapor += "Eksik: <b>" + s.eksik_skills.length + "</b></div>";
    rapor += "<div class='category-box'><b>🎯 Sonuc:</b><br>";
    if(skor >= 80) {
      rapor += "✅ Bu pozisyon icin cok iyi bir adaysin! Hemen basvur!";
    } else if(skor >= 60) {
      rapor += "👍 Iyi bir aday profilin var. Eksik skilleri ogrenirsen daha guclu olursun.";
    } else if(skor >= 40) {
      rapor += "🤔 Orta duzey uyum var. Eksik skillere odaklan.";
    } else {
      rapor += "📚 Bu pozisyon icin daha fazla hazirlik gerekiyor.";
    }
    rapor += "</div>";
    document.getElementById("detayli_rapor").innerHTML = rapor;
    document.getElementById("sonuc_bolum").scrollIntoView({behavior:"smooth"});
  })
  .catch(function(e) {
    alert("Hata: " + e);
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
    