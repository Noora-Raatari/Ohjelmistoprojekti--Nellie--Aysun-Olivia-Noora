import mysql.connector
import random
import time

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
        time.sleep(0)

def hae_kysymys(id):
    sql = (f"SELECT kysymys from kysymykset where id={id}")
    #print (sql)
    kursori =yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchall()
    if kursori.rowcount > 0:
      for i in tulos:
          print (f" {i}")
    else:
        print ("")
def hae_vastaus(id):
    sql = (f"SELECT vastaus from kysymykset where id={id}")
    #print (sql)
    kursori =yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchall()
    if kursori.rowcount > 0:
      for i in tulos:
        oikea_vastaus_str = i[0].strip().lower()
        print(oikea_vastaus_str)
    else:
      print("Vastausta ei löytynyt")
      return None
    return oikea_vastaus_str

def vastausvaihtoehdot():
    while True:
        pelaajan_vastaus = input("Onko väite totta vai tarua?: ").strip().lower()
        if pelaajan_vastaus in ['totta', 'tarua']:
            return pelaajan_vastaus
        else:
            print("Vastaus ei ole kelvollinen. Yritä uudelleen.")
    return pelaajan_vastaus

def choose_airport():
    airport = (f"SELECT name from airport where iso_country = 'FI' and name like '%Airport%'")
    print(airport)
    kursori = yhteys.cursor()
    kursori.execute(airport)
    airport = kursori.fetchall()
    random_airports = random.sample(airport, 3)
    vastaus = []
    for rivi in random_airports:
        vastaus.append(rivi[0])
    print(vastaus)

'''tässä on tietokantayhteys'''

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='peli',
         user='root',
         password='läppäri',
         autocommit=True
         )

'''tästä alkaa pääohjelma'''

tulosta_ohjeet()
arvottu_numero= random.randint(1,47)
hae_kysymys(arvottu_numero)
pelaajan_vastaus = vastausvaihtoehdot()
oikea_vastaus = hae_vastaus(arvottu_numero)
choose_airport()

'''if pelaajan_vastaus==oikea_vastaus:
    print("Jee oikein")
else:
    print("väärin :(")'''


class Karma:
    def __init__(self):
        self.pisteet = 100

    def update_karma(self, correct: bool):
        if correct:
            self.pisteet += 20
            print("Oikein! +20 karmaa.")
        else:
            self.pisteet -= 20
            print("Väärin! -20 karmaa.")
        print(f"Sinulla on nyt {self.pisteet} karmaa.\n")

karma = Karma()
if pelaajan_vastaus == oikea_vastaus:
    karma.update_karma(True)
else:
    karma.update_karma(False)

#Lentokenttä#

def choose_airport():
    airport = (f"SELECT name from airport where iso_country = 'FI' and name like '%Airport%'")
    print(airport)
    kursori = yhteys.cursor()
    kursori.execute(airport)
    airport = kursori.fetchall()
    random_airports = random.sample(airport, 3)
    jono = 1
    for kenttä in random_airports:
        print(f"{jono}. {kenttä[0]}")
        jono += 1

    return random_airports

random_airports = choose_airport()

if random_airports:
    while True:
        valitse = int(input("(1-3): "))
        if 1 <= valitse <= 3:
            valittu_airport = random_airports[valitse - 1][0]
            print(f"Matkasi jatkuu lentokentälle: {valittu_airport}")
            break
        else:
            print("Virheellinen arvo, valitse numeroista 1, 2 tai 3.")
