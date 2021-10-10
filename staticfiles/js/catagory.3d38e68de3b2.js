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
  
  function addToCart(id, price, title) {
    ////console.log("add_to_cart clicked");
    $.ajax({
      method: "post",
      url: "/cart/add-to-cart/",
      data: {
        id: id,
        title: title,
        price: price,
        quantity: 1,
        csrfmiddlewaretoken: csrftoken,
      },
      success: (response) => {
        ////console.log(response);
        ////console.log('length',response.length);
        $('#cart-quan').html(response.length);
      },
    });
  }
  $(".container").hide();
  $(window).on("load", function () {
    ////console.log("window loaded");
    $("#spin").remove();
    $(".container").show();
  
  });