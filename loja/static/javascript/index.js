document.addEventListener("DOMContentLoaded", () => {

  let slides = document.querySelectorAll(".slide");
  let current = 0;

  function showSlide(index) {
    slides.forEach(slide => slide.classList.remove("active"));
    slides[index].classList.add("active");
  }

  document.querySelector(".next").addEventListener("click", () => {
    current = (current + 1) % slides.length;
    showSlide(current);
  });

  document.querySelector(".prev").addEventListener("click", () => {
    current = (current - 1 + slides.length) % slides.length;
    showSlide(current);
  });

  setInterval(() => {
    current = (current + 1) % slides.length;
    showSlide(current);
  }, 5000);

});
document.addEventListener("DOMContentLoaded", () => {

  const track = document.querySelector(".product-track");
  const next = document.querySelector(".next-prod");
  const prev = document.querySelector(".prev-prod");

  if (!track) return;

  const cardWidth = 270;

  /* ===== SETAS ===== */
  next.addEventListener("click", () => {
    track.scrollLeft += cardWidth;
  });

  prev.addEventListener("click", () => {
    track.scrollLeft -= cardWidth;
  });

  /* ===== DRAG MOUSE + TOUCH ===== */
  let isDown = false;
  let startX;
  let scrollLeft;

  track.addEventListener("mousedown", (e) => {
    isDown = true;
    track.classList.add("active-drag");
    startX = e.pageX - track.offsetLeft;
    scrollLeft = track.scrollLeft;
  });

  track.addEventListener("mouseleave", () => {
    isDown = false;
    track.classList.remove("active-drag");
  });

  track.addEventListener("mouseup", () => {
    isDown = false;
    track.classList.remove("active-drag");
  });

  track.addEventListener("mousemove", (e) => {
    if (!isDown) return;
    e.preventDefault();
    const x = e.pageX - track.offsetLeft;
    const walk = (x - startX) * 1.5; // velocidade
    track.scrollLeft = scrollLeft - walk;
  });

  /* ===== TOUCH (CELULAR) ===== */
  track.addEventListener("touchstart", (e) => {
    startX = e.touches[0].pageX;
    scrollLeft = track.scrollLeft;
  });

  track.addEventListener("touchmove", (e) => {
    const x = e.touches[0].pageX;
    const walk = (x - startX) * 1.5;
    track.scrollLeft = scrollLeft - walk;
  });

});
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
document.querySelectorAll(".btn-add-carrinho").forEach(btn => {
    btn.addEventListener("click", () => {
        const produtoId = btn.dataset.id;

        fetch("/carrinho/adicionar/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `produto_id=${produtoId}`
        })
        .then(res => res.json())
        .then(data => {
            atualizarCarrinho(data.carrinho);
            document.getElementById("carrinho-lateral").classList.add("ativo");
            document.getElementById("overlay-carrinho").classList.add("ativo");
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
function atualizarCarrinho(carrinho) {
    const container = document.getElementById("carrinho-itens");
    container.innerHTML = "";

    let total = 0;

    Object.values(carrinho).forEach(item => {
        total += item.preco * item.quantidade;

        container.innerHTML += `
            <div class="item">
                <img src="${item.imagem}">
                <div class="info">
                    <p>${item.nome}</p>
                    <span>R$ ${item.preco.toFixed(2)}</span>
                    <small>Qtd: ${item.quantidade}</small>
                </div>
            </div>
        `;
    });

    document.querySelector(".carrinho-footer strong").innerText =
        `R$ ${total.toFixed(2)}`;
}
