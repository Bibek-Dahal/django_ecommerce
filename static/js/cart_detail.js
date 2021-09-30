
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie("csrftoken");
function addToCart(obj, id, price, title) {
    ////console.log("add_to_cart clicked");
    ////console.log("obj", obj);
}

function handleClick(obj, id, title, price) {
    ////console.log("add button clicked");
    ////console.log(`#${id}`);
    ////console.log($(`#${id}`).html());
    ////console.log("obj", obj.getAttribute("data-btn"));
    let name = obj.getAttribute("data-btn");

    if (name == "add_btn") {
        let value = parseInt($(`#${id}`).html());
        let finalVal = value + 1
        if (parseInt(finalVal) <= 3) {
            //obj.addClass('disabled')
            quantity = finalVal
            $.ajax({
                method: "post",
                url: "http://127.0.0.1:8000/cart/add-to-cart/",
                data: {
                    id: id,
                    title: title,
                    price: price,
                    quantity: quantity,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: (response) => {
                    // obj.attr('class','add_dec_btn shadow btn btn-primary btn-sm')
                    $(`.${id}`).html(`Rs${parseInt(response.data)}`);
                    $("#s_total").html(`Rs ${response.s_price.toFixed(2)}`);
                    $("#price").html(`Price(${response.length} items)`);
                    $("#total_charge").html(
                        `Rs ${response.total_charge.toFixed(2)}`
                    );
                    $("shipping_charge").html(
                        `Rs ${response.shipping_charge.toFixed(2)}`
                    );
                    $('#cart-quan').html(response.length)
                    $(`#${id}`).html(response.quantity);

                },
                error: (response) => {
                    //alert(response);
                },
            });
        }

    }

    if (name == "dec_btn") {

        let value = parseInt($(`#${id}`).html());
        ////console.log('value',value);
        let finalVal = value - 1;
        if (parseInt(finalVal) >= 1) {
            quantity = finalVal;
            $.ajax({
                method: "post",
                url: "http://127.0.0.1:8000/cart/add-to-cart/",
                data: {
                    id: id,
                    title: title,
                    price: price,
                    quantity: quantity,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: (response) => {
                    $(`.${id}`).html(`Rs${parseInt(response.data)}`);
                    $("#s_total").html(`Rs ${response.s_price.toFixed(2)}`);
                    $("#price").html(`Price(${response.length} items)`);
                    $("#total_charge").html(
                        `Rs ${response.total_charge.toFixed(2)}`
                    );
                    $("shipping_charge").html(
                        `Rs ${response.shipping_charge.toFixed(2)}`
                    );
                    $('#cart-quan').html(response.length)
                    $(`#${id}`).html(response.quantity);
                },
                error: (error) => {
                    //alert(error);
                },
            });
        }
       
    }
}

function removeCart(id) {
    $.ajax({
        method: "post",
        url: "http://127.0.0.1:8000/cart/remove-cart/",
        data: {
            pk: id,
            csrfmiddlewaretoken: csrftoken,
        },

        success: (response) => {
            //////console.log(response);
            obj = $(`[data-cart-container=${response.id}]`);
            obj.remove();
            $("#s_total").html(`Rs ${response.s_price.toFixed(2)}`);
            $("#price").html(`Price(${response.length} items)`);
            $("#total_charge").html(`Rs ${response.total_charge.toFixed(2)}`);
            $("shipping_charge").html(
                `Rs ${response.shipping_charge.toFixed(2)}`
            );
            $('#cart-quan').html(response.length)

            if (parseInt(response.length) == 0) {
                //////console.log("less then 0");
                $("#cart_detail").remove();
            }
        },
    });
}