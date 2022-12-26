import gspread
import time

serviceAccount = gspread.service_account(filename="credentials.json")
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
