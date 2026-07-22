import time

class PerformansAnalizi:
    """
        Hash ve Liste yapılarının CRUD operasyon hızlarını karşılaştırır.
        CRUD: Create (Ekleme), Read (Arama/Okuma), Update (Güncelleme), Delete (Silme).
    """

    @staticmethod
    def crud_testi_ciz(fig):
        # Farklı veri boyutları üzerinde test yaparak büyüme hızını gözlemler (Big O Analizi)
        boyutlar = [1000, 5000, 10000, 20000]
        hash_ekle, list_ekle = [], []
        hash_ara, list_ara = [], []
        hash_sil, list_sil = [], []
        
        for boyut in boyutlar:
            test_dict = {}
            test_list = []
            
            # 1. EKLEME TESTİ
            # Hash Table (Dict) için ekleme O(1) sabit zamanlıdır.
            b = time.perf_counter()
            for i in range(boyut): test_dict[f"ID{i}"] = i
            hash_ekle.append(time.perf_counter() - b)

            # List için ekleme O(1) amortized olsa da, büyük verilerde yeniden boyutlandırma maliyeti oluşur.
            b = time.perf_counter()
            for i in range(boyut): test_list.append(f"ID{i}")
            list_ekle.append(time.perf_counter() - b)

            # En kötü durum senaryosu (Worst Case) için listenin en sonundaki eleman aranır.
            aranan = f"ID{boyut-1}" # Worst Case
            
            # 2. ARAMA TESTİ
            # Hash Table arama: O(1) - Anahtar (Key) üzerinden direkt erişim sağlar.
            b = time.perf_counter()
            _ = test_dict.get(aranan)
            hash_ara.append(time.perf_counter() - b)

            # List arama: O(N) - Elemanı bulana kadar tüm listeyi tek tek tarar.
            b = time.perf_counter()
            _ = aranan in test_list
            list_ara.append(time.perf_counter() - b)
            
            # 3. SİLME TESTİ
            # Hash Table silme: O(1) sabit zamanlı.
            b = time.perf_counter()
            del test_dict[aranan]
            hash_sil.append(time.perf_counter() - b)

            # List silme: O(N) - Eleman silindikten sonra diğer elemanların kaydırılması (shifting) gerekir.
            b = time.perf_counter()
            test_list.remove(aranan) # O(N) Maliyeti
            list_sil.append(time.perf_counter() - b)

        # Matplotlib ile verilerin görselleştirilmesi süreci
        fig.clear()

        # Ekleme Grafiği: O(1) vs O(N) farkının görsel kanıtı
        ax1 = fig.add_subplot(131)
        ax1.plot(boyutlar, hash_ekle, 'g-o', label='Hash O(1)')
        ax1.plot(boyutlar, list_ekle, 'r-x', label='List O(N)')
        ax1.set_title("Ekleme Süresi", color="white")
        ax1.tick_params(colors='white')
        ax1.legend()

        # Arama Grafiği: Veri miktarı arttıkça Hash'in sabit kaldığı, List'in ise lineer arttığı gözlemlenir.
        ax2 = fig.add_subplot(132)
        ax2.plot(boyutlar, hash_ara, 'g-o', label='Hash O(1)')
        ax2.plot(boyutlar, list_ara, 'r-x', label='List O(N)')
        ax2.set_title("Arama Süresi", color="white")
        ax2.tick_params(colors='white')
        ax2.legend()

        # Silme Grafiği
        ax3 = fig.add_subplot(133)
        ax3.plot(boyutlar, hash_sil, 'g-o', label='Hash O(1)')
        ax3.plot(boyutlar, list_sil, 'r-x', label='List O(N)')
        ax3.set_title("Silme Süresi", color="white")
        ax3.tick_params(colors='white')
        ax3.legend()

        # Modern UI için grafik renk ayarları
        fig.patch.set_facecolor('#1e1e2e')
        for ax in [ax1, ax2, ax3]: ax.set_facecolor('#313244')
        
        fig.tight_layout()