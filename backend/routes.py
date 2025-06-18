from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
import models
from database import SessionLocal
from pydantic import BaseModel
import bcrypt  # Şifreleme için

router = APIRouter()

# 📌 Veritabanı bağlantısı için
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📌 Kullanıcı modeli (Pydantic)
class KullaniciSchema(BaseModel):
    adSoyad: str
    email: str
    rol: str
    sifre: str
    departman_id: int

# ✅ 1. Kullanıcı Ekleme (Şifre Hash'leniyor)
@router.post("/kullanicilar/")
def create_kullanici(kullanici: KullaniciSchema, db: Session = Depends(get_db)):
    # Şifreyi güvenli hale getirme (hashleme)
    hashed_password = bcrypt.hashpw(kullanici.sifre.encode('utf-8'), bcrypt.gensalt())

    yeni_kullanici = models.Kullanici(
        adSoyad=kullanici.adSoyad,
        email=kullanici.email,
        rol=kullanici.rol,
        sifre=hashed_password.decode('utf-8'),  # Şifre string olarak kaydedilir
        departman_id=kullanici.departman_id
    )
    db.add(yeni_kullanici)
    db.commit()
    db.refresh(yeni_kullanici)
    return yeni_kullanici

# ✅ 2. Tüm Kullanıcıları Listeleme
@router.get("/kullanicilar/")
def kullanicilari_listele(db: Session = Depends(get_db)):
    return db.query(models.Kullanici).all()

# ✅ 3. Belirli Kullanıcıyı Getirme
@router.get("/kullanicilar/{kullanici_id}")
def get_kullanici(kullanici_id: int, db: Session = Depends(get_db)):
    kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
    if kullanici is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    return kullanici

# ✅ 4. Kullanıcı Güncelleme (Şifre Güncellenirse Hash'leme)
@router.put("/kullanicilar/{kullanici_id}")
def update_kullanici(kullanici_id: int, kullanici: KullaniciSchema, db: Session = Depends(get_db)):
    db_kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
    if db_kullanici is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    
    # Şifre değiştiriliyorsa tekrar hash'le
    hashed_password = bcrypt.hashpw(kullanici.sifre.encode('utf-8'), bcrypt.gensalt())

    db_kullanici.adSoyad = kullanici.adSoyad
    db_kullanici.email = kullanici.email
    db_kullanici.rol = kullanici.rol
    db_kullanici.sifre = hashed_password.decode('utf-8')
    db_kullanici.departman_id = kullanici.departman_id

    db.commit()
    db.refresh(db_kullanici)
    return db_kullanici

# ✅ 5. Kullanıcı Silme
@router.delete("/kullanicilar/{kullanici_id}")
def delete_kullanici(kullanici_id: int, db: Session = Depends(get_db)):
    db_kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == kullanici_id).first()
    if db_kullanici is None:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")

    db.delete(db_kullanici)
    db.commit()
    return {"message": "Kullanıcı başarıyla silindi"}

