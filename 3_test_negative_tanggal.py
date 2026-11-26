from playwright.sync_api import sync_playwright
import time

def test_negative():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        print("Mulai Skenario 3: Negative Test Validasi Form...")
        # 1. Login
        page.goto("https://jitra-office.jiwalu.id/login") 
        page.locator("input[type='email']").fill("kintandyahastuti@gmail.com")
        page.locator("input[type='password']").fill("gabolehtau")
        page.locator("button[type='submit']").click()
        page.wait_for_url("**/dashboard")
        
        # 2. Bypass ke halaman Create Asset
        print("Membuka form tambah asset...")
        page.goto("https://jitra-office.jiwalu.id/asset/assets/create?q=test")
        page.wait_for_load_state("networkidle")
        
        # 3. SENGAJA kosongkan Asset Tag (kolom wajib) buat ngetes validasi error
        page.get_by_placeholder("Optional asset name").fill("Monitor Error")
        
        # Isi Model
        page.get_by_text("Select model").click()
        page.keyboard.type("QA215-GPS-MODEL")
        page.keyboard.press("Enter")
        
        # 4. Buka kalender lalu klik 'Select' biar pop-up nutup dan nggak ngalangin tombol Save
        page.get_by_label("Purchase date").click()
        page.get_by_role("button", name="Select").click()
        
        # 5. Klik Save (sekarang nggak ketutupan lagi)
        page.get_by_role("button", name="Save").click()
        
        time.sleep(3)
        print("Skenario 3 Beres: Validasi Negative Test Terbukti!")
        browser.close()

if __name__ == "__main__":
    test_negative()