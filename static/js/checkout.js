$('input[type=radio][name=id]'). change(function() {
    //alert(this.value);
    localStorage.setItem('cid',this.value)
    $('.su').attr('value',`http://127.0.0.1:8000/cart/v-esewa/?cid=${localStorage.getItem('cid')}`);
    //console.log(localStorage.getItem('cid'))
    //console.log($('.su').val())
    //console.log(window.location.href)
    // console.log($('.su').attr('value',`http://127.0.0.1:8000/cart/v-esewa/?cid=${localStorage.getItem('cid')}`))
    localStorage.removeItem('cid')
     
});