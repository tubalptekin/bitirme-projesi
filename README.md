# bitirme-projesi
 Personel performans eğitim takip lisans bitirme projesi

 # Personel Performansı ve Eğitim Takip Sistemi

Bu proje, çalışanların aldığı eğitimleri ve performans süreçlerini yönetmek amacıyla geliştirilmiş basit bir takip sistemidir. Veritabanı olarak SQLite, backend tarafında Python ile FastAPI framework'ü kullanılmıştır.

## 🔧 Kullanılan Teknolojiler

- Python
- FastAPI
- SQLite
- SQLAlchemy
- Bcrypt (şifreleme için)
- Swagger UI (API test arayüzü)

## 📌 Temel Özellikler

- Çalışan (Kullanıcı) Ekleme, Listeleme, Güncelleme, Silme
- Departman Ekleme, Listeleme, Güncelleme, Silme
- Eğitim Ekleme, Listeleme, Güncelleme, Silme
- Katılım Sistemi (Çalışan → Eğitim ilişkisi)
- Belirli bir çalışanın katıldığı eğitimleri listeleme
- Belirli bir eğitime katılan çalışanları listeleme
- Kullanıcı şifreleri bcrypt ile güvenli şekilde hash'lenir

## 🚀 Başlatma

1. Gerekli kütüphaneleri yükleyin:
pip install fastapi uvicorn sqlalchemy bcrypt

2. Uygulamayı başlatın:
python APImain.py (çalışması için shell'e doğru dosya dizinindeyken yazmalısınız)

3. Tarayıcıda açın:
http://127.0.0.1:8080/docs


Dosya yapısı
bitirme-projesi/
│
├── backend/
│   ├── APImain.py
│   ├── database.py
│   ├── models.py
│   ├── routes.py
│   └── personel.db


**Örnek Test Senaryosu 
POST /departmanlar/ ile "İnsan Kaynakları" departmanını ekle

POST /kullanicilar/ ile "Zeynep Çalışkan" isimli bir kullanıcı ekle

POST /egitimler/ ile "Etkili Sunum Teknikleri" adlı eğitimi tanımla

POST /katilimlar/ ile bu kullanıcının bu eğitime katıldığını kaydet

GET /kullanicilar/{id}/katilimlar ile kullanıcının aldığı eğitimleri görüntüle

GET /egitimler/{id}/katilimlar ile eğitime katılan çalışanları görüntüle



Hazırlayan
Tuğba Alptekin 
Yönetim Bilişim Sistemleri 4. Sınıf

### 📄 “Uygulama Özeti” bölümü için kısa açıklama:

Bu bitirme projesinde, kurum içi personelin aldığı eğitimlerin ve performans gelişimlerinin izlenmesi amacıyla geliştirilen "Personel Performansı ve Eğitim Takip Sistemi" yer almaktadır.

Uygulama, Python dilinde FastAPI framework’ü kullanılarak geliştirilmiş ve SQLite veritabanı ile entegre edilmiştir. API desteklidir ve Swagger UI ile kolayca test edilebilir.

Sistemde; kullanıcı, departman ve eğitim bilgileri yönetilebilmekte, çalışanların eğitim katılımları izlenebilmekte ve belirli filtrelemelerle (örneğin “Bu çalışan hangi eğitimlere katıldı?” gibi) sorgular yapılabilmektedir.

Kullanıcı verileri bcrypt algoritması ile şifrelenmiştir. Kodlar GitHub üzerinden erişime açıktır.
