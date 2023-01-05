import gspread
import time
import os
import json

credentials = json.loads(os.environ.get("credentials").replace("\\\\", "\\"))

serviceAccount = gspread.service_account_from_dict(credentials)
database = serviceAccount.open("Better Lectio")
brugerDatabase = database.worksheet("Brugere")

fetchFrequency = 60  # sek
lastFetched = -1

allRecords = []

def getAllRecords():
    global lastFetched
    global allRecords

    if time.time() > lastFetched + fetchFrequency:
        allRecords = brugerDatabase.get_all_records()
        lastFetched = time.time()

    return allRecords, lastFetched

def addRecord(brugerId, skoleId, pro, roller):
    global lastFetched

    brugerDatabase.append_row([f"{brugerId}, {skoleId}", pro, ", ".join(roller)])
    lastFetched = -1

    return True
