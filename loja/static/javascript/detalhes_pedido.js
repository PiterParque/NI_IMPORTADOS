document.addEventListener("DOMContentLoaded", () => {
    const inputs = document.querySelectorAll(".quantidade");
    const totalSpan = document.getElementById("total-pagamento");

    function atualizarTotal() {
        let total = 0;

        inputs.forEach(input => {
            const preco = parseFloat(input.dataset.preco) || 0;
            const qtd = parseInt(input.value) || 1;
            const subtotal = preco * qtd;

            // Atualiza subtotal do item
            const subtotalSpan = input.closest(".detalhes_itens").querySelector(".subtotal");
            subtotalSpan.innerText = subtotal.toFixed(2);

            total += subtotal;
        });

        // Atualiza total geral
        totalSpan.innerText = total.toFixed(2);
    }

    // Atualiza total sempre que o usuário muda a quantidade
    inputs.forEach(input => {
        input.addEventListener("input", atualizarTotal);
    });

    // Atualiza total ao carregar a página
    atualizarTotal();
});
