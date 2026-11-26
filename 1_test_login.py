from playwright.sync_api import sync_playwright
import time

def test_login():
    with sync_playwright() as p:
        # Buka Chrome dan perlambat gerakan agar terekam di video
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        
        print("Mulai Skenario 1: Login...")
        page.goto("https://jitra-office.jiwalu.id/login") 
        
        # PERBAIKAN 1: Pakai type='email' karena web Jitra nggak kenal name='username'
        page.locator("input[type='email']").fill("kintandyahastuti@gmail.com")
        
        # PERBAIKAN 2: Masukin password asli lu di sini, jangan kecampur perintah terminal wkwk
        page.locator("input[type='password']").fill("gabolehtau")
        
        # Klik tombol submit
        page.locator("button[type='submit']").click()
        
        # Tunggu sampai loading selesai
        page.wait_for_load_state("networkidle")
        print("Login sukses!")
        
        time.sleep(2) # Jeda 2 detik sebelum browser menutup
        browser.close()

if __name__ == "__main__":
    test_login()