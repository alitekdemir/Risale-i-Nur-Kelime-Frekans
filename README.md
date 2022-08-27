# Risale-i Nur Kelime Frekansı

**Risale-i Nur'da Sıklıkla Kullanılan Kelimelerin Periyodik Olarak Tekrarlanma Oranı (Frekansı)**

### Sayfa altlarındaki sözlüğe bakmaktan kurtulmak mümkün!

Risale-i Nur okuyanların en fazla yaşadığı problem, birçok kelimeyi bilmemek veya anlamını hatırlayamamaktır.
Aslında eserlerde geçen pek çok kelimeyi, Türkçe bilen hemen hemen herkesin bilmesine rağmen kelimeleri çok az kullandığından, zihninde anlamı oturtması için tekrar etmesi gerekiyor. Bu durumdan dolayı yorulan kimseler ümitsizliğe kapılıp eseri okumayı terk edebiliyorlar.
**Burada amaçladığm, kelimelerin öğrenme sürecini ALFABETİK sıraya göre değil kelimelerin sıklık sırasına göre düzenlemek.**
Böylelikle her yeni okuyucu çok hızlı bir şekilde eserlerden tek başına daha doğru istifade edebilmeye başlayacaktır.
## *Frekansı en çok olanı önce öğrenerek sözlüklere daha az bakmaya matematiksel bir yaklaşım.*

Yaptığım çalışmada aşağıdaki değerlere ulaştım. Bu değerlere göre örneğin Sözler adlı kitaptaki 9922 farklı kelimeyi (bunların bir kısmı eklerle türetilmiştir; hakiki, hakikat, hakaik gibi) bilebilseydik 27092 defa sayfa altına bakma ihtiyacı duymazdık. Tabi bu kadar kelimeyi öğrenmek zaman alacaktır fakat başlangıç için en çok kullanılan kelimelerin ilk 100 adeti acaba bize ne kazandırırdı? En çok tekrarlanan ilk 300 veya 500 kelime toplamda kaç tekrar gücüne sahip? Bizi kaç defa sayfa altlarına bakmaktan kurtarabilir?

| Kitap     | Mükerrer Kelime | Özgün Kelime |
| --------- | --------------- | ------------ |
| Sözler    | 27092           | 9922         |
| Mektubat  | 7201            | 3853         |
| Lemalar   | 18216           | 6927         |
| Şualar    | 29535           | 7531         |
| Mesnevi   | 18091           | 6123         |
| Barla     | 22451           | 7822         |
| Muhakemat | 12016           | 5199         |

Aşağıdaki kod yaptığım çalışmada kullandığım bir parça. Kodların tamamını yukarıdaki "Risale_i_Nur_Kelime_Analizleri_2022_07_28.ipynb" dosyasında bulabilirsiniz.
```python
soz1defa         = sozler['kelime'].value_counts().where(sozler['kelime'].value_counts() == 1).dropna().size
soz1den_buyukler = sozler['kelime'].value_counts().where(sozler['kelime'].value_counts() > 1).dropna().size
print("Sözler'de 1'den fazla tekrarı olan kelimeler", soz1den_buyukler)
print("Sözler'de 1 defa kullanılan kelimeler", soz1defa)
```

Yukarıdaki kod çıktı olarak aşağıdaki sonuçları vermektedir.
```
Sözler'de 1'den fazla tekrarı olan kelimeler 3599
Sözler'de 1 defa kullanılan kelimeler 6323
```

Görüldüğü üzere öğrenilmesi gereken 9922 kelimenin 6323 adeti sadece 1 defa kullanılmış görünüyor.
3599 adet kelime ise 2 veya daha fazla kullanılmış. Yaklaşık 2 katı kadar kelime Sözler adlı eserde bir defa kullanılmış.
Buradan yola çıkarak kelimelerin pek çoğunun ilgili konuya özel ve sadece yerinde kullanıldığını görebiliriz. Ayrıca sayfa altlarında bulunan kelimeleri derleme şeklimiz %100 doğru sonuca ulaşmamızı engellediğini de belirtmek gerekli. Çünkü sayfa altındaki kelime listesine erisale.com gibi sitelerden derledik. Bir sayfada birden fazla tekrarı olmuş olsa bile sayfa altında bir defa geçtiğinden frekans değeri etkilenmiş olacaktır. Fakat ilk 500 kelime listesi içinde sırası değişse de liste içinde kalacağını (%90+) söyleyebiliriz.

--------