# ✅ 6. Kullanıcı Girişi (Şifre Kontrolü)
@router.post("/giris/")
def kullanici_giris(email: str = Form(...), sifre: str = Form(...), db: Session = Depends(get_db)):
    kullanici = db.query(models.Kullanici).filter(models.Kullanici.email == email).first()
    if not kullanici:
        raise HTTPException(status_code=400, detail="Kullanıcı bulunamadı")

    # Şifre doğrulama
    if not bcrypt.checkpw(sifre.encode('utf-8'), kullanici.sifre.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Geçersiz şifre")

    return {"message": "Giriş başarılı!"}

# 📌 Departman modeli (Pydantic)
class DepartmanSchema(BaseModel):
    departmanAd: str

# ✅ 1. Departman Ekleme
@router.post("/departmanlar/")
def create_departman(departman: DepartmanSchema, db: Session = Depends(get_db)):
    yeni_departman = models.Departman(departmanAd=departman.departmanAd)
    db.add(yeni_departman)
    db.commit()
    db.refresh(yeni_departman)
    return yeni_departman

# ✅ 2. Tüm Departmanları Listeleme
@router.get("/departmanlar/")
def list_departmanlar(db: Session = Depends(get_db)):
    return db.query(models.Departman).all()

# ✅ 3. Belirli Departmanı Getirme
@router.get("/departmanlar/{departman_id}")
def get_departman(departman_id: int, db: Session = Depends(get_db)):
    departman = db.query(models.Departman).filter(models.Departman.id == departman_id).first()
    if departman is None:
        raise HTTPException(status_code=404, detail="Departman bulunamadı")
    return departman

# ✅ 4. Departman Güncelleme
@router.put("/departmanlar/{departman_id}")
def update_departman(departman_id: int, departman: DepartmanSchema, db: Session = Depends(get_db)):
    db_departman = db.query(models.Departman).filter(models.Departman.id == departman_id).first()
    if db_departman is None:
        raise HTTPException(status_code=404, detail="Departman bulunamadı")

    db_departman.departmanAd = departman.departmanAd
    db.commit()
    db.refresh(db_departman)
    return db_departman

# ✅ 5. Departman Silme
@router.delete("/departmanlar/{departman_id}")
def delete_departman(departman_id: int, db: Session = Depends(get_db)):
    db_departman = db.query(models.Departman).filter(models.Departman.id == departman_id).first()
    if db_departman is None:
        raise HTTPException(status_code=404, detail="Departman bulunamadı")

    db.delete(db_departman)
    db.commit()
    return {"message": "Departman başarıyla silindi"}

from datetime import date
from pydantic import BaseModel

# 📌 Eğitim Pydantic şeması
class EgitimSchema(BaseModel):
    egitimAdi: str
    egitmen: str
    sure: int
    tarih: date
    aciklama: str | None = None  # Opsiyonel açıklama

# ✅ 1. Eğitim Ekleme
@router.post("/egitimler/")
def create_egitim(egitim: EgitimSchema, db: Session = Depends(get_db)):
    yeni_egitim = models.Egitim(
        egitimAdi=egitim.egitimAdi,
        egitmen=egitim.egitmen,
        sure=egitim.sure,
        tarih=egitim.tarih,
        aciklama=egitim.aciklama
    )
    db.add(yeni_egitim)
    db.commit()
    db.refresh(yeni_egitim)
    return yeni_egitim

# ✅ 2. Tüm Eğitimleri Listele
@router.get("/egitimler/")
def list_egitimler(db: Session = Depends(get_db)):
    return db.query(models.Egitim).all()

# ✅ 3. Belirli Eğitimi Getir
@router.get("/egitimler/{egitim_id}")
def get_egitim(egitim_id: int, db: Session = Depends(get_db)):
    egitim = db.query(models.Egitim).filter(models.Egitim.id == egitim_id).first()
    if egitim is None:
        raise HTTPException(status_code=404, detail="Eğitim bulunamadı")
    return egitim

# ✅ 4. Eğitimi Güncelle
@router.put("/egitimler/{egitim_id}")
def update_egitim(egitim_id: int, egitim: EgitimSchema, db: Session = Depends(get_db)):
    db_egitim = db.query(models.Egitim).filter(models.Egitim.id == egitim_id).first()
    if db_egitim is None:
        raise HTTPException(status_code=404, detail="Eğitim bulunamadı")

    db_egitim.egitimAdi = egitim.egitimAdi
    db_egitim.egitmen = egitim.egitmen
    db_egitim.sure = egitim.sure
    db_egitim.tarih = egitim.tarih
    db_egitim.aciklama = egitim.aciklama

    db.commit()
    db.refresh(db_egitim)
    return db_egitim

# ✅ 5. Eğitimi Sil
@router.delete("/egitimler/{egitim_id}")
def delete_egitim(egitim_id: int, db: Session = Depends(get_db)):
    db_egitim = db.query(models.Egitim).filter(models.Egitim.id == egitim_id).first()
    if db_egitim is None:
        raise HTTPException(status_code=404, detail="Eğitim bulunamadı")

    db.delete(db_egitim)
    db.commit()
    return {"message": "Eğitim başarıyla silindi"}

from datetime import date

# 📌 Katılım Şeması
class KatilimSchema(BaseModel):
    kullanici_id: int
    egitim_id: int
    tarih: date

# ✅ 1. Katılım Ekle
@router.post("/katilimlar/")
def create_katilim(katilim: KatilimSchema, db: Session = Depends(get_db)):
    yeni_katilim = models.Katilim(
        kullanici_id=katilim.kullanici_id,
        egitim_id=katilim.egitim_id,
        tarih=katilim.tarih
    )
    db.add(yeni_katilim)
    db.commit()
    db.refresh(yeni_katilim)
    return yeni_katilim

# ✅ 2. Tüm Katılımları Listele
@router.get("/katilimlar/")
def list_katilimlar(db: Session = Depends(get_db)):
    return db.query(models.Katilim).all()

# ✅ 3. Belirli Katılımı Getir
@router.get("/katilimlar/{katilim_id}")
def get_katilim(katilim_id: int, db: Session = Depends(get_db)):
    katilim = db.query(models.Katilim).filter(models.Katilim.id == katilim_id).first()
    if katilim is None:
        raise HTTPException(status_code=404, detail="Katılım bulunamadı")
    return katilim

# ✅ 4. Katılımı Sil
@router.delete("/katilimlar/{katilim_id}")
def delete_katilim(katilim_id: int, db: Session = Depends(get_db)):
    katilim = db.query(models.Katilim).filter(models.Katilim.id == katilim_id).first()
    if katilim is None:
        raise HTTPException(status_code=404, detail="Katılım bulunamadı")
    db.delete(katilim)
    db.commit()
    return {"message": "Katılım başarıyla silindi"}

@router.get("/egitimler/{egitim_id}/katilimlar")
def egitime_katilan_kullanicilar(egitim_id: int, db: Session = Depends(get_db)):
    katilimlar = (
        db.query(models.Katilim)
        .filter(models.Katilim.egitim_id == egitim_id)
        .all()
    )
    if not katilimlar:
        raise HTTPException(status_code=404, detail="Bu eğitime ait katılım bulunamadı")

    # Katılan kullanıcıların bilgilerini listele
    kullanici_listesi = []
    for katilim in katilimlar:
        kullanici = db.query(models.Kullanici).filter(models.Kullanici.id == katilim.kullanici_id).first()
        if kullanici:
            kullanici_listesi.append({
                "kullanici_id": kullanici.id,
                "adSoyad": kullanici.adSoyad,
                "email": kullanici.email,
                "rol": kullanici.rol
            })

    return {"egitim_id": egitim_id, "katilan_kullanicilar": kullanici_listesi}
