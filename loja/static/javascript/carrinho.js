// ====== FUNÇÕES GLOBAIS ======
function abrirCarrinho() {
    document.getElementById("carrinho-lateral").classList.add("ativo");
    document.getElementById("overlay").style.display = "block";
}

function fecharCarrinho() {
    document.getElementById("carrinho-lateral").classList.remove("ativo");
    document.getElementById("overlay").style.display = "none";
}

function atualizarCarrinho(carrinho) {
    const conteudo = document.querySelector(".carrinho-conteudo");
    const totalSpan = document.getElementById("total");
    conteudo.innerHTML = "";

    let total = 0;

    if (Object.keys(carrinho).length === 0) {
        conteudo.innerHTML = `<p class="carrinho-vazio">Seu carrinho está vazio</p>`;
        totalSpan.innerText = "0.00";
        return;
    }

    Object.values(carrinho).forEach(item => {
        total += item.quantidade * parseFloat(item.preco);

        conteudo.innerHTML += `
            <div class="item-carrinho">
                <p><strong>${item.nome}</strong></p>
                <p>${item.quantidade}x R$ ${item.preco}</p>
            </div>
        `;
    });

    totalSpan.innerText = total.toFixed(2);
}

// ====== EVENTOS ======
document.addEventListener("DOMContentLoaded", () => {
    const btnAbrir = document.querySelector(".fa-cart-shopping");
    const btnFechar = document.getElementById("fechar-carrinho");
    const overlay = document.getElementById("overlay");

    if (btnAbrir) btnAbrir.addEventListener("click", abrirCarrinho);
    btnFechar.addEventListener("click", fecharCarrinho);
    overlay.addEventListener("click", fecharCarrinho);
});
