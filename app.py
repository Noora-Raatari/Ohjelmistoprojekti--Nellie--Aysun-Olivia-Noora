from flask import Flask, request, jsonify, render_template
import mysql.connector
import random

app = Flask(__name__)

# Yhteys tietokantaan
yhteys = mysql.connector.connect(
    host='localhost',
    port=3306,
    database='peli',
    user='root',
    password='läppäri',
    autocommit=True
)

karma = 100
puut = 0

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/peli")
def peli():
    return render_template("peli.html")

@app.route("/get_question", methods=["GET"])
def get_question():
    id = random.randint(1, 47)
    kursori = yhteys.cursor()
    kursori.execute(f"SELECT kysymys FROM kysymykset WHERE id={id}")
    kysymys = kursori.fetchone()
    return jsonify({"id": id, "kysymys": kysymys[0] if kysymys else ""})

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    global karma, puut
    data = request.json
    id = data["id"]
    vastaus = data["vastaus"].strip().lower()
    kentta = data["kentta"]

    kursori = yhteys.cursor()
    kursori.execute(f"SELECT vastaus FROM kysymykset WHERE id={id}")
    oikea = kursori.fetchone()
    oikea_vastaus = oikea[0].strip().lower() if oikea else None

    if vastaus == oikea_vastaus:
        karma += 20
        istutettu = istutetaanko_puu(kentta)
        if istutettu:
            puut += 1
    else:
        karma -= 20
        istutettu = False

    return jsonify({
        "oikein": vastaus == oikea_vastaus,
        "karma": karma,
        "puut": puut,
        "istutettu": istutettu
    })


@app.route("/get_airports", methods=["GET"])
def get_airports():
    try:
        kursori = yhteys.cursor()
        print("Yhteys onnistui!")
        kursori.execute("SELECT name, latitude_deg, longitude_deg FROM airport WHERE iso_country = 'FI' AND name LIKE '%Airport%'")
        kentat = kursori.fetchall()
        print(f"Haettu kentät: {kentat}")
        valitut = random.sample(kentat, 3)
        return jsonify([
            {"name": k[0], "lat": k[1], "lng": k[2]}
            for k in valitut
        ])
    except Exception as e:
        print(f"Virhe reitillä '/get_airports': {e}")
        return jsonify({"error": str(e)}), 500


def istutetaanko_puu(kentta):
    # Sama logiikka kuin aiemmassa: tarkastetaan alkukirjain
    return kentta[0] in "MSHJ"

if __name__ == "__main__":
    app.run(debug=True)
