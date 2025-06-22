from flask import Flask, render_template, request, jsonify
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ✅ 建立連線到 Google Sheets 的函式
def get_sheet():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('drink-bot.json', scope)
    client = gspread.authorize(creds)
    # ✅ 你也可以改用 open_by_key('你的試算表ID')
    sheet = client.open("Drink Orders").sheet1
    return sheet

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit_order():
    data = request.get_json()
    drink = data.get("drink")
    sweetness = data.get("sweetness")
    ice = data.get("ice")
    qty = data.get("qty")

    print(f"收到訂單：{drink}, 甜度：{sweetness}, 冰塊：{ice}, 杯數：{qty}")

    # ✅ 寫入 Google 試算表
    sheet = get_sheet()
    sheet.append_row([drink, sweetness, ice, qty])

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
