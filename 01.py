import random

import mysql.connector
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

yhteys = mysql.connector.connect(
         host='localhost',
         port= 3306,
         database='peli',
         user='root',
         password='läppäri',
         autocommit=True
         )
arvottu_numero= random.randint(1,3)
hae_kysymys(arvottu_numero)

import time
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

tulosta_ohjeet()