Şimdi en çok kullanılan kelimelerin tekrarlarına odaklanalım.
İlk 100, 200 ... 1000 ve 2'den fazla tekrarlananların toplam değerini bulalım.
```python
ozgun = sozler['kelime'].value_counts()

print("Sözler'deki ilk 100 kelimenin tekrar toplamı : ",  ozgun.head(100).sum())
print("Sözler'deki ilk 200 kelimenin tekrar toplamı : ",  ozgun.head(200).sum())
print("Sözler'deki ilk 300 kelimenin tekrar toplamı : ",  ozgun.head(300).sum())
print("Sözler'deki ilk 400 kelimenin tekrar toplamı : ",  ozgun.head(400).sum())
print("Sözler'deki ilk 500 kelimenin tekrar toplamı : ",  ozgun.head(500).sum())
print("Sözler'deki ilk 1000 kelimenin tekrar toplamı : ", ozgun.head(1000).sum())
print("Sözler'deki ilk 3599 kelimenin tekrar toplamı : ", ozgun.head(3599).sum())
```
Yukarıdaki kod çıktı olarak aşağıdaki sonuçları vermektedir.
```
Sözler'deki ilk 100 kelimenin tekrar toplamı :  4540
Sözler'deki ilk 200 kelimenin tekrar toplamı :  6660
Sözler'deki ilk 300 kelimenin tekrar toplamı :  8153
Sözler'deki ilk 400 kelimenin tekrar toplamı :  9333
Sözler'deki ilk 500 kelimenin tekrar toplamı :  10313
Sözler'deki ilk 1000 kelimenin tekrar toplamı :  13689
Sözler'deki ilk 3599 kelimenin tekrar toplamı :  20769
```

## Analiz ve sağlama yapalım.

Sözler adlı kitapta sayfa altlarındaki sözlükte bulunan kelime sayısı, tekrarlar dahil 27092 </br>
Sözler adlı kitapta sayfa altlarındaki sözlükte bulunan kelime sayısı, tekrarlar hariç 9922 </br>
Sözler adlı kitapta sayfa altlarındaki sözlükte 2 defadan fazla kullanılan kelime sayısı ise 3599 </br>

9922 - 3599 = 6323 </br>
27092 - 20769 = 6323

## Şimdi de elde ettiğimiz sonuçların yüzdesini hesaplayalım. Formülümüz;

İlk 100 kelimenin tekrar toplamı / Bir kitaptaki tekrarlanan kelimelerin adedi X 100

```
4540 / 27092 * 100 = %16,75
```

Evet 100 kelime tekrarların yaklaşık %17 sini karşılıyor. Başlangıç için çok iyi öyle değil mi?

| Kitap     | 1-100 Kelime | 200 Kelime | 300 Kelime | 400 Kelime | 500 Kelime | 1000 Kelime |
| --------- | ------------ | ---------- | ---------- | ---------- | ---------- | ----------- |
| Sözler    | 16.76%       | 24.58%     | 30.09%     | 34.45%     | 38.07%     | 50.53%      |
| Mektubat  | 18.07%       | 26.59%     | 32.93%     | 38.45%     | 42.62%     | 58.24%      |
| Lemalar   | 18.26%       | 26.92%     | 33.10%     | 38.01%     | 42.06%     | 55.58%      |
| Şualar    | 22.39%       | 31.75%     | 38.69%     | 44.06%     | 48.44%     | 62.46%      |
| Mesnevi   | 19.70%       | 28.59%     | 34.97%     | 39.97%     | 44.11%     | 58.65%      |
| Barla     | 20.53%       | 28.50%     | 34.00%     | 38.25%     | 41.67%     | 53.56%      |
| Muhakemat | 15.26%       | 22.44%     | 27.70%     | 32.04%     | 35.94%     | 50.02%      |

Kelime sayısı arttıkça sıklık azalıyor.
300 kelime %30'u karşılıyor!
1000 kelime ise %50+ kelimeyi karşılıyor ve lügata bakmaktan kurtarıyor.

Sonuç olarak yeni başlayanlar ve çocuklar için ilk 300-500 kelimenin öğrenileceği basit bir sözlük çok elverişli olacağı apaçık ortadadır.
Peki ilk 100 kelimede neler var?
Burada çok yer tutacağından python kodlarını ve zamanla sonuçları da haricen yüklemek niyetindeyim.

## Merak edileceği üzere Sözler'deki ilk 100 kelime aşağıdadır.

Aşağıdaki 100 kelimeden acaba bildikleriniz kaç tanesi?
Örneğin nazar, zemin, aciz, kainat, alem gibi bildiklerinizi de düşünürseniz 1000 kelimeyi öğrenmek sizce ne kadar zaman alır?

> suret, hakikat, kâinat, hikmet, nefis, mevcudat, kudret, âlem, nazar, nihayetsiz, mazhar, rahmet, zemin, cihet, hadsiz, hakikî, şehadet, sair, beyan, saadet, intizam, icad, temsil, nevi, nuranî, nam, umum, Hâlık, muntazam, muhtelif, arz, Kur’ân-ı Hakîm, âhiret, Cenâb-ı Hak, mahiyet, mâlik, beşer, cilve, mahlûkat, vücud, lisan, cüz’î, tabiat, lâtif, zîhayat, kat’î, Sâni, medar, ulvî, ziya, acz, âciz, zerre, küllî, dalâlet, ubûdiyet, mahlûk, kemâl, nisbet, haşir, esmâ, istidat, âyine, kelâm, saadet-i ebediye, esbab, ebedî, Sâni-i Hakîm, azîm, ihsan, acip, mukabil, ziyade, delâlet, taife, Sâni-i Zülcelâl, muvazene, nihayet, câmid, inkâr, mizan, elhasıl, muhabbet, hak, ihtiyar, nev’, zikretmek, burhan, haşiye, ekser, Aleyhissalâtü Vesselâm, irade, bekà, menzil, muhal, Zât-ı Zülcelâl, vahdet, semâ, musahhar, eşya  >

*İnşallah pek yakında güncellenmeye devam edecek...*
