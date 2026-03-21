// ================= INICIALIZAÇÃO =================

document.addEventListener("DOMContentLoaded", () => {

    carregarCarrinho();

    configurarCarrinho();
    configurarAdicionar();
    configurarQuantidadeProduto();

});


// ================= ABRIR / FECHAR =================

function configurarCarrinho() {

    const carrinhoEl = document.getElementById("carrinho-lateral");
    const overlay = document.getElementById("overlay-carrinho");
    const botaoCarrinho = document.querySelector(".carrinho");
    const fecharBtn = document.querySelector(".fechar-carrinho");

    if (botaoCarrinho) {
        botaoCarrinho.addEventListener("click", abrirCarrinho);
    }

    if (fecharBtn) {
        fecharBtn.addEventListener("click", fecharCarrinho);
    }

    if (overlay) {
        overlay.addEventListener("click", fecharCarrinho);
    }

    function abrirCarrinho() {
        carrinhoEl.classList.add("ativo");
        overlay.classList.add("ativo");
    }

    function fecharCarrinho() {
        carrinhoEl.classList.remove("ativo");
        overlay.classList.remove("ativo");
    }

}


// ================= CONTROLE QUANTIDADE (PÁGINA PRODUTO) =================

function configurarQuantidadeProduto() {

    const aumentar = document.querySelector(".aumentar");
    const diminuir = document.querySelector(".diminuir");
    const input = document.querySelector(".qtd-input");

    if (!aumentar || !diminuir || !input) return;

    // REMOVE eventos antigos (evita duplicação)
    aumentar.replaceWith(aumentar.cloneNode(true));
    diminuir.replaceWith(diminuir.cloneNode(true));

    const novoAumentar = document.querySelector(".aumentar");
    const novoDiminuir = document.querySelector(".diminuir");

    novoAumentar.addEventListener("click", () => {
        input.value = parseInt(input.value) + 1;
    });

    novoDiminuir.addEventListener("click", () => {
        if (input.value > 1) {
            input.value = parseInt(input.value) - 1;
        }
    });

}


// ================= ADICIONAR =================

function configurarAdicionar() {

    document.querySelectorAll(".btn-add").forEach(botao => {

        botao.addEventListener("click", function () {

            const produtoId = this.dataset.id;
            if (!produtoId) return;

            // pega quantidade se existir
            let quantidade = 1;
            const input = document.querySelector(".qtd-input");

            if (input) {
                quantidade = parseInt(input.value) || 1;
            }

            adicionarCarrinho(produtoId, quantidade);

        });

    });

}


// ================= FUNÇÃO ADICIONAR =================

async function adicionarCarrinho(produtoId, quantidade = 1) {

    const formData = new FormData();
    formData.append("produto_id", produtoId);
    formData.append("quantidade", quantidade);

    try {

        const response = await fetch("/adicionar_carrinho/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        });

        const data = await response.json();

        if (data.status === "sucesso") {

            atualizarCarrinho(data.carrinho);

            document.getElementById("carrinho-lateral").classList.add("ativo");
            document.getElementById("overlay-carrinho").classList.add("ativo");

        }

    } catch (error) {
        console.error("Erro ao adicionar:", error);
    }
}


// ================= CARREGAR =================

async function carregarCarrinho() {

    try {

        const response = await fetch("/obter_carrinho/");
        const data = await response.json();

        if (data.carrinho) {
            atualizarCarrinho(data.carrinho);
        }

    } catch (error) {
        console.error("Erro ao carregar carrinho:", error);
    }

}


// ================= ATUALIZAR =================

function atualizarCarrinho(carrinho) {

    const container = document.getElementById("carrinho-itens");
    const totalElemento = document.getElementById("carrinho-total");

    container.innerHTML = "";
    let total = 0;

    if (!carrinho || Object.keys(carrinho).length === 0) {
        container.innerHTML = "<p class='carrinho-vazio'>Seu carrinho está vazio</p>";
        totalElemento.textContent = "R$ 0,00";
        return;
    }

    for (let id in carrinho) {

        const item = carrinho[id];
        const subtotal = item.preco * item.quantidade;
        total += subtotal;

        const div = document.createElement("div");
        div.classList.add("item");

        div.innerHTML = `
            <img src="${item.imagem}" alt="${item.nome}">
            <div class="info">
                <p class="nome-produto">${item.nome}</p>
                <p>Qtd: ${item.quantidade}</p>
                <span class="subtotal">
                    ${subtotal.toLocaleString("pt-BR", { style: "currency", currency: "BRL" })}
                </span>
                <button class="remover-item" data-id="${id}">
                    Remover
                </button>
            </div>
        `;

        container.appendChild(div);
    }

    totalElemento.textContent = total.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });

    ativarRemover();

}


// ================= REMOVER =================

function ativarRemover() {

    document.querySelectorAll(".remover-item").forEach(botao => {

        botao.addEventListener("click", async function () {

            const produtoId = this.dataset.id;

            const response = await fetch("/remover_carrinho/", {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `produto_id=${produtoId}`
            });

            const data = await response.json();
            atualizarCarrinho(data.carrinho);

        });

    });

}


// ================= CSRF =================

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