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
        time.sleep(0.5)

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
         user='root',
         password='läppäri',
         autocommit=True
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

    def karma_loppui(self):
        if self.pisteet <= 0:
            print("Karma on loppui!")
            puu.loppu_tarinat()
            return True
        return False




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
