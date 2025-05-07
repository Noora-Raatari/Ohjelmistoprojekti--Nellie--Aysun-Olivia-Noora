import mysql.connector
import random
import time
from flask import Flask, jsonify, request

app = Flask(__name__)

'''tässä on funktiot'''

def tulosta_ohjeet ():
    ohjeet = [
    "Tervetuloa pelaamaan peliä xx!",
    "Pelin ideana on istuttaa 5 puuta.",
    "Sinulle on annettu 100 karmapistettä, jolla pääset etenemään pelissä.",
    "Jokaisella lentokentällä tulet kohtaamaan pulmia, joihin sinun täytyy vastata.",
    "Oikein vastaamalla voit saada itsellesi lisää karmaa, väärällä vastauksella menetät karmaa.",
    "Mikäli lentokentällä on mahdollista istuttaa puu, voit tehdä sen vastaamalla oikein kysymykseen.",
    "Kun olet suorittanut tehtävän kentällä, saat jatkaa matkaasi.",
    "Kone arpoo sinulle 3 satunnaista kenttää, joista voit valita kohteesi.",
    "Onnea peliin!"
    ]
    for ohje in ohjeet:
        print(ohje)
        time.sleep(0.5)

def hae_kysymys(id):
    kursori = yhteys.cursor()
    kursori.execute("SELECT kysymys FROM kysymykset WHERE id = %s", (id,))
    rivi = kursori.fetchone()
    kursori.close()
    return rivi[0] if rivi else None

def hae_vastaus(id):
    kursori = yhteys.cursor()
    kursori.execute("SELECT vastaus FROM kysymykset WHERE id = %s", (id,))
    rivi = kursori.fetchone()
    kursori.close()
    return rivi[0].strip().lower() if rivi else None


@app.route("/api/kysymys")
def hae_satunnainen_kysymys():
    kursori = yhteys.cursor()
    kursori.execute("SELECT id, kysymys FROM kysymykset ORDER BY RAND() LIMIT 1")
    rivi = kursori.fetchone()
    kursori.close()
    if rivi:
        return jsonify({"id": rivi[0], "kysymys": rivi[1]})
    return jsonify({"kysymys": None})

@app.route("/api/tarkista", methods=["POST"])
def tarkista_vastaus():
    data = request.json
    kysymys_id = data.get("id")
    pelaajan_vastaus = data.get("vastaus", "").strip().lower()
    oikea_vastaus = hae_vastaus(kysymys_id)
    if oikea_vastaus is None:
        return jsonify({"tilanne": "Virhe", "viesti": "Vastausta ei löytynyt"})
    oikein = pelaajan_vastaus == oikea_vastaus
    return jsonify({"oikein": oikein, "oikea_vastaus": oikea_vastaus})

@app.route("/")
def pelisivu():
    return render_template("pelisivu.html")

if __name__ == "__main__":
    app.run(debug=True)

def choose_airport():
    airport = (f"SELECT name from airport where iso_country = 'FI' and name like '%Airport%'")
    #print(airport)
    kursori = yhteys.cursor()
    kursori.execute(airport)
    airport = kursori.fetchall()
    random_airports = random.sample(airport, 3)
    jono = 1
    print(f"Valitse seuraava kohteesi!")
    for kenttä in random_airports:
        print(f"{jono}. {kenttä[0]}")
        jono += 1
    if random_airports:
        while True:
            valitse = int(input("(1-3): "))
            if 1 <= valitse <= 3:
                valittu_airport = random_airports[valitse - 1][0]
                print(f"Matkasi jatkuu lentokentälle: {valittu_airport}")
                if karma.lento():
                    break
                else:
                    print("Ei tarpeeksi karmaa lentämiseen, et voi lentää.")
                    break
            else:
                print("Virheellinen arvo, valitse numeroista 1, 2 tai 3.")
    return valittu_airport

