// Pop- up ikkunat aloitussivulla

const avaaPopUpPainike = document.querySelectorAll('[data-modal-target]')
const suljePopUpPainike = document.querySelectorAll('[data-close-button]')

avaaPopUpPainike.forEach(a => {
    a.addEventListener('click',()=>{
        const modal =document.querySelector(a.dataset.modalTarget)
        openModal(modal)
});
})

suljePopUpPainike.forEach(a => {
    a.addEventListener('click',()=>{
        const modal =a.closest('.modal')
        closeModal(modal)
});
})

function openModal(modal){
    if (modal ==null) return;
    modal.classList.add('active')
}
function closeModal(modal){
    if (modal ==null) return;
    modal.classList.remove('active')
}



let kenttaMarkers = []; // Taulukko kartan merkkejä varten

// Alustetaan kartta
const map = L.map('map').setView([65.0121, 25.4651], 5); // Suomi keskellä

// Lisätään OpenStreetMap taustakartta
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap contributors</a>'
}).addTo(map);

// Funktio, joka tyhjentää kartan ja arpoo uudet kentät
function arvoUudetKentat() {
    // Tyhjennetään kaikki aikaisemmat merkit
    kenttaMarkers.forEach(marker => {
        map.removeLayer(marker);  // Poistetaan merkit kartalta
    });
    kenttaMarkers = []; // Tyhjennetään taulukko

    // Haetaan uudet kentät
    fetch("/get_airports")
        .then(response => response.json())
        .then(data => {
            // Arvotaan satunnaisesti 3 kenttää
            const arvotutKentat = data.sort(() => Math.random() - 0.5).slice(0, 3);

            // Lisätään uudet kentät kartalle
            arvotutKentat.forEach(kentta => {
                const marker = L.marker([kentta.lat, kentta.lng]).addTo(map);
                marker.bindPopup(`<button onclick="valitseKentta('${kentta.name}')">${kentta.name}</button>`);
                kenttaMarkers.push(marker); // Lisätään merkki taulukkoon
            });
        })
        .catch(error => {
            console.error("Virhe kenttien haussa:", error);
        });
}

// Funktio, joka valitsee kentän ja hakee kysymyksen
function valitseKentta(nimi) {
    valittuKentta = nimi; // Tallennetaan valittu kenttä
    haeKysymys(); // Haetaan seuraava kysymys
}

// Funktio, joka hakee kysymyksen ja näyttää sen
function haeKysymys() {
    fetch("/get_question")
        .then(res => res.json())
        .then(data => {
            console.log("Kysymys haettu:", data); // Debug: tulostetaan kysymys

            // Päivitetään kysymys ja formi HTML:ään
            nykyinenKysymysID = data.id;
            const kysymysBox = document.querySelector(".pelivalikko");
            kysymysBox.innerHTML = `
                <p>${data.kysymys}</p>
                <form id="vastausForm">
                    <label><input type="radio" name="vastaus" value="totta"> Totta</label><br>
                    <label><input type="radio" name="vastaus" value="tarua"> Tarua</label><br><br>
                    <button type="submit">Vastaa</button>
                </form>
            `;
            document.getElementById("vastausForm").addEventListener("submit", lahetaVastaus);
        })
        .catch(error => {
            console.error("Virhe kysymyksen haussa:", error);
        });
}

// Funktio, joka lähettää vastauksen palvelimelle
function lahetaVastaus(e) {
    e.preventDefault();
    const valittu = document.querySelector('input[name="vastaus"]:checked');
    if (!valittu) return alert("Valitse vastaus!");

    // Lähetetään vastaus palvelimelle
    fetch("/submit_answer", {
        method: "POST",
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            id: nykyinenKysymysID,
            vastaus: valittu.value,
            kentta: valittuKentta
        })
    })
    .then(res => res.json())
    .then(data => {
        let tulos = `Vastasit ${data.oikein ? "oikein" : "väärin"}! Karma: ${data.karma}, Puut: ${data.puut}`;
        if (data.istutettu && data.oikein) {
            tulos += " — Istutit puun!";
        }
        document.querySelector(".pelivalikko").innerHTML += `<p>${tulos}</p>`;

        // Arvotaan uudet kentät
        arvoUudetKentat();
    });
}

// Alustetaan kentät alussa
arvoUudetKentat();
