document.addEventListener("DOMContentLoaded", function () {

    const botoes = document.querySelectorAll(".btn-add");

    if (botoes.length === 0) {
        console.warn("Nenhum botão .btn-add encontrado");
        return;
    }

    botoes.forEach(botao => {
        botao.addEventListener("click", function () {

            const produtoId = this.dataset.id;

            if (!produtoId) {
                console.error("ID do produto não encontrado");
                return;
            }

            adicionarCarrinho(produtoId);
        });
    });

});


async function adicionarCarrinho(produtoId) {

    const formData = new FormData();
    formData.append("produto_id", produtoId);

    try {

        const response = await fetch("/adicionar_carrinho/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken")
            },
            body: formData
        });

        if (!response.ok) {
            throw new Error("Erro na requisição");
        }

        const data = await response.json();

        console.log("Produto adicionado:", data);

        // 🔥 ESSA LINHA ESTAVA FALTANDO
        if (data.status === "sucesso") {
            atualizarCarrinho(data.carrinho);
        }

    } catch (error) {
        console.error("Erro ao adicionar no carrinho:", error);
    }
}

function atualizarCarrinho(carrinho) {

    const container = document.getElementById("carrinho-itens");
    const totalElemento = document.getElementById("carrinho-total");

    if (!container || !totalElemento) return;

    container.innerHTML = ""; // limpa antes de recriar

    let total = 0;

    // Verifica se o carrinho está vazio
    if (!carrinho || Object.keys(carrinho).length === 0) {
        container.innerHTML = "<p class='carrinho-vazio'>Seu carrinho está vazio</p>";
        totalElemento.textContent = "R$ 0,00";
        return;
    }

    for (let id in carrinho) {

        const item = carrinho[id];

        const subtotal = item.preco * item.quantidade;
        total += subtotal;

        const divItem = document.createElement("div");
        divItem.classList.add("item");

        divItem.innerHTML = `
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

        container.appendChild(divItem);
    }

    totalElemento.textContent = total.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL"
    });
}
document.addEventListener("DOMContentLoaded", () => {

    const botaoCarrinho = document.querySelector(".carrinho");
    const carrinho = document.getElementById("carrinho-lateral");
    const overlay = document.getElementById("overlay-carrinho");
    const fechar = document.getElementById("fechar-carrinho");

    botaoCarrinho.addEventListener("click", (e) => {
        e.preventDefault();
        carrinho.classList.add("ativo");
        overlay.classList.add("ativo");
    });

    fechar.addEventListener("click", fecharCarrinho);
    overlay.addEventListener("click", fecharCarrinho);

    function fecharCarrinho() {
        carrinho.classList.remove("ativo");
        overlay.classList.remove("ativo");
    }

});