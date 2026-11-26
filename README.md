# Jitra QA Automation Test

Automated browser testing project for the Jitra Office web application using Python and Playwright.

## Test Coverage

| Script | Scenario |
|---|---|
| `1_test_login.py` | Verify login with email and password |
| `2_test_tambah_asset.py` | Add a new asset through the create asset form |
| `3_test_negative_tanggal.py` | Verify required Asset Tag validation when the form is submitted with an empty value |
| `4_test_excel_asset.py` | Read asset data from Excel and enter three records into the application |
| `test_jitra400.py` | Test the Raw Message drawer, JSON tab, Copy JSON action, clipboard failure state, and drawer reset behavior |

## Requirements

- Windows 10/11
- Python 3.10 or newer
- Internet access to `https://jitra-office.jiwalu.id`
- Access to a valid Jitra account
- Chromium browser for Playwright

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the Python packages:

```powershell
python -m pip install --upgrade pip
python -m pip install playwright pandas openpyxl
```

Install the Playwright Chromium browser:

```powershell
playwright install chromium
```

## Configuration

Before running the scripts, update the test account and application values in the Python files:

- `EMAIL`: Jitra account email
- `PASSWORD`: Jitra account password
- `LOGIN_URL`: Jitra login URL
- Asset values, purchase date, and model
- `DIRECT_MESSAGES_URL` in `test_jitra400.py`

Example configuration:

```python
EMAIL = "your-email@example.com"
PASSWORD = "your-password"
```

Do not commit real credentials. The repository `.gitignore` excludes `.env`, but the current scripts store credentials directly in source code. For safer credential handling, move these values to environment variables and load them with a package such as `python-dotenv`.

The Excel scenario uses:

```text
Jitra_QA_Office_Assets_Full_Detail_v1.0 (6).xlsx
```

It reads the first three rows and expects columns named `Nama Asset`, `Kategori`, and `Tanggal Pembelian`.

## Running Tests

Run a script directly from the project root:

```powershell
python 1_test_login.py
python 2_test_tambah_asset.py
python 3_test_negative_tanggal.py
python 4_test_excel_asset.py
python test_jitra400.py
```

The scripts launch Chromium with `headless=False`, so the browser remains visible for observation and debugging.

## Test Notes

- Scripts may fail if the Jitra UI or DOM selectors change.
- Login and data-creation results depend on the account permissions and the available master data.
- Asset model selection requires a model that already exists in Jitra.
- The purchase date is currently set to `18-11-2026` in the positive asset scenario.
- The negative scenario intentionally leaves the Asset Tag empty to verify validation.
- `test_jitra400.py` grants clipboard permissions and separately simulates clipboard access failure in one browser scenario.
- `4_test_excel_asset.py` is a first implementation prototype and should be adjusted if the Excel column names or Jitra form selectors differ from the current application.

## Project Structure

```text
.
|-- 1_test_login.py
|-- 2_test_tambah_asset.py
|-- 3_test_negative_tanggal.py
|-- 4_test_excel_asset.py
|-- test_jitra400.py
|-- Jitra_QA_Office_Assets_Full_Detail_v1.0 (6).xlsx
|-- .gitignore
`-- README.md
```

## Troubleshooting

### Playwright browser not found

Run:

```powershell
playwright install chromium
```

### Missing Python package

Run:

```powershell
python -m pip install playwright pandas openpyxl
```

### Login still fails

- Verify the email and password.
- Confirm that the Jitra account is active.
- Check whether two-factor authentication or an additional login step is required.
- Update the login selectors if the application UI changed.

### Element or data is not found

- Confirm the account has access to the relevant module.
- Update the placeholder, label, button, or route in the script.
- Re-run the browser session and inspect the current UI with Playwright debugging tools.