import pandas as pd
from playwright.sync_api import sync_playwright
import time

def test_tambah_asset_dari_excel():
    print("Membaca file Excel...")
    # Pastikan nama file sesuai persis dengan yang ada di folder
    # Kita batasi 3 baris pertama dulu (nrows=3) untuk uji coba simpel
    df = pd.read_excel("Jitra_QA_Office_Assets_Full_Detail_v1.0 (6).xlsx", nrows=3)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        # Proses Login
        page.goto("https://jitra-office.jiwalu.id/login") # GANTI DENGAN URL ASLI
        page.locator("input[type='email']").fill("kintandyahastuti@gmail.com")
        page.locator("input[type='password']").fill("gabolehtau")
        page.locator("button[type='submit']").click()
        page.wait_for_load_state("networkidle")
        
        # Masuk ke Modul Asset
        page.click("text=Modul Asset")
        
        # Looping otomatis sesuai jumlah baris di Excel
        for index, row in df.iterrows():
            print(f"\nMenginput data ke-{index + 1}...")
            page.click("text=Tambah Data")
            
            # GANTI NAMA KOLOM EXCEL SESUAI DENGAN YANG ADA DI FILE (misal: 'Nama Asset', 'Kategori')
            # GANTI SELECTOR HTML SESUAI DENGAN FORM JITRA
            page.fill("input[name='nama_asset']", str(row['Nama Asset']))
            page.fill("input[name='kategori']", str(row['Kategori']))
            page.fill("input[name='tanggal_pembelian']", str(row['Tanggal Pembelian'])) 
            
            # Simpan data
            page.click("button:has-text('Simpan')")
            page.wait_for_load_state("networkidle")
            print(f"-> Sukses input: {row['Nama Asset']}")
            
            time.sleep(1) # Jeda sejenak sebelum input baris selanjutnya
            
        print("\nSemua data dari Excel selesai diuji!")
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    test_tambah_asset_dari_excel()