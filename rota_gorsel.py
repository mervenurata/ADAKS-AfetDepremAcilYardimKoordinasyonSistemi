import networkx as nx

class RotaGorsellestirici:
    """
        Graf veri yapısını Matplotlib ve PyQt5 bileşenleri üzerine çizen görselleştirme modülüdür.
        Düğümleri (noktalar) ve kenarları (yollar) koordinat sistemine yerleştirir.
    """
    
    @staticmethod
    def harita_ciz(graf, ax, yol=None):
        # Önceki çizimleri temizleyerek üst üste binmeyi önler.
        ax.clear()

        # Düğümlerin ekrandaki yerleşim düzenini (layout) belirler.
        # 'spring_layout' düğümleri birbirini iten noktalar gibi dengeli dağıtır.
        pos = nx.spring_layout(graf, seed=42, k=2.0)
        
        # Düğüm renklerini ayarlar: Depolar için mavi, Afet (Enkaz) bölgeleri için kırmızı
        renk_haritasi = []
        cizgi_renkleri = []
        for dugum in graf.nodes:
            if "Depo" in dugum:
                renk_haritasi.append("#3b82f6") # Profesyonel Mavi
                cizgi_renkleri.append("#1e3a8a") # Koyu Mavi Çerçeve
            else:
                renk_haritasi.append("#ef4444") # Profesyonel Kırmızı
                cizgi_renkleri.append("#7f1d1d") # Koyu Kırmızı Çerçeve

        # Düğümleri (Şehirdeki önemli noktalar) kanvasa çizer.
        # 'set_picker' özelliği, harita üzerindeki noktalara tıklanabilirlik sağlar.
        dugumler = nx.draw_networkx_nodes(graf, pos, ax=ax, node_color=renk_haritasi, node_size=2500, edgecolors=cizgi_renkleri, linewidths=2.5)
        dugumler.set_picker(5)

        # Düğüm isimlerini (Depo 1, Enkaz 2 vb.) düğümlerin üzerine yazar.
        nx.draw_networkx_labels(graf, pos, ax=ax, font_color="#11111b", font_weight="bold", font_size=11)

        # Kenar (Yol) Çizimi:
        # Eğer Dijkstra algoritmasından bir rota (yol) gelmişse, bu rotayı vurgular.
        if yol:
            # Algoritmanın bulduğu rotadaki ardışık düğümleri çiftler (A-B, B-C).
            yol_kenarlari = list(zip(yol, yol[1:]))

            # Tüm yolları arka planda hafif (silik) çizer.
            nx.draw_networkx_edges(graf, pos, ax=ax, edge_color="#45475a", alpha=0.3, width=1)

            # Algoritmanın belirlediği en kısa yolu belirgin bir renkle vurgular.
            nx.draw_networkx_edges(graf, pos, ax=ax, edgelist=yol_kenarlari, edge_color="#f38ba8", width=4)
        else:
            # Rota seçilmemişse tüm yolları standart kalınlıkta gösterir.
            nx.draw_networkx_edges(graf, pos, ax=ax, edge_color="#94A3B8", width=2)

        # Yolların üzerindeki ağırlıkları (mesafe/zaman maliyeti) gösterir.
        edge_labels = nx.get_edge_attributes(graf, 'weight')
        nx.draw_networkx_edge_labels(graf, pos, edge_labels=edge_labels, ax=ax, font_color="#1E3A8A", font_weight="bold", font_size=10)

        # Harita eksenlerini (x-y çizgileri) gizleyerek daha temiz bir görünüm sağlar.
        ax.axis('off')