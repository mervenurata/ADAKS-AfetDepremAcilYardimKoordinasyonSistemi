import sys
from PyQt5.QtWidgets import QApplication
from ana_pencere import AnaPencere

def main():
    """
        Uygulamanın ana giriş noktası (Entry Point).
        Sistem kaynaklarını hazırlar ve GUI döngüsünü başlatır.
    """
    # Uygulamanın kontrol akışını yöneten ana nesne oluşturulur.
    app = QApplication(sys.argv)

    # Farklı işletim sistemlerinde standart arayüz görünümü sağlar.
    app.setStyle("Fusion")

    # Veri yapılarının (Trie, BST, Graph) ilklendirildiği ana pencere başlatılır.
    pencere = AnaPencere()
    pencere.show()

    # O(1) Başlatma: Uygulama döngüsüne girilir ve çıkış kodu sisteme iletilir.
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()