import PyPDF2
import pdfplumber
import glob
import os

def pdf_oku(dosya):
    print(f"📄 {os.path.basename(dosya)}")
    metin = ""
    
    # PyPDF2
    try:
        with open(dosya, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for sayfa in pdf.pages:
                metin += sayfa.extract_text() + "\n"
    except:
        pass
    
    # pdfplumber
    try:
        with pdfplumber.open(dosya) as pdf:
            for sayfa in pdf.pages:
                metin += sayfa.extract_text() + "\n"
    except:
        pass
    
    return metin.strip()

if __name__ == "__main__":
    pdfler = glob.glob("uploads/*.pdf")
    if pdfler:
        metin = pdf_oku(pdfler[0])
        print(f"📊 {len(metin)} karakter")
        print(metin[:300])
    else:
        print("PDF yükle!")