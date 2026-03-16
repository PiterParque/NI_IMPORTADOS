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