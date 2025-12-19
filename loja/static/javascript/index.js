// ====== SLIDER PRINCIPAL ======
let index = 0;
const slides = document.querySelectorAll('.slider');

function showSlide(n) {
    slides.forEach(slide => slide.classList.remove('on'));
    slides[n].classList.add('on');
}

function nextSlide() {
    index = (index + 1) % slides.length;
    showSlide(index);
}

function prevSlide() {
    index = (index - 1 + slides.length) % slides.length;
    showSlide(index);
}

// Troca automática a cada 4s
setInterval(nextSlide, 4000);

if (slides.length > 0) showSlide(index);

// ====== CARROSSEL DE PRODUTOS ======
const lista = document.getElementById('lista-produtos');
const btnPrev = document.getElementById('prev');
const btnNext = document.getElementById('next');
const scrollAmount = 250; // distância em px que o carrossel anda a cada clique

if (btnNext && lista) {
    btnNext.addEventListener('click', () => {
        lista.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    });
}

if (btnPrev && lista) {
    btnPrev.addEventListener('click', () => {
        lista.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    });
}

console.log("Ola");
