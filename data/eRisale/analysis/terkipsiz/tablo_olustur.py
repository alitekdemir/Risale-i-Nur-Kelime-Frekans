import os
from collections import defaultdict

def tablo_satiri_olustur(veriler, basliklar, ayrac="|"):
    """Markdown tablo satırı oluşturur"""
    return f"{ayrac} " + f" {ayrac} ".join(str(veriler.get(b, '')) for b in basliklar) + f" {ayrac}"

def tablo_olustur(baslik, basliklar, veriler):
    """Markdown tablosu oluşturur"""
    # Tablo başlığı
    tablo = [f"## {baslik}\n"]
    
    # Başlık satırı
    tablo.append(tablo_satiri_olustur(dict(zip(basliklar, basliklar)), basliklar))
    
    # Ayraç satırı
    tablo.append(tablo_satiri_olustur(dict(zip(basliklar, ['-' * len(b) for b in basliklar])), basliklar))
    
    # Veri satırları
    for kitap, degerler in veriler.items():
        tablo.append(tablo_satiri_olustur(degerler, basliklar))
    
    return "\n".join(tablo)

def sayi_formatla(sayi):
    """Sayıyı binlik ayraçlı formata çevirir"""
    return f"{sayi:,}"

def yuzde_formatla(yuzde):
    """Yüzdeyi formatlar"""
    return f"{yuzde:.1f}%"

def analiz_verilerini_oku(kaynak, analiz_turu):
    """Analiz dosyalarından verileri okur"""
    base_path = os.getcwd()
    analiz_klasor = os.path.join(base_path, "data", kaynak, "analysis", analiz_turu)
    
    veriler = defaultdict(dict)
    
    for dosya in os.listdir(analiz_klasor):
        if dosya.endswith('_analiz.txt'):
            kitap_adi = dosya.replace('_analiz.txt', '')
            
            with open(os.path.join(analiz_klasor, dosya), 'r', encoding='utf-8') as f:
                icerik = f.readlines()
                
                for line in icerik:
                    # Toplam ve benzersiz kelime sayıları
                    if "Toplam kelime sayısı:" in line:
                        veriler[kitap_adi]["Toplam Kelime"] = int(line.split(":")[1].strip().replace(",", ""))
                    elif "Benzersiz kelime sayısı:" in line:
                        veriler[kitap_adi]["Özgün Kelime"] = int(line.split(":")[1].strip().replace(",", ""))
                    
                    # İlk N kelime analizleri
                    elif "İlk" in line and "kelime toplamı:" in line:
                        n = int(line.split()[1])
                        toplam = int(line.split(":")[1].split("(")[0].strip().replace(",", ""))
                        yuzde = float(line.split("(")[1].split("%")[0])
                        
                        veriler[kitap_adi][f"{n} Kelime"] = toplam
                        veriler[kitap_adi][f"{n} %"] = yuzde
    
    return veriler

def tablolari_olustur(kaynak, analiz_turu):
    """Rakamsal ve yüzdelik tabloları oluşturur"""
    veriler = analiz_verilerini_oku(kaynak, analiz_turu)
    
    # Tablo başlıkları
    rakamsal_basliklar = ["Kitap", "Toplam Kelime", "Özgün Kelime"] + [f"{n} Kelime" for n in [100, 200, 300, 400, 500, 1000, 2000]]
    yuzdelik_basliklar = ["Kitap", "Toplam Kelime"] + [f"{n} %" for n in [100, 200, 300, 400, 500, 1000, 2000]]
    
    # Rakamsal tablo verilerini formatla
    rakamsal_veriler = {}
    for kitap, degerler in veriler.items():
        rakamsal_veriler[kitap] = {"Kitap": kitap}
        for baslik in rakamsal_basliklar[1:]:
            if baslik in degerler:
                rakamsal_veriler[kitap][baslik] = sayi_formatla(degerler[baslik])
    
    # Yüzdelik tablo verilerini formatla
    yuzdelik_veriler = {}
    for kitap, degerler in veriler.items():
        yuzdelik_veriler[kitap] = {"Kitap": kitap}
        for baslik in yuzdelik_basliklar[1:]:
            if baslik in degerler:
                yuzdelik_veriler[kitap][baslik] = yuzde_formatla(degerler[baslik])
    
    # Tabloları oluştur
    rakamsal_tablo = tablo_olustur(
        f"Kelimelerin karşıladığı **rakamsal** değerler ({analiz_turu})",
        rakamsal_basliklar,
        rakamsal_veriler
    )
    
    yuzdelik_tablo = tablo_olustur(
        f"Kelimelerin karşıladığı **yüzdelik** dilimler ({analiz_turu})",
        yuzdelik_basliklar,
        yuzdelik_veriler
    )
    
    return rakamsal_tablo, yuzdelik_tablo

def tablolari_kaydet(kaynak):
    """Tabloları oluşturur ve dosyaya kaydeder"""
    for analiz_turu in ["terkipli", "terkipsiz"]:
        rakamsal_tablo, yuzdelik_tablo = tablolari_olustur(kaynak, analiz_turu)
        
        with open(f"tables_{analiz_turu}.md", 'w', encoding='utf-8') as f:
            f.write(rakamsal_tablo)
            f.write("\n\n")
            f.write(yuzdelik_tablo)

if __name__ == "__main__":
    for kaynak in ["eRisale", "SorularlaRisale"]:
        print(f"{kaynak} tabloları oluşturuluyor...")
        tablolari_kaydet(kaynak)
        print(f"{kaynak} tabloları oluşturuldu.")
