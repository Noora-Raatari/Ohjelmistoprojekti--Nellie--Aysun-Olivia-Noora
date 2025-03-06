import mysql.connector
import random
import time
#tässä on funktiot

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
        time.sleep(1)

def hae_kysymys(id):
    sql = (f"SELECT kysymys from kysymykset where id={id}")
    print (sql)
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
    print (sql)
    kursori =yhteys.cursor()
    kursori.execute(sql)
    tulos=kursori.fetchall()
    if kursori.rowcount > 0:
      for i in tulos:
        oikea_vastaus_str=i
        print (oikea_vastaus_str)
    return oikea_vastaus_str

def vastausvaihtoehdot():
    # print (f"Valitse oikea vaihtoehto: \n 1. Totta \n 2. Tarua" )
    pelaajan_vastaus = str (input("Onko väite totta vai tarua?:"))
    return pelaajan_vastaus

#tässä on tietokantayhteys
yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='peli',
         user='root',
         password='läppäri',
         autocommit=True
         )
tulosta_ohjeet()
arvottu_numero= random.randint(1,3)
hae_kysymys(arvottu_numero)
vastausvaihtoehdot()
oikea_vastaus = hae_vastaus(arvottu_numero)
pelaajan_vastaus = vastausvaihtoehdot()



class Karma:
    def __init__(self):
        self.pisteet = 100

    def vastaus(self, oikein: bool):
        if oikein:
            self.pisteet += 10
            print("Oikein! +20 karmaa.")
        else:
            self.pisteet -= 20
            print("Väärin! -20 karmaa.")
        print(f"Sinulla on nyt {self.pisteet} karmaa.\n")

karma = Karma()