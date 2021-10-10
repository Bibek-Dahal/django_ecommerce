$('input[type=radio][name=id]').change(function () {
    $('#su').val(`https://bibekecom.herokuapp.com/cart/v-esewa/?cid=${this.value}`);
    console.log($('#su').val())
});
let uuid = $('#u').val();

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
var config = {
    publicKey: "test_public_key_2cb744b91026476980e513bd0c377ef2",
    productIdentity: '{{uuid}}',
    productName: "Dragon",
    productUrl: "http://gameofthrones.wikia.com/wiki/Dragons",
    paymentPreference: [
        "KHALTI",
        "EBANKING",
        "MOBILE_BANKING",
        "CONNECT_IPS",
        "SCT",
    ],
    eventHandler: {

        onSuccess(payload) {
            $(".container").addClass("d-none");
            $("#spin").attr("class", "d-flex justify-content-center");
            $.ajax({
                type: 'post',
                url: '/cart/verify/',
                data: {
                    token: payload.token,
                    amount: payload.amount,
                    csrfmiddlewaretoken: csrftoken
                },
                success: (response) => {

                    if (response.msg == "success") {

                        $('#payment_form').submit();
                    } else {
                        window.location.href = '/cart/transaction-failed'
                    }

                },
                error: (error) => {
                    ///.log(error)

                }
            });


        },
        onError(error) {
            ///.log(error);
        },
        onClose() {
            ///.log("widget is closing");
        },
    },
};

var checkout = new KhaltiCheckout(config);
var btn = document.getElementById("payment-button");
btn.onclick = function () {

    if ("{{request.user}}" === "AnonymousUser") {
        window.location.href = "{% url 'account:signup'%}";
    } else {
        checkout.show({
            amount: 1000
        });
    }
};