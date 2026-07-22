from dataclasses import dataclass, field

# @dataclass(order=True) ifadesi, nesnelerin karşılaştırılabilir olmasını sağlar.
# Heap (Öncelikli Kuyruk) yapısında 'priority' alanına göre otomatik sıralama yapılmasına olanak tanır.
@dataclass(order=True)
class EkipTalebi:
    priority: int  # Heap sıralaması için ana kriterdir (1: En öncelikli - Kritik).
    talep_id: str = field(compare=False) # Sıralama işlemlerinde dikkate alınmaz.
    ekip_adi: str = field(compare=False)
    adres: str = field(compare=False)
    kategori: str = field(compare=False)
    ihtiyac_adi: str = field(compare=False)
    miktar: int = field(compare=False)
    durum: str = field(compare=False) # Bekliyor, Karşılandı vb.
    kaynak_depo: str = field(compare=False, default="") 

# BST (İkili Arama Ağacı) içerisinde saklanacak temel ürün modeli.
# BST üzerinde düğümler (nodes) bu sınıfın nesnelerini taşır.
@dataclass
class Urun:
    urun_id: int
    ad: str # BST'de sıralama ve arama bu alan üzerinden (alfabetik) yapılır.
    kategori: str
    miktar: int

# Linked List (Bağlı Liste) yapısında her bir düğümün (node) verisini temsil eder.
@dataclass
class MudahaleLog:
    log_id: int
    mesaj: str
    zaman_damgasi: str # İşlem geçmişinin kronolojik takibi için kullanılır.

# Görev yönetimi ve Stack (Yığın) tabanlı 'Undo' işlemleri için kullanılan model.
@dataclass
class Gorev:
    gorev_id: str
    baslik: str
    aciklama: str
    durum: str # Bekliyor, Tamamlandı.
    gereken_uzmanlik: str = ""
    kisi_sayisi: int = 1
    atanan_kisiler: str = ""

# Kuyruk (Queue - FIFO) yapısında bekletilecek gönüllü verilerini temsil eder.
@dataclass
class Gonullu:
    kimlik: str
    ad_soyad: str
    kategori: str # Uzmanlık alanına göre ilgili kuyruğa (Queue) yönlendirilir.