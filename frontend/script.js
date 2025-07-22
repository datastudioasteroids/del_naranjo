// Menú responsive fuera de DOMContentLoaded para que siempre funcione
document.querySelector('.menu-toggle').addEventListener('click', () => {
  document.querySelector('.nav-list').classList.toggle('show');
});

document.addEventListener('DOMContentLoaded', () => {
  // Inicializar Swiper
  new Swiper('.autores-swiper', {
    slidesPerView: 'auto',
    spaceBetween: 16,
    loop: true,
    centeredSlides: true,
    autoplay: {
      delay: 3000,
      disableOnInteraction: false,
    },
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    breakpoints: {
      640: {
        slidesPerView: 2,
        spaceBetween: 20,
      },
      1024: {
        slidesPerView: 3,
        spaceBetween: 24,
      },
    },
  });

  // Aquí puedes seguir añadiendo más funciones tuyas si las tienes…
});
