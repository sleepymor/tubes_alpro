import mysql.connector

# Fungsi untuk membuat koneksi ke database
def create_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",           
        password="", 
        database="apv"
    )

# Fungsi untuk mendapatkan data vendor beserta relasinya
def get_vendors_with_relations(connection):
    query = """
    SELECT 
        v.ID AS VendorID,
        v.Name AS VendorName,
        v.Number AS ContactNumber,
        v.Website AS VendorWebsite,
        v.Logo AS VendorLogo,
        v.Address AS VendorAddress,
        v.MaxPrice,
        v.MinPrice,
        r.Region AS RegionName,
        s.Scale AS ScaleName
    FROM 
        vendor v
    JOIN 
        region r ON v.RegionID = r.ID
    LEFT JOIN 
        vendorscale vs ON v.ID = vs.VendorID
    LEFT JOIN 
        scale s ON vs.ScaleID = s.ID;
    """
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return results

# Fungsi untuk menampilkan data vendor dalam format tabel
def display_vendors(vendors):
    # Header
    print(f"{'VendorID':<10} {'VendorName':<20} {'ContactNumber':<15} {'RegionName':<20} {'ScaleName':<15} {'MaxPrice':<10} {'MinPrice':<10}")
    print("=" * 90)

    # Baris data
    for vendor in vendors:
        print(f"{vendor['VendorID']:<10} {vendor['VendorName']:<20} {vendor['ContactNumber']:<15} {vendor['RegionName']:<20} {vendor['ScaleName']:<15} {vendor['MaxPrice']:<10} {vendor['MinPrice']:<10}")

# Fungsi utama
def main():
    try:
        connection = create_connection()
        print("Koneksi berhasil.\n")

        vendors = get_vendors_with_relations(connection)

        print("Data vendor dengan relasi:")
        display_vendors(vendors)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        # Menutup koneksi
        if connection.is_connected():
            connection.close()
            print("\nKoneksi ditutup.")

# Menjalankan program
if __name__ == "__main__":
    main()
