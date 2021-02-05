'use strict';
//Преобразования числа для удобного парса десятичных чисел(убрать пробелы и поменнять запятую на точку)
const pFloat = a => {
    let res = a + '';
    res = res.replace(/,/, '.');
    res = res.replace(/\s/, '');
    return parseFloat(res)
}

//Сделать цену красивой(добавить пробелы по 3 разряда и поменять точку на запятую),
// по сути, предыдущая функция наоборот
const beautifyFloat = num => {
    const n = parseInt(num);
    if (!((n ^ 0) === n)) {
        const intPart = Math.trunc(n);
        const floatPart = n - intPart;
        const resFloat = (floatPart + '').replace(/^0+/, '').replace(/\./, ',');

        const resInt = reversed.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ');

        return resInt + resFloat
    } else {
        let res = n + '';
        res = res.replace(/(\d)(?=(\d\d\d)+([^\d]|$))/g, '$1 ');

        return res + ',00'
    }
}


window.onload = () => {
    let _quantity, _price, orderItemNum, deltaQuantity, orderItemQuantity, deltaCost;
    const quantityArray = [];
    const priceArray = [];

    const TOTAL_FORMS = parseInt(document.querySelector('input[name=orderitems-TOTAL_FORMS]').getAttribute('value'));
    let orderTotalQuantity = parseInt(document.querySelector('.order_total_quantity').innerText) || 0;
    let orderTotalPrice = document.querySelector('.order_total_cost').innerText || 0;
    if (orderTotalPrice !== 0) {
        orderTotalPrice = pFloat(orderTotalPrice);
    }

    for (let i = 0; i < TOTAL_FORMS - 1; i++) {
        _quantity = parseInt(document.querySelector('input[name=orderitems-' + i + '-quantity]').getAttribute('value'));
        _price = pFloat(document.querySelector('.orderitems-' + i + '-price').innerText);

        quantityArray[i] = _quantity;
        if (_price) {
            priceArray[i] = _price;
        } else {
            priceArray[i] = 0;
        }
    }


    const orderSummaryUpdate = (itemPrice, deltaQuantity) => {
        deltaCost = itemPrice * deltaQuantity;
        orderTotalPrice = pFloat(orderTotalPrice);
        orderTotalPrice = (orderTotalPrice + parseInt(deltaCost)).toFixed(2);
        orderTotalPrice = beautifyFloat(orderTotalPrice);


        orderTotalQuantity = orderTotalQuantity + deltaQuantity;

        document.querySelector('.order_total_quantity').innerText = orderTotalQuantity.toString();
        document.querySelector('.order_total_cost').innerText = orderTotalPrice;
    }


    document.querySelector('body').addEventListener('click', event => {
        const target = event.target;
        if (event.target.tagName === 'INPUT' && event.target.type === 'number') {
            orderItemNum = parseInt(target.name.replace(/orderitems-/, '').replace(/-quantity/, ''))
            if (priceArray[orderItemNum]) {
                orderItemQuantity = parseInt(target.value);
                deltaQuantity = orderItemQuantity - quantityArray[orderItemNum];
                quantityArray[orderItemNum] = orderItemQuantity;
                orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
            }
        }

        if (event.target.tagName === 'INPUT' && event.target.type === 'checkbox') {
            orderItemNum = parseInt(target.name.replace(/orderitems-/, '').replace(/-DELETE/, ''));
            if (target.checked) {
                deltaQuantity = -quantityArray[orderItemNum];
            } else {
                deltaQuantity = quantityArray[orderItemNum];
            }
            orderSummaryUpdate(priceArray[orderItemNum], deltaQuantity);
        }
    });
}