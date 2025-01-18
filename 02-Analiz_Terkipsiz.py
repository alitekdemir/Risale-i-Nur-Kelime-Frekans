# 02-Analiz_Terkipsiz.py
import os
from collections import Counter

def turkce_normalize(text):
    """Türkçe karakterleri koruyan büyük/küçük harf dönüşümü"""
    buyuk = "ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ"
    kucuk = "abcçdefgğhıijklmnoöprsştuüvyz"
    trans_table = str.maketrans(buyuk, kucuk)
    return text.translate(trans_table)

def kelime_parcala(kelime):
    """Kelimeleri parçalara ayırır ve ekleri temizler"""
    ekler = ["-ı", "-i", "-u", "-ü", "-yi", "-yı", "-ye", "-ya"]
    
    parcalar = []
    for parca in kelime.split():
        if '-' in parca:
            alt_parcalar = parca.split('-')
            for alt_parca in alt_parcalar:
                if alt_parca not in ['ı', 'i', 'u', 'ü', 'yi', 'yı', 'ye', 'ya']:
                    temiz_parca = alt_parca
                    for ek in ekler:
                        if alt_parca.endswith(ek):
                            temiz_parca = alt_parca[:-len(ek)]
                            break
                    if temiz_parca:
                        parcalar.append(temiz_parca)
        else:
            parcalar.append(parca)
    
    return parcalar

def kelime_kapsami_hesapla(frekanslar, toplam_kelime, n):
    """İlk n kelimenin toplam kelime sayısına oranını hesaplar"""
    ilk_n_toplam = sum(sayi for _, sayi in frekanslar.most_common(n))
    return ilk_n_toplam, (ilk_n_toplam / toplam_kelime) * 100

def terkipsiz_analiz(kaynak, dosya_yolu, dosya_adi):
    """Terkipsiz analiz yapar ve sonuçları kaydeder"""
    # Analiz klasörünü oluştur
    base_path = os.getcwd()
    analiz_klasor = os.path.join(base_path, "data", kaynak, "analysis", "terkipsiz")
    os.makedirs(analiz_klasor, exist_ok=True)
    
    # Kelimeleri oku ve parçala
    tum_kelimeler = []
    with open(dosya_yolu, 'r', encoding='utf-8') as f:
        next(f)  # Header'ı atla
        for line in f:
            kelime = line.split(',')[0].strip('"').strip()
            tum_kelimeler.extend(kelime_parcala(kelime))
    
    # Frekansları hesapla
    frekanslar = Counter(map(turkce_normalize, tum_kelimeler))
    toplam_kelime = sum(frekanslar.values())
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
        
        for n in [100, 200, 250, 500, 750, 1000]:
            toplam, yuzde = kelime_kapsami_hesapla(frekanslar, toplam_kelime, n)
            f.write(f"İlk {n} kelime toplamı: {toplam:,} ({yuzde:.2f}%)\n")
    
    # 2. Frekans listesi
    frekans_dosya = os.path.join(analiz_klasor, dosya_adi.replace('.csv', '_frekans.txt'))
    with open(frekans_dosya, 'w', encoding='utf-8') as f:
        f.write("kelime,frekans\n")
        for kelime, sayi in frekanslar.most_common():
            f.write(f"{kelime},{sayi}\n")

def risale_terkipsiz_analiz(kaynak):
    """Tüm risalelerin terkipsiz analizini yapar"""
    base_path = os.getcwd()
    raw_path = os.path.join(base_path, "data", kaynak, "raw")
    
    for dosya in os.listdir(raw_path):
        if dosya.endswith('.csv'):
            print(f"\n{dosya} terkipsiz analiz ediliyor...")
            terkipsiz_analiz(kaynak, os.path.join(raw_path, dosya), dosya)
            print(f"{dosya} terkipsiz analizi tamamlandı.")

# Her iki kaynak için analizi çalıştır
for kaynak in ["eRisale", "SorularlaRisale"]:
    print(f"\n{kaynak} terkipsiz analizleri başlıyor...")
    risale_terkipsiz_analiz(kaynak)
    print(f"{kaynak} terkipsiz analizleri tamamlandı.")

