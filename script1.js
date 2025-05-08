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

// Tässä on pelkkä kartta

var map = L.map('map').setView([64.396769, 26.557239], 5);

L.tileLayer('https://api.maptiler.com/maps/landscape/{z}/{x}/{y}.png?key=Nh05MTH4Nra0WX7faVNq', {
    maxZoom: 5,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

L.marker([60.195187, 24.934882]).addTo(map) //L.marker on merkki kartalla, niitä voi luoda lisää lentokentille, jotka ovat valittavina pelaajalle
    .bindPopup('A pretty CSS popup.<br> Easily customizable.') 
    .openPopup()

//kysymys

window.addEventListener("DOMContentLoaded", () => {
    fetch('/api/kysymys')
        .then(response => response.json())
        .then(data => {
            document.getElementById("question").innerText = data.kysymys;
        })
        .catch(error => {
            console.error("Virhe haettaessa kysymystä:", error);
            document.getElementById("question").innerText = "Virhe ladattaessa kysymystä.";
        });
});

let currentQuestionId = null;

function loadQuestion() {
    fetch('/api/kysymys')
        .then(response => response.json())
        .then(data => {
            if (data.kysymys) {
                document.getElementById("question").innerText = data.kysymys;
                currentQuestionId = data.id;
            } else {
                document.getElementById("question").innerText = "Virhe ladattaessa kysymystä.";
            }
        })
        .catch(error => {
            console.error("Virhe kysymyksen haussa:", error);
            document.getElementById("question").innerText = "Virhe ladattaessa kysymystä.";
        });
}

function loadQuestion() {
    fetch('/api/kysymys')
        .then(response => response.json())
        .then(data => {
            if (data.kysymys) {
                document.getElementById("question").innerText = data.kysymys;
            } else {
                document.getElementById("question").innerText = "Kysymystä ei löytynyt.";
            }
        })
        .catch(error => {
            console.error("Virhe kysymyksen lataamisessa:", error);
            document.getElementById("question").innerText = "Virhe ladattaessa kysymystä.";
        });
}

function submitAnswer() {
    const userAnswer = document.getElementById("answer").value.toLowerCase().trim();

    fetch('/api/tarkista', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ vastaus: userAnswer })
    })
    .then(response => response.json())
    .then(data => {
        const msg = data.oikein ? "Oikein vastattu! + 10 karmaa" : "Väärin meni! - 10 karmaa";
        document.getElementById("confirmation").innerText = msg;
    })
    .catch(error => {
        console.error("Virhe vastauksen tarkistuksessa:", error);
        document.getElementById("confirmation").innerText = "Jotain meni pieleen.";
    });
}

window.onload = function() {
    loadQuestion();
};