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
