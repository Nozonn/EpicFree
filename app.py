from flask import Flask, render_template
from getFreeGames import get_free_games
import datetime as dt

app = Flask(__name__)

today = dt.date.today().strftime("%A %d %B %Y")
free_games = get_free_games()

startToday = dt.datetime.strptime(today, "%A %d %B %Y")
end = dt.datetime.strptime(free_games[0]["end_date"], "%A %d %B %Y")
remainingTime = (end-startToday).days



@app.route("/")
def index():
   return render_template("index.html", freeGames=free_games, today=today, remainingTime=remainingTime)

if __name__ == "__main__":
   app.run("192.168.1.159", 9000, debug=True)
