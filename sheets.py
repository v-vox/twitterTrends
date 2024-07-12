import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
import getTrends

from datetime import datetime


SERVICE_ACCOUNT_FILE = # service account json 
SPREADSHEET_ID = # id of spread sheet
RANGE_NAME = # output range on sheets

def write_to_sheet(values):
    # authenticate service API
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/spreadsheets']
    )
    service = build('sheets', 'v4', credentials=creds)

    body = {
        'values': values
    }
    result = service.spreadsheets().values().append(
        spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME,
        valueInputOption='USER_ENTERED', body=body).execute()
    print(f"{result.get('updatedCells')} cells updated.")


if __name__ == '__main__':
    time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    print(time)
    output = getTrends.main(5,5) #change this to edit parameters for scraping
    output_data = [[time],[output]]
    write_to_sheet(output_data)
