import json
from flask import Flask
app = Flask(__name__)
@app.route('/') # heittomerkin jälkeen jotain joka johtaa sen 01.py tiedostoon (kai)
def tulosta_ohjeet(): # esim. tähän def funktioiden nimet, jokaiselle omat
    # .....
    return # ...

if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=3000)