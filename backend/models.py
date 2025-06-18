from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base  # database.py içindeki Base'i kullanıyoruz

# Departman Modeli
class Departman(Base):
    __tablename__ = "departmanlar"

    id = Column(Integer, primary_key=True, index=True)
    departmanAd = Column(String, nullable=False, unique=True)

    # Departman ile kullanıcılar arasındaki ilişki
    kullanicilar = relationship("Kullanici", back_populates="departman")


# Kullanıcı Modeli
class Kullanici(Base):
    __tablename__ = "kullanicilar"

    id = Column(Integer, primary_key=True, index=True)
    adSoyad = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    rol = Column(String, nullable=False)
    sifre = Column(String, nullable=False)
    departman_id = Column(Integer, ForeignKey("departmanlar.id"))

    # Kullanıcının bağlı olduğu departmanı
    departman = relationship("Departman", back_populates="kullanicilar")
from sqlalchemy import Column, Integer, String, Date

# Eğitimler Tablosu
class Egitim(Base):
    __tablename__ = "egitimler"

    id = Column(Integer, primary_key=True, index=True)
    egitimAdi = Column(String, nullable=False)
    egitmen = Column(String, nullable=False)
    sure = Column(Integer, nullable=False)
    tarih = Column(Date, nullable=False)
    aciklama = Column(String)

from sqlalchemy import Date

# Katılım Tablosu
class Katilim(Base):
    __tablename__ = "katilimlar"

    id = Column(Integer, primary_key=True, index=True)
    kullanici_id = Column(Integer, ForeignKey("kullanicilar.id"))
    egitim_id = Column(Integer, ForeignKey("egitimler.id"))
    tarih = Column(Date)

    kullanici = relationship("Kullanici")
    egitim = relationship("Egitim")
