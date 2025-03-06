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
        oikea_vastaus_str=i
    return oikea_vastaus_str

def vastausvaihtoehdot():
    pelaajan_vastaus = str (input("Onko väite totta vai tarua?:"))
    if pelaajan_vastaus != "":
            pass
    else:
        print("Anna kelvollinen vastaus")
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
         password='tuut',
         autocommit=True
         )

'''tästä alkaa pääohjelma'''

tulosta_ohjeet()
arvottu_numero= random.randint(1,47)
hae_kysymys(arvottu_numero)
pelaajan_vastaus = vastausvaihtoehdot()
oikea_vastaus = hae_vastaus(arvottu_numero)
hae_vastaus()
tarkista_vastaus()
choose_airport()


class Karma:
    def __init__(self):
        self.pisteet = 100
    def hae_vastaus(self,numero):
        vaihtoehdot = [hae_kysymys()]
        return random.choice(vaihtoehdot)

    def tarkista_vastaus(self,arvottu_numero):
        oikea_vastaus = self.hae_vastaus(arvottu_numero)
        pelaajan_vastaus = self.vastausvaihtoehdot()

        if pelaajan_vastaus == oikea_vastaus:
            self.pisteet += 20
            print("Oikein! +20 karmaa.")
        else:
            self.pisteet -= 20
            print("Väärin! -20 karmaa.")

        print(f"Sinulla on nyt {self.pisteet} karmaa.\n")

karma = Karma()
