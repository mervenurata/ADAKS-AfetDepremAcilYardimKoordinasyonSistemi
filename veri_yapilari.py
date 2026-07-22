# ARAMA VE OTOMATİK TAMAMLAMA (TRIE)
# ComboBox'larda (Ekip, İhtiyaç, Adres) hızlı arama ve öneri sunmak için kullanılır.
# Karmaşıklık: O(M) - M: Aranan kelimenin uzunluğu. Standart listeden (O(N)) çok daha hızlıdır.
class TrieDugumu:
    def __init__(self):
        # Her bir harf için alt dalları tutan sözlük yapısı.
        self.cocuklar = {}
        # Bir kelimenin bu noktada tamamlanıp tamamlanmadığını belirtir.
        self.kelime_sonu_mu = False


class GenelTrie:
    def __init__(self):
        # Ağacın başlangıç (kök) noktası.
        self.kok = TrieDugumu()

    def ekle(self, metin):
        # Kelimeyi harf harf ağaç yapısına (prefix tree) yerleştirir.
        aktif = self.kok
        for harf in metin.lower():
            if harf not in aktif.cocuklar:
                aktif.cocuklar[harf] = TrieDugumu()
            aktif = aktif.cocuklar[harf]
        aktif.kelime_sonu_mu = True

    def oneri_getir(self, on_ek):
        # Verilen ön eke göre ağaçta gezinip tüm alternatif kelimeleri döndürür.
        aktif = self.kok
        on_ek = on_ek.lower()
        for harf in on_ek:
            if harf not in aktif.cocuklar: return []
            aktif = aktif.cocuklar[harf]

        sonuclar = []
        # Ön ekin bittiği yerden itibaren tüm kelimeleri rekürsif olarak bulur.
        self._kelimeleri_bul(aktif, on_ek, sonuclar)
        return sonuclar

    def _kelimeleri_bul(self, dugum, anlik_kelime, sonuclar):
        # Bulunan kelimeyi listeye ekler.
        if dugum.kelime_sonu_mu: sonuclar.append(anlik_kelime)
        # Alt dallarda derinlemesine arama (DFS) yapar.
        for harf, cocuk_dugum in dugum.cocuklar.items():
            self._kelimeleri_bul(cocuk_dugum, anlik_kelime + harf, sonuclar)


# MÜDAHALE GEÇMİŞİ (LINKED LIST)
# Logların (işlem geçmişi) dinamik ve esnek bir şekilde saklanmasını sağlar.
# Karmaşıklık: Başa ekleme O(1) sabit zamanlıdır.
class BagliListeDugumu:
    def __init__(self, veri):
        self.veri = veri
        self.sonraki = None


class LogBagliListe:
    def __init__(self):
        # Listenin başlangıç noktası.
        self.bas = None

    def basa_ekle(self, veri):
        # Yeni veriyi listenin en başına (son girilen en üstte görünecek şekilde) ekler.
        yeni_dugum = BagliListeDugumu(veri)
        yeni_dugum.sonraki = self.bas
        self.bas = yeni_dugum

    def listele(self):
        # Listenin başından sonuna kadar tüm düğümleri gezip listeye aktarır.
        sonuclar, aktif = [], self.bas
        while aktif:
            sonuclar.append(aktif.veri)
            aktif = aktif.sonraki
        return sonuclar


# ENVANTER YÖNETİMİ (BINARY SEARCH TREE - BST)
# Ürünlerin alfabetik sıralanmasını ve verimli bir şekilde aranmasını sağlar.
# Karmaşıklık: Ortalama O(log N) arama/ekleme süresi.
class BSTAgaçDugumu:
    def __init__(self, urun):
        self.urun = urun
        self.sol = None
        self.sag = None


