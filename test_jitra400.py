import json
import re
import time
from playwright.sync_api import sync_playwright, expect

LOGIN_URL = "https://jitra-office.jiwalu.id/login"
DIRECT_MESSAGES_URL = "https://jitra-office.jiwalu.id/operation/objects/216389/messages"
EMAIL = "kintandyahastuti@gmail.com"
PASSWORD = "gabolehtau"  # <-- Ganti dengan password asli kamu


def login_jitra(page):
    print("Mulai Login...")
    page.goto(LOGIN_URL)
    page.locator("input[type='email']").fill(EMAIL)
    page.locator("input[type='password']").fill(PASSWORD)
    page.locator("button[type='submit']").click()
    page.wait_for_url(lambda url: "/login" not in url, timeout=15000)
    page.wait_for_load_state("networkidle")
    print("Login sukses!")


def assert_tab_aktif(tab_locator, nama_tab):
    is_active = (
        tab_locator.get_attribute("aria-selected") == "true"
        or tab_locator.get_attribute("data-state") == "active"
    )
    assert is_active, f"Tab '{nama_tab}' seharusnya aktif!"


def skenario_1_raw_message_full_ac(playwright):
    print("\n--- Mulai Skenario 1: Raw Message (OOP-AC-027 & OOP-AC-028) ---")
    browser = playwright.chromium.launch(headless=False, slow_mo=400)
    context = browser.new_context(permissions=["clipboard-read", "clipboard-write"])
    page = context.new_page()

    try:
        login_jitra(page)
        print(f"Langsung buka {DIRECT_MESSAGES_URL}...")
        page.goto(DIRECT_MESSAGES_URL)
        page.locator("table tbody tr").first.wait_for(state="visible", timeout=15000)

        first_row = page.locator("table tbody tr").first
        first_row.click()

        drawer = page.locator("[role='dialog']").first
        expect(drawer).to_be_visible(timeout=10000)

        tab_formatted = drawer.get_by_role("tab", name="Formatted").or_(
            drawer.get_by_role("button", name="Formatted")
        ).first
        tab_json = drawer.get_by_role("tab", name="JSON").or_(
            drawer.get_by_role("button", name="JSON")
        ).first
        btn_copy_json = drawer.get_by_role("button", name=re.compile(r"Copy JSON", re.I))

        # 1. Default tab Formatted & Copy JSON tersembunyi
        assert_tab_aktif(tab_formatted, "Formatted")
        expect(btn_copy_json).to_be_hidden()
        print("[PASS] Default tab Formatted aktif & Copy JSON tersembunyi.")

        # Ambil seluruh teks di panel Formatted (aman untuk <table>, <dl>, maupun <div>)
        time.sleep(1)
        formatted_panel_text = drawer.inner_text()
        assert len(formatted_panel_text.strip()) > 0, "Isi tab Formatted kosong!"

        # 2. Pindah ke tab JSON & cek tombol Copy JSON sejajar kanan
        tab_json.click()
        assert_tab_aktif(tab_json, "JSON")
        expect(btn_copy_json).to_be_visible()

        tab_box = tab_json.bounding_box()
        copy_box = btn_copy_json.bounding_box()
        assert copy_box["x"] > tab_box["x"], "Tombol Copy JSON tidak di kanan tab"
        assert abs(copy_box["y"] - tab_box["y"]) < 20, "Tombol Copy JSON tidak sejajar tab"
        print("[PASS] Tab JSON aktif & tombol Copy JSON sejajar di kanan.")

        # 3. Cek keaslian key & Copy JSON ke clipboard
        json_box = drawer.locator("pre, code").first
        expect(json_box).to_be_visible(timeout=5000)
        displayed_json_text = json_box.inner_text()
        parsed_json = json.loads(displayed_json_text)

        sample_keys = list(parsed_json.keys())[:5]
        for key in sample_keys:
            assert key in formatted_panel_text, f"Raw key '{key}' tidak ditemukan di tab Formatted!"

        btn_copy_json.click()
        clipboard_text = page.evaluate("navigator.clipboard.readText()")
        assert json.loads(clipboard_text) == parsed_json, "Isi clipboard beda dengan JSON!"
        print("[PASS] Nama key asli cocok & Copy JSON berhasil menyalin payload.")

        # 4. Kembali ke Formatted -> Copy JSON hilang
        tab_formatted.click()
        expect(btn_copy_json).to_be_hidden()
        print("[PASS] Kembali ke tab Formatted, Copy JSON disembunyikan.")

        # 5. Tutup drawer & buka ulang -> reset ke Formatted
        btn_close = drawer.get_by_role("button", name=re.compile(r"Close|Tutup", re.I)).first
        if btn_close.is_visible():
            btn_close.click()
        else:
            page.keyboard.press("Escape")
        expect(drawer).to_be_hidden()

        first_row.click()
        expect(drawer).to_be_visible()
        assert_tab_aktif(tab_formatted, "Formatted")
        expect(btn_copy_json).to_be_hidden()
        print("[PASS] Reopen drawer reset kembali ke tab Formatted.")

    finally:
        time.sleep(1)
        browser.close()


def skenario_2_clipboard_gagal(playwright):
    print("\n--- Mulai Skenario 2: Simulasi Clipboard Gagal (OOP-TC-057) ---")
    browser = playwright.chromium.launch(headless=False, slow_mo=400)
    context = browser.new_context()
    page = context.new_page()

    try:
        page.add_init_script("""
            // 1. Gagalkan Clipboard API modern
            Object.defineProperty(navigator, 'clipboard', {
                value: {
                    writeText: () => Promise.reject(new Error('Clipboard access denied'))
                },
                configurable: true
            });
            // 2. Gagalkan juga fallback lama document.execCommand('copy')
            document.execCommand = () => false;
        """)

        login_jitra(page)
        page.goto(DIRECT_MESSAGES_URL)
        page.locator("table tbody tr").first.wait_for(state="visible", timeout=15000)

        page.locator("table tbody tr").first.click()
        drawer = page.locator("[role='dialog']").first
        expect(drawer).to_be_visible(timeout=10000)

        tab_json = drawer.get_by_role("tab", name="JSON").or_(
            drawer.get_by_role("button", name="JSON")
        ).first
        tab_json.click()
        drawer.get_by_role("button", name=re.compile(r"Copy JSON", re.I)).click()

        alert = page.locator("[role='alert']").first
        expect(alert).to_be_visible(timeout=5000)
        alert_text = alert.inner_text()
        print("Alert yang muncul:", alert_text)

        assert re.search(r"gagal|failed|error|unable|could not|cannot", alert_text, re.I), (
            f"Harusnya pesan gagal, tapi yang muncul: '{alert_text}'"
        )
        print("[PASS] Pesan gagal clipboard tampil dengan benar.")

    finally:
        time.sleep(1)
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        skenario_1_raw_message_full_ac(p)
        skenario_2_clipboard_gagal(p)
        print("\nSEMUA SKENARIO SELESAI!")