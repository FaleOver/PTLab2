// Функция для добавления id продукта в список при клике на кнопку
let product_ids = [];

function addToCart(productId) {
    product_ids.push(productId);
    console.log(product_ids);
}

// Получаем элемент контейнера
const cart = document.getElementById('cart');

// Добавляем обработчик клика на контейнер
cart.addEventListener('click', function () {
    if (product_ids.length > 0) {
        let form = document.createElement("form");
        form.setAttribute("method", "post");
        form.setAttribute("action", "cart/");

        let data = document.createElement('input');
        data.setAttribute("name", "product_ids");
        data.setAttribute("value", product_ids);

        form.style.display = "none";
        form.appendChild(data);

        document.body.appendChild(form);

        form.submit();
    }
});