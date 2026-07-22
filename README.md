# 🚨 ADAKS - Afet ve Deprem Acil Yardım Koordinasyon Sistemi

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt/Tkinter](https://img.shields.io/badge/GUI-Desktop-blue?style=for-the-badge)
![Data Structures](https://img.shields.io/badge/Focus-Data_Structures_%26_Algorithms-orange?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Completed-success?style=for-the-badge)

## 📌 Projenin Amacı
**ADAKS (Afet ve Deprem Acil Yardım Koordinasyon Sistemi)**; doğal afetler ve acil durumlar anında kritik kaynakların, lojistik ağların, gönüllü yönetiminin ve arama-kurtarma ekiplerinin en verimli şekilde koordine edilmesini sağlamak amacıyla geliştirilmiş kapsamlı bir masaüstü uygulamasıdır. 

Sistem, karmaşık kriz anlarında insan hatasını en aza indirmeyi, sınırlı kaynakları en çok ihtiyaç duyulan bölgelere hızlıca ulaştırmayı ve saha operasyonlarını veriye dayalı, analitik bir şekilde yönetmeyi hedefler.

---

## ⚙️ Nasıl Çalışır?
Sistem, arka planda çalışan gelişmiş veri yapıları ve algoritmalar sayesinde sahadan gelen ihbarları toplar, önceliklendirir ve merkez depolar ile enkaz bölgeleri arasındaki en optimal ağ bağlantılarını kurar.

Kullanıcı arayüzü ana olarak **5 sekmeden** oluşur:
1. **Saha İhbar Formu:** Sahadaki ekiplerin ihtiyaçlarını ve durumlarını sisteme hızlıca girdiği, otomatik tamamlama destekli form alanıdır.
2. **Lojistik ve Tedarik:** Merkez depoların anlık stok durumlarını ve tedarikçi zincirlerini yöneten, azalan stokları gösteren paneldir.
3. **Harita ve İhtiyaçlar:** Şehirdeki mevcut enkaz bölgeleri ve depolar arasındaki bağlantıyı interaktif bir graf üzerinde gösteren, en kısa yol algoritmasını çalıştırarak araçları ve malzemeleri sevk eden sistemdir.
4. **Görev ve Gönüllü Yönetimi:** Sisteme kayıtlı gönüllülerin uzmanlık alanlarına göre kuyruğa alındığı ve sahadaki spesifik görevlere atandığı modüldür.
5. **Raporlama:** Gerçekleşmiş tüm işlemlerin, sevkiyatların ve geri alınan adımların zaman damgalı log kayıtlarının tutulduğu yönetici ekranıdır.

---

## 🚀 Temel Özellikler
- 🗺️ **Dinamik Harita Görselleştirme:** Depolar ve enkazlar arası yol ağını, mesafeleriyle birlikte gerçek zamanlı gösterir ve sevk edilen aracın rotasını çizer.
- 🎯 **Akıllı En Yakın Depo Seçimi:** Bir enkaz bölgesi için malzeme talebi karşılanmak istendiğinde, sistem yalnızca elinde stok bulunan depoları tarar ve enkaza en kısa sürede ulaşabilecek depoyu otomatik atayarak rotayı çizer.
- 🚑 **Araç Durum Takibi:** Göreve gönderilen araçlar (Ambulans, İtfaiye, İş Makinesi vb.) listeden düşerek "Görevde" statüsüne geçer, belirli bir süre sonra bakım aşamasına (*Cooldown*) girer ve ardından tekrar müsait hale gelir.
- 👥 **Uzmanlık Bazlı Gönüllü Ataması:** Oluşturulan görevlerin gerektirdiği uzmanlık tipine göre (örneğin Sağlık/Tıp), o alanda kayıtlı gönüllüler sırasıyla (*ilk gelen ilk çıkar*) göreve atanır.
- ↩️ **Geri Alma (Undo) Sistemi:** Yapılan görev atamalarının ve operasyonların hatalı olması durumunda işlemi son yapılandan başlayarak geri alma imkanı sunar.
- 🔍 **Hızlı Arama ve Filtreleme:** On binlerce satır malzeme listesi arasında anında arama yapabilen otomatik tamamlama filtresi bulunur.

---

## 🧬 Kullanılan Veri Yapıları ve Algoritmalar

Sistem performansını ve ölçeklenebilirliğini artırmak amacıyla modern bilgisayar bilimleri veri yapıları entegre edilmiştir:

* 🌐 **Graf (Graph) & Dijkstra Algoritması:** Şehir haritası bir ağ (Network) olarak modellenmiştir. Düğümler (*Nodes*) depoları ve enkazları, kenarlar (*Edges*) ise yolları temsil eder. Malzeme sevkinde en az maliyetli/mesafeli rotayı bulur.
* ⚡ **Öncelik Kuyruğu (Priority Queue / Max-Heap):** Sahadan gelen ihbarlar geliş zamanına göre değil, *Kritiklik Seviyesine* göre işlenir. En acil talepler her zaman listenin en başına alınır.
* 🌲 **İkili Arama Ağacı (Binary Search Tree - BST):** Lojistik depolarındaki binlerce farklı tür ürünün envanter takibi ve stok arama işlemleri $O(\log N)$ karmaşıklığında gerçekleştirilir.
* 🔤 **Ön Ek Ağacı (Trie):** İhbar formunda malzeme girilirken çalışan kelime tamamlama (*Autocomplete*) özelliği Trie yapısı üzerine inşa edilmiştir.
* 📥 **Kuyruk (Queue - FIFO):** Gönüllü yönetimi ve saha ekiplerinin sıralanması, uzmanlık alanlarına göre bağımsız kuyruklar üzerinden yürütülür.
* 📤 **Yığın (Stack - LIFO):** Son yapılan yönetimsel kararları hafızada tutarak "Geri Al" (*Undo*) işlevini sağlar.
* 🗂️ **Hash Haritaları (Dictionaries/Sets):** Birim durumlarını, araç filosunu ve logları $O(1)$ zaman karmaşıklığı ile anlık sorgulamak için kullanılır.