class EnvanterBST:
    def __init__(self):
        self.kok = None

    def ekle(self, urun):
        # Ağaç boşsa kökü oluşturur, doluysa uygun konumu rekürsif olarak arar.
        if self.kok is None:
            self.kok = BSTAgaçDugumu(urun)
        else:
            self._ekle_rekursif(self.kok, urun)

    def _ekle_rekursif(self, dugum, urun):
        # Alfabetik sıraya göre sol veya sağ dallanmaya karar verir.
        if urun.ad < dugum.urun.ad:
            if dugum.sol is None:
                dugum.sol = BSTAgaçDugumu(urun)
            else:
                self._ekle_rekursif(dugum.sol, urun)
        elif urun.ad > dugum.urun.ad:
            if dugum.sag is None:
                dugum.sag = BSTAgaçDugumu(urun)
            else:
                self._ekle_rekursif(dugum.sag, urun)
        else:
            # Ürün zaten varsa sadece miktar güncellemesi yapar.
            dugum.urun.miktar += urun.miktar

    def inorder_gezin(self, dugum, liste):
        # Sol-Kök-Sağ sıralaması ile ürünleri alfabetik (A'dan Z'ye) listeler.
        if dugum:
            self.inorder_gezin(dugum.sol, liste)
            liste.append(dugum.urun)
            self.inorder_gezin(dugum.sag, liste)

    def tum_urunler(self):
        liste = []
        self.inorder_gezin(self.kok, liste)
        return liste

    def miktar_azalt(self, urun_adi, miktar):
        # Belirli bir ürünü bulup miktarını eksiltir.
        dugum = self._dugum_bul(self.kok, urun_adi)
        if dugum and dugum.urun.miktar >= miktar:
            dugum.urun.miktar -= miktar
            return True
        return False

    def _dugum_bul(self, dugum, urun_adi):
        # İkili arama mantığı ile düğümü bulur.
        if dugum is None: return None
        if urun_adi == dugum.urun.ad: return dugum
        if urun_adi < dugum.urun.ad: return self._dugum_bul(dugum.sol, urun_adi)
        return self._dugum_bul(dugum.sag, urun_adi)

    def sil(self, urun_adi):
        # Ürünü ağaçtan çıkarırken BST yapısını koruyarak düğümleri yeniden bağlar.
        self.kok = self._sil_rekursif(self.kok, urun_adi)

    def _sil_rekursif(self, dugum, urun_adi):
        if dugum is None: return None

        if urun_adi < dugum.urun.ad:
            dugum.sol = self._sil_rekursif(dugum.sol, urun_adi)
        elif urun_adi > dugum.urun.ad:
            dugum.sag = self._sil_rekursif(dugum.sag, urun_adi)
        else:
            # Tek çocuklu veya çocuksuz düğüm silme durumu.
            if dugum.sol is None:
                return dugum.sag
            elif dugum.sag is None:
                return dugum.sol

            # İki çocuklu düğümde sağ alt ağacın en küçüğünü (successor) bulup yerine koyar.
            gecici = self._min_deger_dugumu(dugum.sag)
            dugum.urun = gecici.urun
            dugum.sag = self._sil_rekursif(dugum.sag, gecici.urun.ad)
        return dugum

    def _min_deger_dugumu(self, dugum):
        # Alt ağaçtaki en soldaki (en küçük) düğüme ulaşır.
        aktif = dugum
        while aktif.sol is not None:
            aktif = aktif.sol
        return aktif


# GERİ ALMA SİSTEMİ (STACK/YIĞIN)
# İşlemleri Son Giren İlk Çıkar (LIFO) mantığıyla yönetir.
class Yigin:
    def __init__(self): self.yigin = []

    # O(1) maliyetle veriyi en üste ekler.
    def push(self, islem): self.yigin.append(islem)

    # O(1) maliyetle en üstteki veriyi çıkarır.
    def pop(self): return self.yigin.pop() if not self.bos_mu() else None

    def bos_mu(self): return len(self.yigin) == 0


# GÖNÜLLÜ/HİZMET SIRALAMASI (QUEUE/KUYRUK)
# Verileri İlk Gelen İlk Çıkar (FIFO) mantığıyla yönetir.
class Kuyruk:
    def __init__(self): self.kuyruk = []

    # O(1) maliyetle sıranın sonuna ekleme yapar.
    def enqueue(self, kisi): self.kuyruk.append(kisi)

    # O(N) maliyetle sıranın başından veri çıkarır (liste kaydırma nedeniyle).
    def dequeue(self): return self.kuyruk.pop(0) if not self.bos_mu() else None

    def bos_mu(self): return len(self.kuyruk) == 0

    def boyut(self): return len(self.kuyruk)


# SABİT KAPASİTELİ VERİ SAKLAMA (SABİT DİZİ)
# Bellekte önceden ayrılmış, boyutu değişmeyen veri alanı.
class SabitDizi:
    def __init__(self, kapasite):
        self.kapasite = kapasite
        self.dizi = [None] * kapasite

    def eleman_ata(self, indeks, veri):
        # Belirli bir indekse O(1) maliyetle erişim sağlar.
        if 0 <= indeks < self.kapasite: self.dizi[indeks] = veri

    def eleman_getir(self, indeks):
        # Belirli bir indeksteki veriyi O(1) maliyetle getirir.
        if 0 <= indeks < self.kapasite: return self.dizi[indeks]
        return None