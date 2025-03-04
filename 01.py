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