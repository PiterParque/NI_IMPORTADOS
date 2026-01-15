// ====== CARRINHO (VARIÁVEL GLOBAL) ======
let carrinho = {};

// ====== FUNÇÕES GLOBAIS ======
function abrirCarrinho() {
    document.getElementById("carrinho-lateral").classList.add("ativo");
    document.getElementById("overlay").style.display = "block";
}

function fecharCarrinho() {
    document.getElementById("carrinho-lateral").classList.remove("ativo");
    document.getElementById("overlay").style.display = "none";
}

// ====== ATUALIZA CARRINHO ======
function atualizarCarrinho() {
    const conteudo = document.querySelector(".carrinho-conteudo");
    const totalSpan = document.getElementById("total");
    conteudo.innerHTML = "";

    let total = 0;

    if (Object.keys(carrinho).length === 0) {
        conteudo.innerHTML = `<p class="carrinho-vazio">Seu carrinho está vazio</p>`;
        totalSpan.innerText = "0.00";
        return;
    }

    Object.entries(carrinho).forEach(([id, item]) => {
        const preco = parseFloat(item.preco) || 0;
        const subtotal = item.quantidade * preco;
        total += subtotal;

        conteudo.innerHTML += `
            <div class="item-carrinho">
                <p><strong>${item.nome || "Produto"}</strong></p>

                <div class="controle-quantidade">
                    <button class="btn-qty" onclick="alterarQuantidade('${id}', -1)">−</button>
                    <span class="qtd">${item.quantidade}</span>
                    <button class="btn-qty" onclick="alterarQuantidade('${id}', 1)">+</button>
                    <button class="btn-remover" onclick="removerItem('${id}')">x</button>
                </div>

                <p>Subtotal: R$ ${subtotal.toFixed(2)}</p>
            </div>
        `;
    });

    totalSpan.innerText = total.toFixed(2);
}

// ====== ALTERAR QUANTIDADE ======
function alterarQuantidade(id, valor) {
    if (!carrinho[id]) return;

    carrinho[id].quantidade += valor;

    if (carrinho[id].quantidade <= 0) {
        delete carrinho[id];
    }

    atualizarCarrinho();
}

// ====== REMOVER ITEM ======
function removerItem(id) {
    if (carrinho[id]) {
        delete carrinho[id];
        atualizarCarrinho();
    }
}

// ====== ADICIONAR PRODUTO ======
document.addEventListener("click", (e) => {
    const botao = e.target.closest(".button_carrinho");
    if (!botao) return;

    const id = botao.dataset.produtoId;
    const nome = botao.dataset.produtoNome || "Produto";
    const preco = parseFloat(botao.dataset.produtoPreco) || 0;

    if (carrinho[id]) {
        carrinho[id].quantidade += 1;
    } else {
        carrinho[id] = {
            nome: nome,
            preco: preco,
            quantidade: 1
        };
    }

    atualizarCarrinho();
    abrirCarrinho();
});

// ====== EVENTOS DO CARRINHO ======
document.addEventListener("DOMContentLoaded", () => {
    const btnAbrir = document.querySelector(".fa-cart-shopping");
    const btnFechar = document.getElementById("fechar-carrinho");
    const overlay = document.getElementById("overlay");

    if (btnAbrir) btnAbrir.addEventListener("click", abrirCarrinho);
    if (btnFechar) btnFechar.addEventListener("click", fecharCarrinho);
    if (overlay) overlay.addEventListener("click", fecharCarrinho);

    // Inicializa carrinho se houver dados no sessionStorage
    const data = sessionStorage.getItem("carrinho");
    if (data) {
        carrinho = JSON.parse(data);
        atualizarCarrinho();
    }
});

// ====== SALVA CARRINHO NO SESSION STORAGE ======
function salvarCarrinho() {
    sessionStorage.setItem("carrinho", JSON.stringify(carrinho));
}

// Sempre que atualizar o carrinho, salva
const observer = new MutationObserver(salvarCarrinho);
observer.observe(document.querySelector(".carrinho-conteudo"), { childList: true, subtree: true });
function finalizarCompra() {
    if (Object.keys(carrinho).length === 0) {
        alert("Seu carrinho está vazio");
        return;
    }

    fetch("/salvar-carrinho/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify(carrinho)
    })
    .then(response => response.json())
    .then(data => {
        if (data.ok) {
            window.location.href = "/detalhes_pedido/";
        } else {
            alert("Erro ao processar carrinho");
        }
    })
    .catch(() => alert("Erro de conexão"));
}
