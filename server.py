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
    return jsonify({"mesaj": "CV Job Matcher çalışıyor!"})

@app.route('/upload', methods=['POST'])
def upload():
    try:
        dosya = request.files['file']
        dosya_id = str(uuid.uuid4())[:8]
        os.makedirs("uploads", exist_ok=True)
        dosya_adi = f"uploads/{dosya_id}_{dosya.filename}"
        dosya.save(dosya_adi)
        return jsonify({"id": dosya_id, "dosya": dosya.filename})
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

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

@app.route('/match', methods=['POST'])
def match():
    try:
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
    except Exception as e:
        return jsonify({"hata": str(e)}), 500

@app.route('/test')
def test():
    return """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CV İş Eşleştirici</title>
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
.container { max-width:850px; margin:0 auto; padding:30px 20px; }
h1 { text-align:center; color:white; font-size:2.5em; margin-bottom:10px; text-shadow:0 2px 10px rgba(0,0,0,0.3); }
.altyazi { text-align:center; color:rgba(255,255,255,0.8); margin-bottom:30px; font-size:1.1em; }
.kart {
  background: rgba(255,255,255,0.15);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255,255,255,0.3);
  border-radius: 20px;
  padding: 30px;
  margin: 20px 0;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
  transition: transform 0.3s ease;
}
.kart:hover { transform: translateY(-3px); }
.kart h3 { color:white; font-size:1.3em; margin-bottom:20px; }
.yukle-alani {
  border: 2px dashed rgba(255,255,255,0.5);
  border-radius: 15px;
  padding: 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
}
.yukle-alani:hover { border-color:white; background:rgba(255,255,255,0.1); }
.yukle-ikonu { font-size:3em; margin-bottom:10px; }
.yukle-yazisi { font-size:1.1em; opacity:0.9; }
textarea {
  width:100%; padding:15px;
  border:1px solid rgba(255,255,255,0.3);
  border-radius:12px; font-size:14px;
  resize:vertical;
  background:rgba(255,255,255,0.1);
  color:white; outline:none;
}
textarea::placeholder { color:rgba(255,255,255,0.6); }
textarea:focus { border-color:white; background:rgba(255,255,255,0.2); }
.buton {
  background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
  color: #764ba2; border:none;
  padding:15px 30px; border-radius:12px;
  cursor:pointer; font-size:1.1em;
  font-weight:bold; width:100%;
  margin-top:15px; transition:all 0.3s ease;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}
.buton:hover { transform:translateY(-2px); box-shadow:0 6px 20px rgba(0,0,0,0.3); }
.id-kutusu {
  background:rgba(255,255,255,0.2);
  border:1px solid rgba(255,255,255,0.4);
  border-radius:10px; padding:12px 15px;
  color:white; margin-top:15px; font-weight:bold;
}
.skor-kutusu {
  text-align:center; padding:40px;
  border-radius:20px; color:white;
  margin:20px 0;
  box-shadow:0 8px 32px rgba(0,0,0,0.3);
  transition: background 1s ease;
}
.skor-emoji { font-size:3em; margin-bottom:10px; }
.skor-sayi { font-size:5em; font-weight:bold; line-height:1; }
.skor-yorum { font-size:1.3em; opacity:0.9; margin-top:10px; }
.ilerleme-cubugu {
  background:rgba(255,255,255,0.2);
  border-radius:50px; height:25px;
  margin:15px 0; overflow:hidden;
}
.ilerleme-dolgu {
  height:100%; border-radius:50px;
  background:linear-gradient(135deg,#fff,rgba(255,255,255,0.7));
  transition:width 1.5s ease; width:0%;
}
.ilerleme-yazi { text-align:center; color:rgba(255,255,255,0.9); font-size:0.95em; margin-top:5px; }
.yetenek-etiketi {
  display:inline-block; padding:8px 16px;
  border-radius:50px; margin:5px;
  font-size:14px; font-weight:bold;
}
.eslesen { background:rgba(46,213,115,0.3); border:1px solid rgba(46,213,115,0.6); color:white; }
.eksik { background:rgba(255,71,87,0.3); border:1px solid rgba(255,71,87,0.6); color:white; }
.rapor-kutusu {
  background:rgba(255,255,255,0.1);
  border-left:4px solid rgba(255,255,255,0.6);
  border-radius:0 12px 12px 0;
  padding:15px 20px; margin:10px 0; color:white;
}
.rapor-kutusu a { color:#f0f0f0; text-decoration:underline; }
.yukleniyor {
  display:inline-block; width:30px; height:30px;
  border:3px solid rgba(255,255,255,0.3);
  border-top:3px solid white;
  border-radius:50%;
  animation:don 1s linear infinite;
}
@keyframes don { to { transform:rotate(360deg); } }
.istatistik-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:15px; margin:15px 0; }
.istatistik-kutu { background:rgba(255,255,255,0.1); border-radius:12px; padding:15px; text-align:center; color:white; }
.istatistik-sayi { font-size:2em; font-weight:bold; }
.istatistik-etiket { font-size:0.85em; opacity:0.8; margin-top:5px; }
</style>
</head>
<body>
<div class="container">
  <h1>🧠 CV İş Eşleştirici</h1>
  <p class="altyazi">Yapay zeka destekli CV ve iş ilanı eşleştirme sistemi</p>

  <div class="kart">
    <h3>📤 CV Yükle</h3>
    <div class="yukle-alani" onclick="document.getElementById('pdf_girdi').click()">
      <input type="file" id="pdf_girdi" accept=".pdf" onchange="cvYukle()" style="display:none">
      <div class="yukle-ikonu">📄</div>
      <div class="yukle-yazisi">PDF CV yüklemek için tıklayın</div>
      <div style="color:rgba(255,255,255,0.6);font-size:0.85em;margin-top:5px">veya sürükleyip bırakın</div>
    </div>
    <div id="yukle_sonucu"></div>
  </div>

  <div class="kart">
    <h3>💼 İş İlanı Girin</h3>
    <textarea id="is_ilani" rows="6" placeholder="İş ilanını buraya yapıştırın...
Örnek: Python, Docker, AWS bilen backend geliştirici arıyoruz. 3+ yıl deneyim gereklidir."></textarea>
    <input type="hidden" id="cv_kimlik">
    <button class="buton" onclick="eslesmeYap()">🎯 Analiz Et</button>
  </div>

  <div id="sonuc_bolumu" style="display:none">
    <div class="skor-kutusu" id="skor_kutusu">
      <div class="skor-emoji" id="skor_emoji">🎯</div>
      <div class="skor-sayi" id="skor_sayisi">0%</div>
      <div class="skor-yorum" id="skor_yorumu">Analiz ediliyor...</div>
    </div>

    <div class="kart">
      <h3>📊 Uyum Oranı</h3>
      <div class="ilerleme-cubugu">
        <div class="ilerleme-dolgu" id="ilerleme_dolgu"></div>
      </div>
      <div class="ilerleme-yazi" id="ilerleme_yazisi"></div>
      <div class="istatistik-grid" id="istatistik_grid"></div>
    </div>

    <div class="kart">
      <h3>✅ Eşleşen Yetenekler</h3>
      <div id="eslesen_div"></div>
    </div>

    <div class="kart">
      <h3>❌ Eksik Yetenekler</h3>
      <div id="eksik_div"></div>
      <div id="oneri_div"></div>
    </div>

    <div class="kart">
      <h3>📋 Detaylı Rapor</h3>
      <div id="rapor_div"></div>
    </div>
  </div>
</div>

<script>
var cv_kimlik = "";

function cvYukle() {
  var dosya = document.getElementById("pdf_girdi").files[0];
  if(!dosya) return;
  document.getElementById("yukle_sonucu").innerHTML = 
    "<div style='text-align:center;padding:20px;color:white'><div class='yukleniyor'></div><p style='margin-top:10px'>Yükleniyor...</p></div>";
  var form = new FormData();
  form.append("file", dosya);
  fetch("/upload", {method:"POST", body:form})
    .then(function(r) { return r.json(); })
    .then(function(veri) {
      cv_kimlik = veri.id;
      document.getElementById("cv_kimlik").value = veri.id;
      document.getElementById("yukle_sonucu").innerHTML =
        "<div class='id-kutusu'>✅ " + dosya.name + " yüklendi! Kimlik: " + veri.id + "</div>";
    })
    .catch(function(hata) {
      document.getElementById("yukle_sonucu").innerHTML = 
        "<div class='id-kutusu' style='background:rgba(255,71,87,0.3)'>❌ Hata: " + hata + "</div>";
    });
}

function eslesmeYap() {
  var kimlik = document.getElementById("cv_kimlik").value;
  var ilan = document.getElementById("is_ilani").value;
  if(!kimlik) { alert("Önce CV yükleyin!"); return; }
  if(!ilan) { alert("İş ilanı girin!"); return; }
  document.getElementById("sonuc_bolumu").style.display = "block";
  document.getElementById("skor_sayisi").innerHTML = "<div class='yukleniyor'></div>";
  document.getElementById("skor_yorumu").innerHTML = "Analiz ediliyor...";
  fetch("/match", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({cv_id: kimlik, is_ilani: ilan})
  })
  .then(function(r) { return r.json(); })
  .then(function(veri) {
    var s = veri.sonuc;
    var skor = s.skor;
    var renk, emoji;
    if(skor >= 80) { renk = "linear-gradient(135deg
        if(skor >= 80) { renk = "linear-gradient(135deg,#2ecc71,#27ae60)"; emoji = "🌟"; }
    else if(skor >= 60) { renk = "linear-gradient(135deg,#f39c12,#e67e22)"; emoji = "👍"; }
    else if(skor >= 40) { renk = "linear-gradient(135deg,#e67e22,#d35400)"; emoji = "🤔"; }
    else { renk = "linear-gradient(135deg,#e74c3c,#c0392b)"; emoji = "😟"; }

    document.getElementById("skor_emoji").innerHTML = emoji;
    document.getElementById("skor_sayisi").innerHTML = "%" + skor;
    document.getElementById("skor_yorumu").innerHTML = s.yorum;
    document.getElementById("skor_kutusu").style.background = renk;
    document.getElementById("ilerleme_dolgu").style.width = skor + "%";
    document.getElementById("ilerleme_yazisi").innerHTML = 
      s.eslesen_skills.length + " / " + (s.eslesen_skills.length + s.eksik_skills.length) + " yetenek eşleşti";

    document.getElementById("istatistik_grid").innerHTML =
      "<div class='istatistik-kutu'><div class='istatistik-sayi'>" + veri.cv_skills.length + "</div><div class='istatistik-etiket'>CV Yeteneği</div></div>" +
      "<div class='istatistik-kutu'><div class='istatistik-sayi'>" + veri.is_skills.length + "</div><div class='istatistik-etiket'>İş İlanı Yeteneği</div></div>" +
      "<div class='istatistik-kutu'><div class='istatistik-sayi'>" + s.eslesen_skills.length + "</div><div class='istatistik-etiket'>Eşleşen</div></div>" +
      "<div class='istatistik-kutu'><div class='istatistik-sayi'>" + s.eksik_skills.length + "</div><div class='istatistik-etiket'>Eksik</div></div>";

    var eslesen = "";
    s.eslesen_skills.forEach(function(yetenek) {
      eslesen += "<span class='yetenek-etiketi eslesen'>✅ " + yetenek + "</span>";
    });
    document.getElementById("eslesen_div").innerHTML = eslesen || "<p style='color:rgba(255,255,255,0.7)'>Eşleşen yetenek bulunamadı</p>";

    var eksik = "";
    s.eksik_skills.forEach(function(yetenek) {
      eksik += "<span class='yetenek-etiketi eksik'>❌ " + yetenek + "</span>";
    });
    document.getElementById("eksik_div").innerHTML = eksik || "<p style='color:#2ecc71'>🎉 Tüm yetenekler eşleşti!</p>";

    var oneri = "";
    if(s.eksik_skills.length > 0) {
      oneri = "<div class='rapor-kutusu' style='margin-top:15px'><b>💡 Öneriler:</b><ul style='margin-top:10px;padding-left:20px'>";
      s.eksik_skills.forEach(function(yetenek) {
        oneri += "<li style='margin:5px 0'>" + yetenek + " öğrenmek için: <a href='https://www.google.com/search?q=" + yetenek + "+tutorial' target='_blank'>Google'da Ara</a></li>";
      });
      oneri += "</ul></div>";
    }
    document.getElementById("oneri_div").innerHTML = oneri;

    var rapor = "";
    rapor += "<div class='rapor-kutusu'><b>📊 Analiz Özeti:</b><br><br>";
    rapor += "CV'nizdeki toplam yetenek: <b>" + veri.cv_skills.length + "</b><br>";
    rapor += "İş ilanındaki toplam yetenek: <b>" + veri.is_skills.length + "</b><br>";
    rapor += "Eşleşen yetenek sayısı: <b>" + s.eslesen_skills.length + "</b><br>";
    rapor += "Eksik yetenek sayısı: <b>" + s.eksik_skills.length + "</b></div>";

    rapor += "<div class='rapor-kutusu' style='margin-top:10px'><b>🎯 Sonuç ve Tavsiye:</b><br><br>";
    if(skor >= 80) {
      rapor += "✅ Bu pozisyon için mükemmel bir adaysınız! Hemen başvurun!";
    } else if(skor >= 60) {
      rapor += "👍 Bu pozisyon için iyi bir aday profiliniz var. Eksik yetenekleri öğrenirseniz daha güçlü olursunuz.";
    } else if(skor >= 40) {
      rapor += "🤔 Orta düzeyde uyum var. Eksik yeteneklere odaklanmanızı öneririz.";
    } else {
      rapor += "📚 Bu pozisyon için daha fazla hazırlık gerekiyor. Eksik yetenekleri öğrenin.";
    }
    rapor += "</div>";

    document.getElementById("rapor_div").innerHTML = rapor;
    document.getElementById("sonuc_bolumu").scrollIntoView({behavior:"smooth"});
  })
  .catch(function(hata) {
    alert("Hata oluştu: " + hata);
  });
}
</script>
</body>
</html>"""

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
    