# eslestirici.py

def esles(cv_skills, is_skills):
    """CV ve iş ilanı skill'lerini karşılaştır"""
    
    cv_set = set([s.lower() for s in cv_skills])
    is_set = set([s.lower() for s in is_skills])
    
    # Eşleşen skill'ler
    eslesen = [s for s in cv_skills if s.lower() in is_set]
    
    # Eksik skill'ler
    eksik = [s for s in is_skills if s.lower() not in cv_set]
    
    # Skor hesapla
    if len(is_set) == 0:
        skor = 0
    else:
        skor = round((len(eslesen) / len(is_set)) * 100, 1)
    
    # Yorum
    if skor >= 80:
        yorum = "🟢 Çok iyi uyum!"
    elif skor >= 60:
        yorum = "🟡 İyi uyum"
    elif skor >= 40:
        yorum = "🟠 Orta uyum"
    else:
        yorum = "🔴 Düşük uyum"
    
    return {
        "skor": skor,
        "yorum": yorum,
        "eslesen_skills": eslesen,
        "eksik_skills": eksik,
        "cv_toplam": len(cv_skills),
        "is_toplam": len(is_skills)
    }

# TEST
if __name__ == "__main__":
    cv_skills = ["Python", "Java", "JavaScript", "HTML", "CSS", "Git"]
    is_skills = ["Python", "Docker", "AWS", "Git", "SQL"]
    
    sonuc = esles(cv_skills, is_skills)
    
    print(f"📊 Eşleşme Skoru: %{sonuc['skor']}")
    print(f"💬 Yorum: {sonuc['yorum']}")
    print(f"✅ Eşleşen: {sonuc['eslesen_skills']}")
    print(f"❌ Eksik: {sonuc['eksik_skills']}")
    