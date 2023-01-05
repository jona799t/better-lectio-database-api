import gspread
import time
import os

from flask import *
from flask_cors import CORS


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


app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

def _bruger(brugerId, skoleId, retry=False):
    data, lastFetched = getAllRecords()

    bruger = {}
    for __bruger in data:
        if __bruger["BrugerId og SkoleId"] == f"{brugerId}, {skoleId}":
            bruger = __bruger

    if bruger == {}:
        if not retry:
            addRecord(brugerId=brugerId, skoleId=skoleId, pro=False, roller=[])
            return _bruger(brugerId, skoleId, retry=True)
        else:
            return {"error": "Der skete en fejl"}
    else:
        return jsonify({
            "bruger_id": bruger["BrugerId og SkoleId"].split(", ")[0],
            "skole_id": bruger["BrugerId og SkoleId"].split(", ")[1],
            "pro": True if bruger["Pro"] == "TRUE" else False,
            "last_fetched": lastFetched
        })

@app.route('/')
def index():
    return """
        <!DOCTYPE html>
        <html>
          <head>
            <title>Loading...</title>
            <meta http-equiv="refresh" content="0; url=https://github.com/BetterLectio/database-api">
            <script>window.location.href = "https://github.com/BetterLectio/database-api"</script>
          </head>
          <body>
            <p>Not redirected? Go to <a href="https://github.com/BetterLectio/database-api">github.com/BetterLectio/database-api</a></p>
          </body>
        </html>
    """
    #
@app.route('/bruger')
def bruger():
    brugerId = request.args.get('bruger_id')
    skoleId = request.args.get('skole_id')

    if brugerId == None or skoleId == None:
        return jsonify({"error": "Før at denne handling kan gennemføres skal du definere både et bruger_id og et skole_id"})

    return _bruger(brugerId, skoleId)

if __name__ == '__main__':
   app.run(debug = True)