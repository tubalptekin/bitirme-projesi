import sqlite3

# Veritabanına bağlantı fonksiyonu
def get_connection():
    return sqlite3.connect("personel.db")

# Departman ekleme fonksiyonu
def add_department():
    departman_ad = input("Departman adını girin: ")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO departmanlar (departmanAd) VALUES (?)", (departman_ad,))
    conn.commit()
    conn.close()
    print("Departman eklendi.")

# Departmanları listeleme fonksiyonu
def list_departments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM departmanlar")
    departments = cursor.fetchall()
    conn.close()
    print("Departmanlar:")
    for dept in departments:
        print(f"ID: {dept[0]}, Ad: {dept[1]}")

# Çalışan ekleme fonksiyonu
def add_employee():
    ad_soyad = input("Çalışanın adını ve soyadını girin: ")
    email = input("E-posta girin: ")
    rol = input("Rol girin: ")
    sifre = input("Şifre girin: ")
    
    # Kullanıcıya departmanları listeleyip seçim yaptırmak
    list_departments()
    departman_id = input("Departman ID'sini girin: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kullanicilar (adSoyad, email, rol, sifre, departman_id) 
        VALUES (?, ?, ?, ?, ?)
    """, (ad_soyad, email, rol, sifre, departman_id))
    conn.commit()
    conn.close()
    print("Çalışan eklendi.")

# Çalışanları listeleme fonksiyonu
def list_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT k.id, k.adSoyad, k.email, d.departmanAd 
        FROM kullanicilar k
        LEFT JOIN departmanlar d ON k.departman_id = d.id
    """)
    employees = cursor.fetchall()
    conn.close()
    print("Çalışanlar:")
    for emp in employees:
        print(f"ID: {emp[0]}, Ad Soyad: {emp[1]}, E-posta: {emp[2]}, Departman: {emp[3]}")

# Eğitim ekleme fonksiyonu
def add_education():
    egitim_adi = input("Eğitim adını girin: ")
    egitmen = input("Eğitmen adını girin: ")
    sure = input("Eğitimin süresini (dakika) girin: ")
    tarih = input("Tarih girin (YYYY-MM-DD): ")
    aciklama = input("Açıklama girin: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO egitimler (egitimAdi, egitmen, sure, tarih, aciklama)
        VALUES (?, ?, ?, ?, ?)
    """, (egitim_adi, egitmen, sure, tarih, aciklama))
    conn.commit()
    conn.close()
    print("Eğitim eklendi.")

# Eğitimleri listeleme fonksiyonu
def list_educations():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM egitimler")
    educations = cursor.fetchall()
    conn.close()
    print("Eğitimler:")
    for edu in educations:
        print(f"ID: {edu[0]}, Eğitim Adı: {edu[1]}, Eğitmen: {edu[2]}, Süre: {edu[3]}, Tarih: {edu[4]}, Açıklama: {edu[5]}")

# Katılım ekleme fonksiyonu
def add_participation():
    list_employees()
    kullanici_id = input("Katılım eklemek istediğiniz çalışanın ID'sini girin: ")
    list_educations()
    egitim_id = input("Çalışanın katılacağı eğitimin ID'sini girin: ")
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO katilimlar (kullanici_id, egitim_id) VALUES (?, ?)", (kullanici_id, egitim_id))
    conn.commit()
    conn.close()
    print("Katılım kaydı eklendi.")

# Ana menü fonksiyonu
def main_menu():
    while True:
        print("\n--- Personel Performansı ve Eğitim Takip Sistemi ---")
        print("1. Departman Ekle")
        print("2. Çalışan Ekle")
        print("3. Eğitim Ekle")
        print("4. Katılım Ekle")
        print("5. Departmanları Listele")
        print("6. Çalışanları Listele")
        print("7. Eğitimleri Listele")
        print("8. Çıkış")
        secim = input("Seçiminizi yapın (1-8): ")
        
        if secim == '1':
            add_department()
        elif secim == '2':
            add_employee()
        elif secim == '3':
            add_education()
        elif secim == '4':
            add_participation()
        elif secim == '5':
            list_departments()
        elif secim == '6':
            list_employees()
        elif secim == '7':
            list_educations()
        elif secim == '8':
            print("Programdan çıkılıyor.")
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")

if __name__ == "__main__":
    main_menu()
