# 01-Analiz.py
import os
from collections import Counter

def turkce_normalize(text):
    """Türkçe karakterleri koruyan büyük/küçük harf dönüşümü"""
    buyuk = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    kucuk = "abcçdefgğhıijklmnoöprsştuüvyz"
    trans_table = str.maketrans(buyuk, kucuk)
    return text.translate(trans_table)

def kelime_kapsami_hesapla(frekanslar, toplam_kelime, n):
    """İlk n kelimenin toplam kelime sayısına oranını hesaplar"""
    ilk_n_toplam = sum(sayi for _, sayi in frekanslar.most_common(n))
    return ilk_n_toplam, (ilk_n_toplam / toplam_kelime) * 100

def dosya_analiz(kaynak, dosya_yolu, dosya_adi):
    """Tek bir CSV dosyasını analiz eder ve sonuçları iki ayrı dosyaya yazar"""
    # Çalışma dizininden base_path oluştur
    base_path = os.getcwd()
    
    # Kaynak için analiz klasörü oluştur
    analiz_klasor = os.path.join(base_path, "data", kaynak, "analysis", "terkipli")
    os.makedirs(analiz_klasor, exist_ok=True)
    
    # Kelimeleri oku ve frekansları hesapla
    kelimeler = []
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        next(f)
        for line in f:
            kelime = line.split(',')[0].strip('"').strip()
            # Kelimeyi normalize et
            kelime = turkce_normalize(kelime)
            kelimeler.append(kelime)
    
    frekanslar = Counter(kelimeler)
    toplam_kelime = len(kelimeler)
    benzersiz_kelime = len(frekanslar)
    
    # 1. Analiz dosyası
    analiz_dosya = os.path.join(analiz_klasor, dosya_adi.replace('.csv', '_analiz.txt'))
    with open(analiz_dosya, 'w', encoding='utf-8') as f:
        f.write(f"Dosya: {dosya_adi}\n")
        f.write(f"Toplam kelime sayısı: {toplam_kelime:,}\n")
        f.write(f"Benzersiz kelime sayısı: {benzersiz_kelime:,}\n\n")
        
        f.write("En sık kullanılan kelimeler:\n")
        ilk_10_toplam = 0
        for kelime, sayi in frekanslar.most_common(10):
            f.write(f"{kelime}: {sayi}\n")
            ilk_10_toplam += sayi
        
        f.write(f"\nİlk 10 kelimenin toplamı: {ilk_10_toplam:,}\n")
        f.write(f"İlk 10 kelimenin yüzdesi: {(ilk_10_toplam/toplam_kelime)*100:.2f}%\n\n")
        
        # Farklı n değerleri için kapsam analizi
        for n in [100, 200, 250, 500, 750, 1000]:
            toplam, yuzde = kelime_kapsami_hesapla(frekanslar, toplam_kelime, n)
            f.write(f"İlk {n} kelime toplamı: {toplam:,} ({yuzde:.2f}%)\n")
    
    # 2. Frekans listesi dosyası
    frekans_dosya = os.path.join(analiz_klasor, dosya_adi.replace('.csv', '_frekans.txt'))
    with open(frekans_dosya, 'w', encoding='utf-8') as f:
        f.write("kelime,frekans\n")
        for kelime, sayi in frekanslar.most_common():
            f.write(f"{kelime},{sayi}\n")

def risale_analiz(kaynak):
    """Tüm risaleleri analiz eder"""
    base_path = os.getcwd()
    raw_path = os.path.join(base_path, "data", kaynak, "raw")
    
    for dosya in os.listdir(raw_path):
        if dosya.endswith('.csv'):
            print(f"\n{dosya} analiz ediliyor...")
            dosya_analiz(kaynak, os.path.join(raw_path, dosya), dosya)
            print(f"{dosya} analizi tamamlandı.")

# Her iki kaynak için analizi çalıştır
for kaynak in ["eRisale", "SorularlaRisale"]:
    print(f"\n{kaynak} analizleri başlıyor...")
    risale_analiz(kaynak)
    print(f"{kaynak} analizleri tamamlandı.")
