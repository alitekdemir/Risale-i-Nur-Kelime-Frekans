# 01-Analiz.py
import os

def analiz_verilerini_oku(kaynak, analiz_turu):
    """Analiz dosyalarından verileri okur"""
    base_path = os.getcwd()
    analiz_klasor = os.path.join(base_path, "data", kaynak, "analysis", analiz_turu)
    
    veriler = {}
    
    for dosya in os.listdir(analiz_klasor):
        if dosya.endswith('_analiz.txt'):
            kitap_adi = dosya.replace('_analiz.txt', '')
            veriler[kitap_adi] = {}
            
            with open(os.path.join(analiz_klasor, dosya), 'r', encoding='utf-8') as f:
                icerik = f.readlines()
                
                for line in icerik:
                    line = line.strip()
                    if "Toplam kelime sayısı:" in line:
                        toplam = int(line.split(":")[1].strip().replace(",", ""))
                        veriler[kitap_adi]["Toplam Kelime"] = toplam
                    
                    elif "Benzersiz kelime sayısı:" in line:
                        benzersiz = int(line.split(":")[1].strip().replace(",", ""))
                        veriler[kitap_adi]["Özgün Kelime"] = benzersiz
                    
                    elif "İlk" in line and "kelime toplamı:" in line and "(" in line:
                        parts = line.split()
                        n = int(parts[1])
                        toplam = int(parts[4].replace(",", ""))
                        yuzde = float(line.split("(")[1].split("%")[0])
                        
                        if n in [100, 200, 500, 1000]:  # Sadece tabloda istenen değerler
                            veriler[kitap_adi][f"{n} Kelime"] = toplam
                            veriler[kitap_adi][f"{n}%"] = yuzde
    
    return veriler

def tablo_olustur(veriler, tablo_turu="rakamsal"):
    """Markdown formatında tablo oluşturur"""
    if tablo_turu == "rakamsal":
        basliklar = ["Kitap", "Toplam Kelime", "Özgün Kelime", "100 Kelime", 
                     "200 Kelime", "500 Kelime", "1000 Kelime"]
    else:  # yuzdelik
        basliklar = ["Kitap", "Toplam Kelime", "100 Kelime", "200 Kelime", 
                     "500 Kelime", "1000 Kelime"]
    
    # Tablo başlığı
    tablo = ["| " + " | ".join(basliklar) + " |"]
    # Ayraç satırı
    tablo.append("| " + " | ".join(["-" * len(b) for b in basliklar]) + " |")
    
    # Veri satırları
    for kitap in sorted(veriler.keys()):  # Kitapları sırala
        degerler = veriler[kitap]
        if tablo_turu == "rakamsal":
            satir = [
                kitap,
                f"{degerler['Toplam Kelime']:,}",
                f"{degerler['Özgün Kelime']:,}",
                f"{degerler['100 Kelime']:,}",
                f"{degerler['200 Kelime']:,}",
                f"{degerler['500 Kelime']:,}",
                f"{degerler['1000 Kelime']:,}"
            ]
        else:  # yuzdelik
            satir = [
                kitap,
                str(degerler['Toplam Kelime']),
                f"{degerler['100%']:.1f}%",
                f"{degerler['200%']:.1f}%",
                f"{degerler['500%']:.1f}%",
                f"{degerler['1000%']:.1f}%"
            ]
        tablo.append("| " + " | ".join(satir) + " |")
    
    return "\n".join(tablo)

def tablolari_olustur_ve_kaydet():
    """Her iki analiz türü için tabloları oluşturur ve kaydeder"""
    for analiz_turu in ["terkipli", "terkipsiz"]:
        veriler = analiz_verilerini_oku("eRisale", analiz_turu)
        
        with open(f"tablolar_{analiz_turu}.md", "w", encoding="utf-8") as f:
            f.write(f"# {analiz_turu.title()} Kelimeler\n\n")
            
            f.write("## Kelimelerin karşıladığı **rakamsal** değerler\n\n")
            f.write(tablo_olustur(veriler, "rakamsal"))
            f.write("\n\n")
            
            f.write("## Kelimelerin karşıladığı **yüzdelik** dilimler\n\n")
            f.write(tablo_olustur(veriler, "yuzdelik"))

if __name__ == "__main__":
    tablolari_olustur_ve_kaydet()
