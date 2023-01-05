import databaseHandler

from flask import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

def _bruger(brugerId, skoleId, retry=False):
    data, lastFetched = databaseHandler.getAllRecords()

    bruger = {}
    for __bruger in data:
        if __bruger["BrugerId og SkoleId"] == f"{brugerId}, {skoleId}":
            bruger = __bruger

    if bruger == {}:
        if not retry:
            databaseHandler.addRecord(brugerId=brugerId, skoleId=skoleId, pro=False, roller=[])
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