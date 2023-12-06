// Функция анимирования корзины
const cartButtons = document.querySelectorAll('.cart-animator-btn');

const animatedContainer = document.querySelector('.animated-container');
const cartContainer = document.querySelector('.cart-container');
const cartHandleWrapper = document.querySelector('.cart-handle-wrapper');
const cartHandle = document.querySelector('.cart-handle');
const cartItem = document.querySelector('.cart-item');

let isAnimating = false; // Флаг для отслеживания состояния анимации

function RemoveAnimatorClasses() {
    cartContainer.classList.remove('border-animator');
    cartHandleWrapper.classList.remove('handle-animator');
    cartHandle.classList.remove('handle-border-animator');
    cartItem.classList.remove('item-animator');
}

function AddAnimatorClasses() {
    cartContainer.classList.add('border-animator');
    cartHandleWrapper.classList.add('handle-animator');
    cartHandle.classList.add('handle-border-animator');
    cartItem.classList.add('item-animator');
}

cartButtons.forEach(function (cartButton) {
    cartButton.addEventListener('click', function () {
        if (isAnimating) {
            RemoveAnimatorClasses();
            void animatedContainer.offsetWidth; // Принудительный пересчёт стилей для сброса анимации
        }

        AddAnimatorClasses();

        // Установка флага, что анимация проигрывается
        isAnimating = true;

        // Ожидаем окончания анимации и удаляем класс
        animatedContainer.addEventListener('animationend', function animationEndHandler() {
            RemoveAnimatorClasses();
            animatedContainer.removeEventListener('animationend', animationEndHandler); // Удаляем обработчик события
            isAnimating = false; // Сброс флага анимации
        }, { once: true });
    });
});