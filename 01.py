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
    return
def etsi_puu():
    kentän_puu= False
    puun_sijainti = (
        f"select name from airport where iso_country = 'FI' AND name like '%airport%' and name like 'M%' or iso_country = 'FI' AND name like '%airport%' and name like 'S%' or iso_country = 'FI' AND name like '%airport%' and name like 'H%' or iso_country = 'FI' AND name like '%airport%' and name like 'J%'")
    if puun_sijainti in puun_sijainti:
        print("Löysit puun")
        kentän_puu = True
    else:
        print("Puuta ei ole saatavilla tällä lentokentällä")
    return kentän_puu

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

    def lento(self):
        if self.pisteet >= 10:
            self.pisteet -= 10
            print("Lentosi hinta: -10 karmaa.")
            print(f"Sinulla on nyt {self.pisteet} karmaa.")
        else:
            print("Ei tarpeeksi karmaa lentämiseen!")
            return False
        return True

class Puu:
    def __init__(self):
        self.puut = 0

    def update_puut(self, correct: bool):
        if correct:
            self.puut += 1
            print("Istutit kentällä puun!")
        else:
            print("Et pysty kasvattamaan kentällä puuta :(")

karma = Karma()
mahdollisuus_puuhun= etsi_puu()


random_airports = choose_airport()
arvottu_numero= random.randint(1,47)
hae_kysymys(arvottu_numero)
pelaajan_vastaus = vastausvaihtoehdot()
oikea_vastaus = hae_vastaus(arvottu_numero)

if pelaajan_vastaus == oikea_vastaus:
    karma.update_karma(True)
else:
    karma.update_karma(False)

puu = Puu()

if pelaajan_vastaus == oikea_vastaus and mahdollisuus_puuhun == True:
    puu.update_puut(True)
elif mahdollisuus_puuhun== True:
    puu.update_puut(False)
