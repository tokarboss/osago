import gspread
from oauth2client.service_account import ServiceAccountCredentials

def send_to_google_sheets(data: dict):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("your_service_account.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Заявки ОСАГО").sheet1
    sheet.append_row([
        data.get('car_model'),
        data.get('year'),
        data.get('city'),
        data.get('driver_info'),
        data.get('drivers_type'),
        data.get('sts_number')
    ])
