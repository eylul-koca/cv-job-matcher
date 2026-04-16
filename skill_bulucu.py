# skill_bulucu.py

SKILLS = [
    # Programlama dilleri
    "Python", "Java", "JavaScript", "TypeScript", "C#", "C++", "Go", "Ruby", "PHP", "Swift",
    
    # Backend
    "FastAPI", "Django", "Flask", "Spring Boot", "Express", "Node.js",
    
    # Frontend
    "React", "Vue", "Angular", "HTML", "CSS", "Tailwind",
    
    # Veritabanı
    "PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "SQL",
    
    # DevOps / Cloud
    "Docker", "Kubernetes", "AWS", "GCP", "Azure", "CI/CD", "Git", "Linux",
    
    # AI / Data
    "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch", "Pandas", "NumPy", "NLP",
    
    # Diğer
    "REST API", "GraphQL", "Microservices", "Agile", "Scrum"
]

def skill_bul(metin):
    """Metinden skill'leri bul"""
    bulunan = []
    
    for skill in SKILLS:
        if skill.lower() in metin.lower():
            bulunan.append(skill)
    
    return {
        "bulunan_skills": bulunan,
        "toplam": len(bulunan)
    }

# TEST
if __name__ == "__main__":
    test_metin = """
    Ahmet Yılmaz - Backend Developer
    Python, FastAPI, PostgreSQL, Docker, AWS kullandım.
    React ile frontend geliştirdim.
    Git, CI/CD, Linux bilgim var.
    """
    
    sonuc = skill_bul(test_metin)
    print(f"✅ {sonuc['toplam']} skill bulundu:")
    for s in sonuc['bulunan_skills']:
        print(f"  - {s}")
        