def etsi_puu(valittukenttä):
    kentän_puu = False
    puun_sijainti = f"SELECT name from airport WHERE name = '{valittukenttä}' AND (name LIKE 'M%' OR name LIKE 'S%' OR name LIKE 'H%' OR name LIKE 'J%')"
    kursori = yhteys.cursor()
    kursori.execute(puun_sijainti)
    if kursori.fetchall():
        print("Löysit puun!")
        kentän_puu = True
    else:
        print("Puuta ei ole saatavilla tällä lentokentällä.")
    return kentän_puu

'''tässä on tietokantayhteys'''

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='peli',
         user='aysunlol',
         password='entiia',
         autocommit=True,
         )

'''tästä alkaa pääohjelma'''

tulosta_ohjeet()

''' Tässä on Karma ja Puut'''
class Puu:
    def __init__(self):
        self.puut = 0

    def update_puut(self, correct: bool):
        if correct:
            self.puut += 1
            print("Istutit kentällä puun!")
            print (f"Olet istuttanut {self.puut} puuta")
        else:
            print("Et pysty kasvattamaan kentällä puuta :(")
        return self.puut
    def puut_istutettu(self):
        if self.puut == 5:
            print("Sait istutettua kaikki 5 puuta! Onneksi olkoon!! Istutit tarpeeksi puita, jotta ilmaston lämpeneminen saadaan pysäytettyä!")
            return True
    def loppu_tarinat(self):

        if self.puut <=1:
            print("Et istuttanut tarpeeksi puita, etkä pystynyt vaikuttamaan ilmastonmuutoksen etenemiseen :(")
        elif 2<= self.puut <=3:
            print("Istutit vähän puita ja vain osa maailmasta selviytyi muuttuvasta ilmastosta")
        elif  self.puut == 4:
            print("Karmasi loppui, mutta onnistuit istuttamaan aika monta puuta!\n Pystyit pelastamaan suuren osan maailmaa lämpenevältä ilmastolta.")

class Karma:
    def __init__(self):
        self.pisteet = 100

    def update_karma(self, correct):
        if correct:
            self.pisteet += 20
            return "Oikein! +20 karmaa."
        else:
            self.pisteet -= 20
            return "Väärin! -20 karmaa."

    def lento(self):
        if self.pisteet >= 10:
            self.pisteet -= 10
            return "Lentosi hinta: -10 karmaa."
        else:
            return "Ei tarpeeksi karmaa lentämiseen!"

    def karma_loppui(self):
        return self.pisteet <= 0

karma = Karma()


#Karman alkuarvo:
karma = Karma()
#Puiden alkuarvo
puu = Puu()
peli_loppui = False
puut_kerätty = False

#Tästä alkaa pelin koko looppi
while not (peli_loppui or puut_kerätty):

        #Pelaaja saa valita lentokentän
    pelaajan_sijainti= choose_airport()

        #tarksitetaan onko kentällä puuta istutettavaksi
    mahdollisuus_puuhun= etsi_puu(pelaajan_sijainti)

        #Arvotaan kysymyspulma
    arvottu_numero= random.randint(1,47)
    hae_kysymys(arvottu_numero)

        #pelaaja vastaa
    pelaajan_vastaus = vastausvaihtoehdot()
    oikea_vastaus = hae_vastaus(arvottu_numero)

        #Tarkistetaan onko pelaajan vastaus ja päivitetään karma
    if pelaajan_vastaus == oikea_vastaus:
        karma.update_karma(True)
    else:
        karma.update_karma(False)

        #päivitetään puiden määrä jos kentällä pystyi istuttamaan ja jos pelaaja vastasi oikein
    if pelaajan_vastaus == oikea_vastaus and mahdollisuus_puuhun == True:
        puu.update_puut(True)
    elif mahdollisuus_puuhun== True:
        puu.update_puut(False)

    if karma.karma_loppui():
        peli_loppui = True

    if puu.puut_istutettu():
        puut_kerätty = True
else:
    print ("Peli on päättynyt")

