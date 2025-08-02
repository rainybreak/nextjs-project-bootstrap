# 🏨 Otel Yönetim Sistemi (Hotel Management System)

Modern bir otel yönetim sistemi - Python ve PyQt5 kullanılarak geliştirilmiştir.

## 📋 Özellikler

### 🔧 Teknik Servis Menüsü
- **Arıza Yönetim Arayüzü**
  - Bekleyen arızaları listele
  - Yeni arıza bildirimi
  - Tüm arızaları görüntüle
  - Arıza detaylarını görüntüle (çift tıklama ile)
  - Arıza durumu güncelleme (Bekleniyor, Çözüldü, Çözülemedi)

**Arıza Bilgileri:**
- Tarih
- Oda Numarası
- Bildiren (F/O, HK, F&B, Animasyon, Diğer)
- Arıza Açıklaması
- Arıza Durumu

### 🍽️ F&B Menüsü

#### Vardiya Yönetim Arayüzü
- Çalışan personel listesi
- İzinli personel listesi
- Günlük örtü rengi seçimi
- Vardiya bilgilerini kaydetme

#### Özel Servis Yönetim Arayüzü
- Günlük özel servis istekleri
- Yeni özel servis ekleme
- Servis durumu takibi

#### Menü Yönetim Arayüzü
- Günlük yemek menüsü (değiştirilebilir)
- Kokteyl tarifleri (sabit)
- Menü güncelleme

## 🚀 Kurulum

### Gereksinimler
- Python 3.7 veya üzeri
- PyQt5

### Adım 1: Projeyi İndirin
```bash
# Proje klasörünü bilgisayarınıza kopyalayın
cd hotel_management_system
```

### Adım 2: Gerekli Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Uygulamayı Çalıştırın
```bash
python main.py
```

## 🗄️ Veritabanı

Uygulama SQLite veritabanı kullanır. İlk çalıştırmada otomatik olarak `hotel.db` dosyası oluşturulur.

### Veritabanı Tabloları:
- **faults**: Arıza kayıtları
- **shifts**: Vardiya bilgileri
- **special_services**: Özel servis istekleri
- **menus**: Günlük menüler
- **cocktail_recipes**: Kokteyl tarifleri (önceden yüklenmiş)

## 🧪 Test

Veritabanı işlevselliğini test etmek için:
```bash
python test_database.py
```

## 📱 Kullanım

### Arıza Yönetimi
1. **Yeni Arıza Bildirme:**
   - "Arıza Bildir" butonuna tıklayın
   - Gerekli bilgileri doldurun
   - "Tamam" butonuna tıklayın

2. **Arıza Detaylarını Görüntüleme:**
   - Listeden bir arızaya çift tıklayın
   - Detay penceresinde arıza durumunu güncelleyebilirsiniz

3. **Arıza Listelerini Görüntüleme:**
   - "Bekleyen Arızalar": Sadece bekleyen arızalar
   - "Tüm Arızalar": Tüm arıza kayıtları

### F&B Yönetimi

#### Vardiya Yönetimi
1. Çalışan personel isimlerini virgülle ayırarak girin
2. İzinli personel isimlerini virgülle ayırarak girin
3. Günlük örtü rengini seçin
4. "Vardiya Bilgilerini Kaydet" butonuna tıklayın

#### Özel Servis
1. "Yeni Özel Servis Ekle" butonuna tıklayın
2. Servis açıklamasını yazın
3. Durumu seçin
4. "Tamam" butonuna tıklayın

#### Menü Yönetimi
1. **Günlük Menü:** Sol panelde günlük yemek menüsünü düzenleyin
2. **Kokteyl Tarifleri:** Sağ panelde sabit kokteyl tariflerini görüntüleyin
3. "Menüyü Kaydet" butonuna tıklayın

## 🎨 Arayüz Özellikleri

- Modern ve kullanıcı dostu tasarım
- Renkli durum göstergeleri
- Sekme tabanlı navigasyon
- Responsive layout
- Türkçe arayüz

## 🔧 Teknik Detaylar

### Dosya Yapısı
```
hotel_management_system/
├── main.py                 # Ana uygulama dosyası
├── database.py             # Veritabanı işlemleri
├── ui_fault_management.py  # Arıza yönetimi arayüzü
├── ui_fb_menu.py          # F&B yönetimi arayüzü
├── requirements.txt        # Gerekli paketler
├── test_database.py       # Veritabanı test dosyası
├── README.md              # Bu dosya
└── hotel.db               # SQLite veritabanı (otomatik oluşur)
```

### Kullanılan Teknolojiler
- **Python 3.x**: Ana programlama dili
- **PyQt5**: GUI framework
- **SQLite**: Veritabanı
- **datetime**: Tarih/saat işlemleri

## 🐛 Sorun Giderme

### Yaygın Sorunlar

1. **PyQt5 kurulum hatası:**
   ```bash
   pip install --upgrade pip
   pip install PyQt5
   ```

2. **Veritabanı hatası:**
   - `hotel.db` dosyasını silin ve uygulamayı yeniden başlatın

3. **Arayüz görünmüyor:**
   - Grafik arayüz desteği olan bir ortamda çalıştırdığınızdan emin olun
   - Linux'ta: `sudo apt-get install python3-pyqt5`

## 📞 Destek

Herhangi bir sorun yaşarsanız:
1. `test_database.py` dosyasını çalıştırarak veritabanı işlevselliğini test edin
2. Hata mesajlarını kontrol edin
3. Gerekli paketlerin yüklü olduğundan emin olun

## 📝 Notlar

- Uygulama ilk çalıştırıldığında örnek kokteyl tarifleri otomatik olarak yüklenir
- Tüm veriler yerel SQLite veritabanında saklanır
- Uygulama kapatılırken onay penceresi görüntülenir

## 🎯 Gelecek Geliştirmeler

- Rapor oluşturma özelliği
- Veri dışa aktarma (Excel, PDF)
- Kullanıcı yetkilendirme sistemi
- E-posta bildirimleri
- Mobil uygulama desteği

---

**Geliştirici:** Hotel Management Solutions  
**Versiyon:** 1.0  
**Tarih:** 2024
