function adicionarDiv() {

    const container = document.getElementById("container");

    const div = document.createElement("div");
    div.classList.add("endereco");

    const inputEndereco = document.createElement("input");
    inputEndereco.type = "text";
    inputEndereco.name = "novo_endereco";
    inputEndereco.placeholder = "Digite o endereço";
    inputEndereco.required = true;

    const inputCep = document.createElement("input");
    inputCep.type = "text";
    inputCep.name = "novo_cep";
    inputCep.placeholder = "Digite o CEP";
    inputCep.required = true;

    div.appendChild(inputEndereco);
    div.appendChild(inputCep);

    container.appendChild(div);

    const btnAdicionar = document.getElementById("btn-add");
    if (btnAdicionar) btnAdicionar.remove();
}

document.addEventListener("DOMContentLoaded", () => {

    const btn = document.getElementById("btn-add");

    if (btn){
        btn.addEventListener("click", adicionarDiv);
    }

});
document.addEventListener("DOMContentLoaded", function () {

    const radiosPagamento = document.querySelectorAll('input[name="pagamento"]');
    const cartaoCampos = document.getElementById("cartao-campos");

    radiosPagamento.forEach(radio => {
        radio.addEventListener("change", function () {

            if (this.value === "cartao") {
                cartaoCampos.style.display = "block";
            } else {
                cartaoCampos.style.display = "none";
            }

        });
    });

});
const form = document.querySelector("form");

form.addEventListener("submit", function (e) {

    const metodo = document.querySelector('input[name="pagamento"]:checked');

    // Se não selecionou nada
    if (!metodo) {
        alert("Escolha um método de pagamento");
        e.preventDefault();
        return;
    }

    // Se for cartão → valida
    if (metodo.value === "cartao") {

        const numero = document.getElementById("numero_cartao").value;

        if (!validarCartao(numero)) {
            alert("Cartão inválido!");
            e.preventDefault(); // ❌ BLOQUEIA ENVIO
            return;
        }
    }

    // ✅ Se passou → deixa enviar normal
});