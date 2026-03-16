function adicionarDiv() {
    const container = document.getElementById("container");

    const div = document.createElement("div");
    div.classList.add("endereco");

    const inputEndereco = document.createElement("input");
    inputEndereco.type = "text";
    inputEndereco.placeholder = "Digite o endereço";
    inputEndereco.required = true;

    const inputCep = document.createElement("input");
    inputCep.type = "text";
    inputCep.placeholder = "Digite o CEP";
    inputCep.required = true;

    div.appendChild(inputEndereco);
    div.appendChild(inputCep);

    container.appendChild(div);

    // Remove o botão de adicionar após criar os campos
    const btnAdicionarEndereco = document.getElementById("btn-add");
    const finalizar = document.getElementById("btn-finalizar");
    
    if (btnAdicionarEndereco) {
        btnAdicionarEndereco.remove();
    }
}