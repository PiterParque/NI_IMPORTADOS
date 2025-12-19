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

showSlide(index);


// Carrossel de produtos
const lista = document.getElementById('lista-produtos');
const btnPrev = document.getElementById('prev');
const btnNext = document.getElementById('next');

const scrollAmount = 250; // distância em px que o carrossel anda a cada clique

btnNext.addEventListener('click', () => {
  lista.scrollBy({ left: scrollAmount, behavior: 'smooth' });
});

btnPrev.addEventListener('click', () => {
  lista.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
});

console.log("Ola");
function atualizarCarrinho(carrinho) {
    const conteudo = document.querySelector(".carrinho-conteudo");
    conteudo.innerHTML = "";

    if (Object.keys(carrinho).length === 0) {
        conteudo.innerHTML = "<p>Seu carrinho está vazio</p>";
        return;
    }

    Object.values(carrinho).forEach(item => {
        conteudo.innerHTML += `
            <div class="item-carrinho">
                <p>${item.nome}</p>
                <p>${item.quantidade}x R$ ${item.preco}</p>
            </div>
        `;
    });
}
