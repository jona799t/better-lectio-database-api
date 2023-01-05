import gspread
import time
import os
import json

credentials = {
    'type': os.environ.get("type"),
    'project_id': os.environ.get("project_id"),
    'private_key_id': os.environ.get("private_key_id"),
    'private_key': os.environ.get("private_key"),
    'client_email': os.environ.get("client_email"),
    'client_id': os.environ.get("client_id"),
    'auth_uri': os.environ.get("auth_uri"),
    'token_uri': os.environ.get("token_uri"),
    'auth_provider_x509_cert_url': os.environ.get("auth_provider_x509_cert_url"),
    'client_x509_cert_url': os.environ.get("type")
}

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