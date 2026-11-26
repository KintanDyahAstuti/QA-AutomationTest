from playwright.sync_api import sync_playwright
import time

def test_tambah_asset():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        print("Mulai Skenario 2: Tambah Data Asset...")
        # 1. Login 
        page.goto("https://jitra-office.jiwalu.id/login") 
        page.locator("input[type='email']").fill("kintandyahastuti@gmail.com")
        
        # JANGAN LUPA GANTI PASSWORD LU DI SINI
        page.locator("input[type='password']").fill("gabolehtau")
        page.locator("button[type='submit']").click()
        page.wait_for_load_state("networkidle")
        
        # 2. JALUR BYPASS
        print("Membuka form tambah asset...")
        page.goto("https://jitra-office.jiwalu.id/asset/assets/create")
        page.wait_for_load_state("networkidle")
        
        # 3. Isi form
        page.get_by_placeholder("e.g. GPS-2026-001").fill("TEST-LAPTOP-01")
        page.get_by_placeholder("Optional asset name").fill("Laptop QA Kintan")
        
        # Ngisi Model
        page.get_by_text("Select model").click()
        page.keyboard.type("QA215-GPS-MODEL")
        page.keyboard.press("Enter")
        
        # PERBAIKAN: Ngisi Tanggal Beli
        # Karena ini tombol kalender, kita klik dulu baru ketik pakai keyboard
        page.get_by_label("Purchase date").click()
        page.keyboard.type("18-11-2026")
        page.keyboard.press("Enter")
        
        # 4. Klik tombol Save warna biru
        page.get_by_role("button", name="Save").click()
        
        print("Skenario 2 Beres: Robot sukses ngeklik Save!")
        
        time.sleep(3)
        browser.close()

if __name__ == "__main__":
    test_tambah_asset()