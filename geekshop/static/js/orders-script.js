$(document).ready(function() {
    let _quantity, _price, orderitem_num, delta_quantity, orderitem_quantity, delta_cost;
    let oldSelectedValue;
    let newProductPrice;

    let quantity_arr = []
    let price_arr = []

    let total_forms = parseInt($('input[name=orderitems-TOTAL_FORMS]').val());

    let order_total_quantity = parseInt($('.order_total_quantity').text()) || 0;
    let order_total_price = parseFloat($('.order_total_cost').text()) || 0;

    for (let i = 0; i < total_forms; i++) {
        _quantity = parseInt($('input[name=orderitems-' + i + '-quantity]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantity_arr[i] = _quantity;
        if (_price) {
            price_arr[i] = _price;
        } else {
            price_arr[i] = 0;
        }
    }

    $('.order_form').on('click', 'input[type=number]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-quantity', ''));
        if (price_arr[orderitem_num]) {
            orderitem_quantity = parseInt(target.value);
            delta_quantity = orderitem_quantity - quantity_arr[orderitem_num];
            quantity_arr[orderitem_num] = orderitem_quantity;

            orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
        }
    });

    $('.order_form').on('click', 'input[type=checkbox]', function () {
        let target = event.target;
        orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-DELETE', ''));
        if (target.checked) {
            delta_quantity = -quantity_arr[orderitem_num];
        } else {
            delta_quantity = quantity_arr[orderitem_num];
        }

        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity);
    });

    function orderSummaryUpdate(orderitem_price, delta_quantity) {
        delta_cost = orderitem_price * delta_quantity;
        order_total_price = Number((order_total_price + delta_cost).toFixed(2));
        order_total_quantity = order_total_quantity + delta_quantity;

        $('.order_total_quantity').text(order_total_quantity.toString());
        $('.order_total_cost').text(order_total_price.toString());
    }

    $('.formset_row').formset({
        addText: 'Добавить продукт',
        deleteText: 'Удалить',
        prefix: 'orederitems',
        removed: deleteOrderItem,
    });

    function deleteOrderItem(row) {
        let target_name = row[0].querySelector('input[type=number]').name;
        orderitem_num = parseInt(target_name.replace('orderitem-', '').replace('quantity', ''));

        delta_quantity = -quantity_arr[orderitem_num];
        orderSummaryUpdate(price_arr[orderitem_num], delta_quantity)
    }

    $('.order_form').on('click', 'select', function () {
        let target = event.target;
        if (target.tagName == 'SELECT') {
            orderitem_num = parseInt(target.name.replace('orderitems-', '').replace('-product', ''));
            oldSelectedValue = target.selectedOptions[0].value;
        } else if (target.tagName == 'OPTION') {
            const newSelectedValue = target.value;
            if (newSelectedValue) {
                if (newSelectedValue != oldSelectedValue) {
                    $.ajax({
                        url: '/order/get-product-price/' + newSelectedValue,
                        success: function (data) {
                            if (data.price) {
                                $('.orderitems-' + orderitem_num + '-price').text(data.price);
                                const oldProductCost = Number((price_arr[orderitem_num] * quantity_arr[orderitem_num]).toFixed(2));
                                const newProductCost = Number((Number(data.price) * quantity_arr[orderitem_num]).toFixed(2));
                                order_total_price = order_total_price - oldProductCost + newProductCost;
                                price_arr[orderitem_num] = Number(data.price);
                                $('.order_total_cost').text(order_total_price.toString());
                            }
                        }
                    });
                }
            }
        }
    });
});