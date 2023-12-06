document.querySelector('.btn-three').addEventListener('click', function () {
    const fio = document.querySelector('input[name="person"]').value;
    const address = document.querySelector('input[name="address"]').value;
    const productIds = document.querySelectorAll('input[name="product_id"]').value; // Пример массива с id продуктов

    const requestData = {
        fio: fio,
        address: address,
        product_ids: productIds
    };

    fetch('/path/to/order_view/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Ошибка:', error);
        });
});