
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
    .openPopup();