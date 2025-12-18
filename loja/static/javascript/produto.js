const thumbnails = document.querySelectorAll(".thumb");
const mainImage = document.getElementById("imagem-principal");
const btnEsquerda = document.querySelector(".seta-esquerda");
const btnDireita = document.querySelector(".seta-direita");

let imagemAtual = 0;

// Atualiza imagem principal
function atualizarImagem(index) {
  thumbnails.forEach(t => t.classList.remove("active"));
  thumbnails[index].classList.add("active");
  mainImage.src = thumbnails[index].src;
  imagemAtual = index;
}

// Clique nas miniaturas
thumbnails.forEach((thumb, index) => {
  thumb.addEventListener("click", () => {
    atualizarImagem(index);
  });
});

// Navegar com setas
btnDireita.addEventListener("click", () => {
  imagemAtual = (imagemAtual + 1) % thumbnails.length;
  atualizarImagem(imagemAtual);
});

btnEsquerda.addEventListener("click", () => {
  imagemAtual = (imagemAtual - 1 + thumbnails.length) % thumbnails.length;
  atualizarImagem(imagemAtual);
});
document.addEventListener("DOMContentLoaded", () => {
    const botaoCarrinho = document.querySelector(".button_carrinho");

    botaoCarrinho.addEventListener("click", () => {
        const produtoId = botaoCarrinho.dataset.produtoId;

        fetch("/adicionar-carrinho/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `produto_id=${produtoId}`,
        })
        .then(res => res.json())
        .then(data => {
            console.log("Produto adicionado:", data);
            abrirCarrinho(); // abre o carrinho lateral
            atualizarCarrinho(data.carrinho);
        });
    });
});

// CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
     
}
