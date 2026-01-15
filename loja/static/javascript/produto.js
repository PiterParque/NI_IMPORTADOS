// ====== GALERIA DE IMAGENS ======
document.addEventListener("DOMContentLoaded", () => {
    const thumbnails = document.querySelectorAll(".thumb");
    const mainImage = document.getElementById("imagem-principal");
    const btnEsquerda = document.querySelector(".seta-esquerda");
    const btnDireita = document.querySelector(".seta-direita");

    let imagemAtual = 0;

    function atualizarImagem(index) {
        thumbnails.forEach(t => t.classList.remove("active"));
        thumbnails[index].classList.add("active");
        mainImage.src = thumbnails[index].src;
        imagemAtual = index;
    }

    thumbnails.forEach((thumb, index) => {
        thumb.addEventListener("click", () => atualizarImagem(index));
    });

    if (btnDireita) {
        btnDireita.addEventListener("click", () => {
            imagemAtual = (imagemAtual + 1) % thumbnails.length;
            atualizarImagem(imagemAtual);
        });
    }

    if (btnEsquerda) {
        btnEsquerda.addEventListener("click", () => {
            imagemAtual = (imagemAtual - 1 + thumbnails.length) % thumbnails.length;
            atualizarImagem(imagemAtual);
        });
    }
});
