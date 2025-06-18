# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Veritabanı bağlantı URL'si
DATABASE_URL = "sqlite:///./personel.db"

# SQLite için Engine oluştur
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SQLAlchemy ORM için Session Factory (Veritabanı işlemleri için)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tüm modellerin türetileceği Base sınıfı
Base = declarative_base()
