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

document.addEventListener("DOMContentLoaded", () => {
    const btn = document.querySelector(".button_carrinho");

    btn.addEventListener("click", () => {
        const produtoId = btn.dataset.produtoId;

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
            atualizarCarrinho(data.carrinho);
            abrirCarrinho();
        });
    });
});

// CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie) {
        document.cookie.split(";").forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
