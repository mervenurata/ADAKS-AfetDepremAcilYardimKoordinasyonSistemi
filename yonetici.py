import heapq
import time
import networkx as nx
from datetime import datetime
from modeller import Urun, MudahaleLog, Gorev, EkipTalebi
from veri_yapilari import LogBagliListe, EnvanterBST, Yigin, Kuyruk, SabitDizi, GenelTrie

class SistemYoneticisi:
    def __init__(self):
        self._sayac = 1
        # Graf Veri Yapısı: Şehir haritasını düğüm (nokta) ve kenar (yol) olarak temsil eder.
        self.sehir_grafi = nx.Graph()
        # Bağlı Liste (Linked List): Müdahale loglarını O(1) maliyetle saklar.
        self.mudahale_gecmisi = LogBagliListe()
        # Stack Mantığı: Taleplerin son girilen ilk çıkar (LIFO) prensibiyle geri alınmasını sağlar.
        self.islem_gecmisi_talepler = [] # Talepleri geri almak için stack
        
        # --- ÇOKLU DEPO SİSTEMİ (BST Kullanımı) ---
        # Her depo, ürünlerini alfabetik sıralı tutan ayrı bir Binary Search Tree (BST) yapısına sahiptir.
        self.depolar = ["Depo 1", "Depo 2", "Depo 3", "Depo 4"]
        self.depo_envanterleri = {depo: EnvanterBST() for depo in self.depolar}
        # -------------------------------
        self.tedarikciler = ["AFAD Lojistik", "Kızılay Merkez", "Yerel Tedarik Zinciri", "Uluslararası Yardım Ağı"]

        # Stack (Yığın): Görev tamamlama işlemlerini geri almak (Undo) için kullanılır.
        self.islem_gecmisi_yigini = Yigin()

        # Kuyruk (Queue): Gönüllüleri uzmanlık alanlarına göre FIFO (İlk Gelen İlk Çıkar) düzeninde tutar.
        self.gonullu_kuyruklari = {
            "Arama-Kurtarma": Kuyruk(),
            "Sağlık/Tıp": Kuyruk(),
            "Lojistik": Kuyruk(),
            "Psikososyal Destek": Kuyruk(),
            "Mutfak/Gıda": Kuyruk()
        }

        # Sabit Dizi (Static Array): Bellekte önceden ayrılmış sınırlı yedek araç filosunu temsil eder.
        self.arac_filosu = SabitDizi(5)

        # Hash Table (Dictionary): Görevlere ID üzerinden O(1) sürede erişim sağlar.
        self.gorev_yonetimi = {}

        # Heap (Priority Queue): Talepleri öncelik derecesine göre otomatik sıralı tutar.
        self.ekip_talepleri_heap = []

        # Trie (Önek Ağacı): Arama işlemlerinde otomatik tamamlama ve hızlı filtreleme sağlar.
        self.arama_trie = GenelTrie()
        
        self.tum_ekipler = ["Arama-Kurtarma 1", "Arama-Kurtarma 2", "Paramedik 1", "Paramedik 2", "Lojistik Destek"]
        self.musait_ekipler = set(self.tum_ekipler)
        self.musait_araclar = {
            "Ambulans-01", "Ambulans-02", "Ambulans-03", "Ambulans-04", 
            "İtfaiye-01", "İtfaiye-02", "İtfaiye-03", 
            "İş Makinesi-01", "Ekskavatör-01", "Vinç-01", "Kamyon-01"
        }
        
        self.mesgul_birimler = {} 
        
        self._baslangic_verilerini_yukle()

        self.tedarikci_verileri = {
        "Arama Kurtarma Ekipmanı": ["Hilti Türkiye", "Aksa Jeneratör"],
        "Barınma": ["Ankara Çadır Sarayı", "Nurşah Prefabrik"],
        "Gıda ve Su": ["Türk Kızılay Lojistik", "Ülker (Yıldız Holding)"],
        "Sağlık ve İlk Yardım": ["Türk İlaç", "Bıçakcılar Tıbbi Cihaz"],
        "Hijyen": ["Eczacıbaşı Profesyonel", "Hayat Kimya"],
        "Lojistik ve Enerji": ["Aksa Enerji", "Aras Kargo (Lojistik)"],
        "Personel/Gönüllü": ["AFAD Akademi", "UMKE"],
        "Araç/İş Makinesi": ["Hidromek", "BMC Otomotiv"]
    }

    def _baslangic_verilerini_yukle(self):
        # Gerçekçi afet kategorileri ve ihtiyaçları Trie'ye yükleniyor
        kategoriler = [
            "Arama Kurtarma Ekipmanı", "Barınma", "Gıda ve Su", 
            "Sağlık ve İlk Yardım", "Hijyen", "Lojistik ve Enerji", 
            "Personel/Gönüllü", "Araç/İş Makinesi", "Diğer Kategori"
        ]

        gercekci_ogeler = [
            "Hilti", "Jeneratör", "Termal Kamera", "Enkaz Dinleme Cihazı", "Demir Kesme Makası",
            "Çadır (Kışlık)", "Konteyner", "Uyku Tulumu", "Isıtıcı (Elektrikli)", "Isıtıcı (Tüplü)", "Battaniye", "Mat",
            "Su (5 Lt)", "Konserve Gıda", "Bebek Maması", "Bebek Bisküvisi", "Ekmek",
            "İlk Yardım Çantası", "Sargı Bezi", "Ağrı Kesici", "Turnike", "Sedye",
            "Bebek Bezi", "Kadın Pedi", "Islak Mendil", "Tuvalet Kağıdı", "Sabun", "Dezenfektan",
            "El Feneri", "Pil", "Powerbank", "Aydınlatma Kulesi",
            "Arama Kurtarma Uzmanı", "Sağlık Personeli (Paramedik)", "Çevirmen", "Gönüllü (Lojistik)", "Psikososyal Destek Ekibi",
            "Ekskavatör", "Vinç", "Ambulans", "İtfaiye Arazözü", "Kamyon", "Diğer"
        ]

        # Arama/Öneri sistemi için tüm veriler Trie yapısına indekslenir.
        for veri in self.tum_ekipler + list(self.musait_araclar) + kategoriler + gercekci_ogeler:
            self.arama_trie.ekle(veri)

        # Depolara sadece "Malzeme" olanları (Araç ve Personeller hariç) kendi kategorileriyle ekliyoruz
        malzeme_listesi = [
            ("Hilti", "Arama Kurtarma Ekipmanı"), ("Termal Kamera", "Arama Kurtarma Ekipmanı"), 
            ("Enkaz Dinleme Cihazı", "Arama Kurtarma Ekipmanı"), ("Demir Kesme Makası", "Arama Kurtarma Ekipmanı"),
            ("Jeneratör", "Lojistik ve Enerji"), ("El Feneri", "Lojistik ve Enerji"), 
            ("Pil", "Lojistik ve Enerji"), ("Powerbank", "Lojistik ve Enerji"), ("Aydınlatma Kulesi", "Lojistik ve Enerji"),
            ("Çadır (Kışlık)", "Barınma"), ("Konteyner", "Barınma"), ("Uyku Tulumu", "Barınma"), 
            ("Isıtıcı (Elektrikli)", "Barınma"), ("Isıtıcı (Tüplü)", "Barınma"), ("Battaniye", "Barınma"), ("Mat", "Barınma"),
            ("Su (5 Lt)", "Gıda ve Su"), ("Konserve Gıda", "Gıda ve Su"), ("Bebek Maması", "Gıda ve Su"), 
            ("Bebek Bisküvisi", "Gıda ve Su"), ("Ekmek", "Gıda ve Su"),
            ("İlk Yardım Çantası", "Sağlık ve İlk Yardım"), ("Sargı Bezi", "Sağlık ve İlk Yardım"), 
            ("Ağrı Kesici", "Sağlık ve İlk Yardım"), ("Turnike", "Sağlık ve İlk Yardım"), ("Sedye", "Sağlık ve İlk Yardım"),
            ("Bebek Bezi", "Hijyen"), ("Kadın Pedi", "Hijyen"), ("Islak Mendil", "Hijyen"), 
            ("Tuvalet Kağıdı", "Hijyen"), ("Sabun", "Hijyen"), ("Dezenfektan", "Hijyen")
        ]

        # Her malzemenin en az bir depoda bolca (2000 adet) olmasını sağlıyoruz
        for i, (ad, kat) in enumerate(malzeme_listesi):
            depo_index = (i % 4) + 1
            depo_adi = f"Depo {depo_index}"
            self.depo_envanterleri[depo_adi].ekle(Urun(i, ad, kat, 2000))
            
            # Diğer depolara da az miktarda (çeşitlilik için) ekleyelim
            for d in self.depolar:
                if d != depo_adi:
                    self.depo_envanterleri[d].ekle(Urun(i, ad, kat, 50))

        # Graf düğümleri (Depolar ve Enkazlar) oluşturulur.
        # 4 Depo ve 7 Enkaz bölgesi 
        enkazlar = [f"Enkaz {i}" for i in range(1, 8)] 
        self.sehir_grafi.add_nodes_from(self.depolar + enkazlar)
        
        # Gerçekçi ve geniş alana yayılmış mesafe (ağırlık) ağları
        self.sehir_grafi.add_weighted_edges_from([
            ("Depo 1", "Enkaz 1", 4), ("Depo 1", "Enkaz 2", 7), ("Depo 1", "Enkaz 3", 12),
            ("Depo 2", "Enkaz 3", 5), ("Depo 2", "Enkaz 4", 6), 
            ("Depo 3", "Enkaz 5", 8), ("Depo 3", "Enkaz 7", 9), 
            ("Depo 4", "Enkaz 6", 3), ("Depo 4", "Enkaz 7", 5), ("Depo 4", "Enkaz 2", 14),
            ("Enkaz 1", "Enkaz 3", 2), ("Enkaz 2", "Enkaz 4", 3), ("Enkaz 3", "Enkaz 5", 4),
            ("Enkaz 5", "Enkaz 6", 2), ("Enkaz 6", "Enkaz 7", 4), ("Enkaz 7", "Enkaz 1", 10)
        ])

        # Başlangıç görevleri Hash Table üzerinde ilklendirilir.
        self.gorev_yonetimi = {
            "G01": Gorev("G01", "Arama Kurtarma", "Enkaz 1 incelemesi ve ses dinleme", "Bekliyor", "Arama-Kurtarma", 3),
            "G02": Gorev("G02", "Sağlık Müdahalesi", "Enkaz 2'de yaralılara ilk yardım", "Bekliyor", "Sağlık/Tıp", 2),
            "G03": Gorev("G03", "Çadır Kurulumu", "Enkaz 3 bölgesinde geçici barınma kurulumu", "Bekliyor", "Lojistik", 4),
            "G04": Gorev("G04", "Erzak Dağıtımı", "Depo 1'den Enkaz 4'e erzak dağıtımı", "Bekliyor", "Mutfak/Gıda", 2),
            "G05": Gorev("G05", "Psikolojik Destek", "Enkaz 5 toplanma alanında destek", "Bekliyor", "Psikososyal Destek", 1),
            "G06": Gorev("G06", "Arama Kurtarma", "Enkaz 6 ağır yıkım bölgesi tespiti", "Bekliyor", "Arama-Kurtarma", 4)
        }

        # Kuyruk yapısına (FIFO) örnek gönüllü verileri eklenir (20 adet).
        import random
        from modeller import Gonullu
        isimler = ["Ahmet Yılmaz", "Ayşe Demir", "Mehmet Kaya", "Fatma Çelik", "Ali Şahin", "Zeynep Öztürk", "Mustafa Arslan", "Elif Yıldız", "Hasan Gökgöz", "Senanur Uluman",
                   "Kemal Aydın", "Selin Polat", "Beyzanur Topcu", "Cansu Öz", "Oğuzhan Tekin", "Büşra Çetin", "Caner Gök", "Deniz Kurt", "Emre Karaca", "Ebru Aslan"]
        uzmanliklar = ["Arama-Kurtarma", "Sağlık/Tıp", "Lojistik", "Psikososyal Destek", "Mutfak/Gıda"]
        
        for i, isim in enumerate(isimler):
            uzm = random.choice(uzmanliklar)
            # Arama kurtarma daha sık olsun
            if i % 3 == 0: uzm = "Arama-Kurtarma"
            if i % 4 == 0: uzm = "Sağlık/Tıp"
            self.gonullu_siraya_al(Gonullu(f"TC{1000+i}", isim, uzm))

        # Sabit diziye yedek araçlar atanır.
        self.arac_filosu.eleman_ata(0, "Ambulans-Yedek")
        self.arac_filosu.eleman_ata(1, "İtfaiye-Yedek")

        self.log_ekle("Sistem başlatıldı. Gerçekçi afet verileri ve çoklu depolar yüklendi.")

    def durumlari_guncelle(self):
        # Birimlerin görev ve dinlenme (Cooldown) süreleri simüle edilir.
        simdi = time.time()
        donenler = []
        for birim, info in list(self.mesgul_birimler.items()):
            if simdi >= info["bitis"]:
                if info["durum"] == "Görevde":
                    # Durum geçişi: Görev biter, Cooldown (bekleme) başlar.
                    self.mesgul_birimler[birim] = {"durum": "Cooldown", "bitis": simdi + 10}
                    donenler.append(birim)
                    self.log_ekle(f"DURUM GÜNCELLEME: {birim} görevden döndü, Cooldown (Bakım/Dinlenme) aşamasında.")
                elif info["durum"] == "Cooldown":
                    # Dinlenme biter, birim müsait havuzuna geri döner.
                    if "Ambulans" in birim or "İtfaiye" in birim or "Makine" in birim or "Vinç" in birim or "Ekskavatör" in birim:
                        self.musait_araclar.add(birim)
                    else:
                        self.musait_ekipler.add(birim)
                    del self.mesgul_birimler[birim]
                    donenler.append(birim)
                    self.log_ekle(f"DURUM GÜNCELLEME: {birim} Cooldown'u bitirdi, tekrar MÜSAİT duruma geçti.")
        return donenler

    def ekip_talep_ekle(self, ekip_adi, adres, kategori, ihtiyac_adi, miktar, manuel_oncelik=None, kaynak_depo=""):
        # Öncelik seviyeleri atanarak Heap yapısının sıralama mantığı belirlenir.
        if manuel_oncelik:
            priority = manuel_oncelik
        else:
            oncelik_haritasi = {
                "Arama Kurtarma Ekipmanı": 1,
                "Sağlık ve İlk Yardım": 1,
                "Araç/İş Makinesi": 1,
                "Gıda ve Su": 2,
                "Barınma": 2,
                "Personel/Gönüllü": 2,
                "Lojistik ve Enerji": 3,
                "Hijyen": 3,
                "Diğer Kategori": 4
            }
            priority = oncelik_haritasi.get(kategori, 5)

        t_id = f"TLP-{self._sayac}"

        talep = EkipTalebi(priority, t_id, ekip_adi, adres, kategori, ihtiyac_adi, miktar, "Bekliyor", kaynak_depo)
        # Priority Queue (Heap): O(log N) maliyetle talebi öncelik sırasına göre ekler.
        heapq.heappush(self.ekip_talepleri_heap, talep)
        # Geri alma işlemi için talep Stack hafızasına kopyalanır.
        self.islem_gecmisi_talepler.append(talep)
            
        self.log_ekle(f"TALEPLER GÜNCELLENDİ: {ekip_adi} (Öncelik: {priority}) -> {ihtiyac_adi}")
        self._sayac += 1

    def talep_geri_al(self):
        # LIFO prensibi: Stack'ten son talebi çekip Heap'ten temizler.
        if not self.islem_gecmisi_talepler: return False, "Geri alınacak talep yok."
        son_talep = self.islem_gecmisi_talepler.pop()
        if son_talep in self.ekip_talepleri_heap:
            self.ekip_talepleri_heap.remove(son_talep)
            # Heap invariant (özelliği) bozulduğu için yeniden düzenlenir (O(N)).
            heapq.heapify(self.ekip_talepleri_heap)
            self.log_ekle(f"GERİ ALINDI: {son_talep.talep_id} silindi.")
            return True, "Son talep başarıyla geri alındı."
        return False, "Talep zaten işleme alınmış veya bulunamadı."

    def talep_karsila(self, talep_id, secilen_depo=None):
        if not self.ekip_talepleri_heap: return False, "Bekleyen talep yok."

        # Seçilen talep Heap listesinde O(N) sürede aranır.
        secilen_talep = None
        for t in self.ekip_talepleri_heap:
            if t.talep_id == talep_id:
                secilen_talep = t
                break
                
        if not secilen_talep:
            return False, "Talep bulunamadı."

        malzeme_kategorileri = ["Arama Kurtarma Ekipmanı", "Barınma", "Gıda ve Su", "Sağlık ve İlk Yardım", "Hijyen", "Lojistik ve Enerji", "Malzeme"]
        
        if secilen_talep.kategori in malzeme_kategorileri:
            if not secilen_depo: secilen_depo = "Depo 1"

            # BST Araması: O(log N) sürede ilgili depodaki ürünün stok kontrolünü yapar.
            dugum = self.depo_envanterleri[secilen_depo]._dugum_bul(self.depo_envanterleri[secilen_depo].kok, secilen_talep.ihtiyac_adi)
            stok_miktari = dugum.urun.miktar if dugum else 0

            if stok_miktari < secilen_talep.miktar:
                # Stok yetersizse dış tedarikçiden veri çekme (Simülasyon).
                import random
                tedarikci = random.choice(self.tedarikciler)
                eksik = secilen_talep.miktar - stok_miktari + 100 # İhtiyaçtan biraz fazla isteyelim
                self.log_ekle(f"STOK YETERSİZ: {secilen_depo} için {tedarikci} üzerinden {eksik} adet {secilen_talep.ihtiyac_adi} tedarik edildi.")
                
                # Tedarikçiden gelen malı depoya ekle
                if not dugum:
                    self.depo_envanterleri[secilen_depo].ekle(Urun(999, secilen_talep.ihtiyac_adi, secilen_talep.kategori, eksik))
                else:
                    dugum.urun.miktar += eksik

            # Artık stok kesin var, sevkiyat yapabiliriz
            self.depo_envanterleri[secilen_depo].miktar_azalt(secilen_talep.ihtiyac_adi, secilen_talep.miktar)
            mesaj = f"{secilen_depo}'dan {secilen_talep.miktar} adet {secilen_talep.ihtiyac_adi} sevk edildi."
            self.log_ekle(f"KARŞILANDI: {secilen_talep.talep_id} ({secilen_talep.ihtiyac_adi})")

            # Heap'ten eleman çıkarılır ve yapı korunur.
            self.ekip_talepleri_heap.remove(secilen_talep)
            heapq.heapify(self.ekip_talepleri_heap)
            
            return True, mesaj
            
        elif secilen_talep.kategori == "Personel/Gönüllü":
            # Gönüllü taleplerini karşıla
            eslesme = {
                "Arama Kurtarma Uzmanı": "Arama-Kurtarma",
                "Sağlık Personeli (Paramedik)": "Sağlık/Tıp",
                "Gönüllü (Lojistik)": "Lojistik",
                "Psikososyal Destek Ekibi": "Psikososyal Destek",
                "Çevirmen": "Arama-Kurtarma" # veya farklı bir yaklaşım
            }
            uzmanlik = eslesme.get(secilen_talep.ihtiyac_adi, "Arama-Kurtarma")
            kuyruk = self.gonullu_kuyruklari.get(uzmanlik)

            # FIFO (İlk Gelen İlk Çıkar): Sıradaki gönüllüler sahaya atanır.
            if kuyruk and kuyruk.boyut() >= secilen_talep.miktar:
                atananlar = [kuyruk.dequeue() for _ in range(secilen_talep.miktar)]
                isimler = ", ".join([g.ad_soyad for g in atananlar])
                self.ekip_talepleri_heap.remove(secilen_talep)
                heapq.heapify(self.ekip_talepleri_heap)
                mesaj = f"{secilen_talep.miktar} kişi görevlendirildi: {isimler}"
                self.log_ekle(f"KARŞILANDI: {secilen_talep.talep_id} ({secilen_talep.ihtiyac_adi}) -> {isimler}")
                return True, mesaj
            else:
                return False, f"Yeterli '{uzmanlik}' gönüllüsü yok! (İstenen: {secilen_talep.miktar})"

        else:
            # Araç atama: Müsait havuzundan çıkarılıp meşgul (Görevde) listesine eklenir.
             if secilen_depo and secilen_depo in self.musait_araclar:
                 self.musait_araclar.remove(secilen_depo)
                 # 15 saniye görev süresi
                 self.mesgul_birimler[secilen_depo] = {"durum": "Görevde", "bitis": time.time() + 15}
                 mesaj = f"{secilen_depo} yönlendirildi."
                 self.log_ekle(f"KARŞILANDI: {secilen_talep.talep_id} ({secilen_talep.ihtiyac_adi}) -> {secilen_depo}")
             else:
                 mesaj = f"{secilen_talep.ihtiyac_adi} yönlendirildi (belirli araç seçilmedi)."
                 self.log_ekle(f"KARŞILANDI: {secilen_talep.talep_id} ({secilen_talep.ihtiyac_adi})")
                 
             self.ekip_talepleri_heap.remove(secilen_talep)
             heapq.heapify(self.ekip_talepleri_heap)
             return True, mesaj

    def gorev_tamamla(self, gorev_id):
        # ID üzerinden Hash Table erişimi: O(1).
        if gorev_id in self.gorev_yonetimi:
            gorev = self.gorev_yonetimi[gorev_id]
            if gorev.durum == "Tamamlandı": return False, "Bu görev zaten tamamlandı."
            
            # Gönüllü eşleştirme (Strict FIFO)
            gereken_uzmanlik = gorev.gereken_uzmanlik
            kisi_sayisi = gorev.kisi_sayisi
            
            kuyruk = self.gonullu_kuyruklari.get(gereken_uzmanlik)

            # Queue: Görev için gereken kişi sayısı kadar dequeue yapılır.
            if kuyruk and kuyruk.boyut() >= kisi_sayisi:
                atananlar = [kuyruk.dequeue() for _ in range(kisi_sayisi)]
                gorev.durum = "Tamamlandı"
                # Yapılan işlemi Stack'e pushlayarak geri alınabilir (Undo) kılar.
                self.islem_gecmisi_yigini.push(gorev_id) 
                isimler = ", ".join([g.ad_soyad for g in atananlar])
                gorev.atanan_kisiler = isimler
                self.log_ekle(f"GÖREV ATANDI: {gorev_id} -> Gönderilenler: {isimler}")
                return True, f"Görev başladı! Atanan kişiler: {isimler}"
            else:
                mevcut = kuyruk.boyut() if kuyruk else 0
                self.log_ekle(f"GÖREV İPTAL: {gorev_id} için {gereken_uzmanlik} eksik. (İstenen: {kisi_sayisi}, Mevcut: {mevcut})")
                return False, f"Kuyrukta yeterli sayıda '{gereken_uzmanlik}' uzmanlığına sahip gönüllü yok!"

    def gorev_geri_al(self):
        # Stack (Undo): Son tamamlanan görevin durumunu 'Bekliyor'a geri çeker.
        gorev_id = self.islem_gecmisi_yigini.pop()
        if gorev_id:
            self.gorev_yonetimi[gorev_id].durum = "Bekliyor"
            self.gorev_yonetimi[gorev_id].atanan_kisiler = ""
            self.log_ekle(f"UNDO: {gorev_id} tekrar beklemede (Gönüllüler geri alınmadı).")

    def gonullu_siraya_al(self, gonullu_obj):
        # Kategoriye göre ilgili kuyruğa O(1) maliyetle ekleme yapar.
        kuyruk = self.gonullu_kuyruklari.get(gonullu_obj.kategori)
        if kuyruk is not None:
            kuyruk.enqueue(gonullu_obj)
            self.log_ekle(f"Gönüllü Kuyruğa Girdi ({gonullu_obj.kategori}): {gonullu_obj.ad_soyad}")
        else:
            self.log_ekle(f"Geçersiz gönüllü kategorisi: {gonullu_obj.kategori}")

    def gonullu_sahaya_gonder(self, kategori):
        # Kuyruğun başındaki gönüllüyü çeker (FIFO).
        kuyruk = self.gonullu_kuyruklari.get(kategori)
        if kuyruk and not kuyruk.bos_mu():
            kisi = kuyruk.dequeue()
            self.log_ekle(f"Kuyruktan Çıktı ({kategori}): {kisi.ad_soyad}")
            return kisi
        return None

    def rota_hesapla(self, baslangic, bitis):
        try:
            # Dijkstra Algoritması: Graf üzerindeki en kısa yolu hesaplar.
            yol = nx.dijkstra_path(self.sehir_grafi, baslangic, bitis, weight='weight')
            mesafe = nx.dijkstra_path_length(self.sehir_grafi, baslangic, bitis, weight='weight')
            self.log_ekle(f"Rota Bulundu: {' -> '.join(yol)}")
            return yol, mesafe
        except nx.NetworkXNoPath:
            return None, -1

    def log_ekle(self, mesaj: str):
        # Bağlı Liste (Linked List): Başa ekleme yaparak geçmişi kronolojik tutar (O(1)).
        zaman = datetime.now().strftime("%H:%M:%S")
        self.mudahale_gecmisi.basa_ekle(MudahaleLog(self._sayac, mesaj, zaman))

    def uygun_depolari_bul(self, enkaz_adi, kategori, ihtiyac_adi, miktar):
        malzeme_kategorileri = ["Arama Kurtarma Ekipmanı", "Barınma", "Gıda ve Su", "Sağlık ve İlk Yardım", "Hijyen", "Lojistik ve Enerji", "Malzeme"]
        uygunlar = []
        for depo in self.depolar:
            urun_var_mi = False
            if kategori in malzeme_kategorileri:
                # BST Araması (O(log N)): İlgili depoda ürün ve stok miktarını doğrular.
                dugum = self.depo_envanterleri[depo]._dugum_bul(self.depo_envanterleri[depo].kok, ihtiyac_adi)
                if dugum and dugum.urun.miktar >= miktar:
                    urun_var_mi = True
            else:
                urun_var_mi = True # Araç/Personel ise mesafe olarak tüm depolar listelenebilir
                
            if urun_var_mi:
                try:
                    # Mesafe ölçümü: Dijkstra maliyeti hesaplanır.
                    mesafe = nx.dijkstra_path_length(self.sehir_grafi, depo, enkaz_adi, weight='weight')
                    uygunlar.append((depo, mesafe))
                except nx.NetworkXNoPath: pass
                
        # Mevcut uygun depoları mesafeye göre küçükten büyüğe sıralar ve döndürür.
        return sorted(uygunlar, key=lambda x: x[1])
    
    def envantere_yeni_urun_ekle(self, depo_adi, urun_obj):
        # BST Ekleme: Yeni ürünü ilgili deponun ağacına yerleştirir.
        self.depo_envanterleri[depo_adi].ekle(urun_obj)
        self.log_ekle(f"ENVANTER: {depo_adi} deponuna yeni ürün eklendi: {urun_obj.ad}")

    def envanterden_urun_sil(self, depo_adi, urun_adi):
        # BST Silme: Ürünü ilgili depodan hiyerarşiyi bozmadan temizler.
        self.depo_envanterleri[depo_adi].sil(urun_adi)
        self.log_ekle(f"ENVANTER: {depo_adi} deponundan ürün silindi: {urun_adi}")