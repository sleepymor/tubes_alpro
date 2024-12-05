import mysql.connector as mc
import bcrypt as bc


def db_setup():
    try:
        db = mc.connect(
            host="localhost",
            user="root",  
            password="",  
            database="apv"  
        )
        return db
    except mc.Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise

db = db_setup()
cursor = db.cursor()

#Logika SignUp
# try:
#     usernames = input("Enter your usernames: ")
#     passwords = input("Enter your passwords: ")
#     status = 'user'

#     hashed_password = bc.hashpw(passwords.encode('utf-8'), bc.gensalt())

#     cursor.execute("INSERT INTO user (usernames, passwords, status) VALUES (%s, %s, %s)", (usernames, hashed_password.decode('utf-8'), status))
#     db.commit()
#     print("Data inserted successfully!")

# except mc.Error as e:
#     print(f"Error: {e}")
# finally:
#     cursor.close()
#     db.close()

#logika login
# usernames = input("Enter your username: ")
# raw_password = input("Enter your password: ")
# try:
#     cursor.execute("SELECT passwords FROM user WHERE usernames = %s", (usernames,))
#     result = cursor.fetchone()
#     if result:
#         stored_password = result[0]
#         if bc.checkpw(raw_password.encode('utf-8'), stored_password.encode('utf-8')):
#             print("Login successful!")
#         else:
#             print("Invalid password.")
#     else:
#         print("Username not found.")
# except mc.Error as e:
#     print(f"Error: {e}")

# Fungsi untuk menampilkan region
# def display_regions(cursor):
#     cursor.execute("SELECT ID, Region FROM region")
#     regions = cursor.fetchall()
#     print("Daftar Region:")
#     for region in regions:
#         print(f"{region[0]}: {region[1]}")
#     return regions

# Fungsi untuk menampilkan scale
# def display_scales(cursor):
#     cursor.execute("SELECT ID, Scale FROM scale")
#     scales = cursor.fetchall()
#     print("Daftar Scale:")
#     for scale in scales:
#         print(f"{scale[0]}: {scale[1]}")
#     return scales

# Fungsi untuk menambahkan vendor
# def add_vendor(cursor):

#     name = input("Masukkan nama vendor: ")
#     number = input("Masukkan nomor vendor: ")
#     website = input("Masukkan website vendor: ")
#     logo = input("Masukkan logo vendor (URL/file path): ")
#     address = input("Masukkan alamat vendor: ")
#     max_price = int(input("Masukkan harga maksimum: "))
#     min_price = int(input("Masukkan harga minimum: "))

#     display_regions(cursor)
#     region_ids = input("Masukkan ID region (maksimal 3, pisahkan dengan koma): ")
#     region_ids = [int(id.strip()) for id in region_ids.split(",")[:3]]

#     display_scales(cursor)
#     scale_ids = input("Masukkan ID scale (maksimal 3, pisahkan dengan koma): ")
#     scale_ids = [int(id.strip()) for id in scale_ids.split(",")[:3]]

#     try:
#         cursor.execute(
#             "INSERT INTO vendor (Name, Number, Website, Logo, Address, MaxPrice, MinPrice, RegionID) "
#             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#             (name, number, website, logo, address, max_price, min_price, region_ids[0]),
#         )
#         vendor_id = cursor.lastrowid

#         for scale_id in scale_ids:
#             cursor.execute(
#                 "INSERT INTO vendorscale (VendorID, ScaleID) VALUES (%s, %s)",
#                 (vendor_id, scale_id),
#             )

#         for region_id in region_ids[1:]:
#             cursor.execute(
#                 "INSERT INTO vendor (Name, Number, Website, Logo, Address, MaxPrice, MinPrice, RegionID) "
#                 "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
#                 (name, number, website, logo, address, max_price, min_price, region_id),
#             )

#         db.commit()
#         print("Vendor berhasil ditambahkan.")
#     except mc.Error as err:
#         print(f"Terjadi kesalahan: {err}")
#         db.rollback()
#     finally:
#         cursor.close()
#         db.close()

# if __name__ == "__main__":
#     add_vendor(cursor)