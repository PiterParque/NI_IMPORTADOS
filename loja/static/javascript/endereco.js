console.log("JS carregado");

function salvarEndereco(endereco, cep) {

    const formData = new FormData();
    formData.append("acao", "adicionar");
    formData.append("endereco", endereco);
    formData.append("cep", cep);

    fetch("", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    })
    .then(response => response.json()) // 🔥 agora é JSON
    .then(data => {
        console.log("Resposta JSON:", data);

        if (data.status === "ok") {
            alert("Endereço salvo com sucesso!");
            location.reload(); // opcional
        }
    })
    .catch(error => {
        console.error("Erro:", error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function adicionarDiv() {

    const container = document.getElementById("container");

    const div = document.createElement("div");
    div.classList.add("endereco");

    const inputEndereco = document.createElement("input");
    inputEndereco.type = "text";
    inputEndereco.placeholder = "Digite o endereço";

    const inputCep = document.createElement("input");
    inputCep.type = "text";
    inputCep.placeholder = "Digite o CEP";

    const botaoSalvar = document.createElement("button");
    botaoSalvar.innerText = "Salvar";
    botaoSalvar.type = "button";
    const botaoApagar = document.createElement("button");
    botaoApagar.innerText = "Apagar";

    botaoApagar.onclick = function () {
        apagarEndereco(ID_DO_ENDERECO, div);
    };

    // 🔥 AQUI ESTÁ O QUE FALTAVA
    botaoSalvar.onclick = function () {
        console.log("SALVAR CLICADO");
        salvarEndereco(inputEndereco.value, inputCep.value);
    };

    div.appendChild(inputEndereco);
    div.appendChild(inputCep);
    div.appendChild(botaoSalvar);

    container.appendChild(div);
}

function apagarEndereco(enderecoId, elementoDiv) {

    const formData = new FormData();
    formData.append("acao", "deletar");
    formData.append("endereco_id", enderecoId);

    fetch("", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "ok") {
            elementoDiv.remove(); // 🔥 remove da tela
        }
    })
    .catch(error => {
        console.error("Erro ao deletar:", error);
    });
}
