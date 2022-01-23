$(".yes-vac").click(function() {
    $("#reason-ta").removeAttr("required");
    $(".vac-reasoning").css({ "display": "none" })
    $(".appearing-form-wrap").css({ "display": "block" });
    $('html,body').animate({
        scrollTop: $("#scroll-yes").offset().top - 60
    });
})

$(".no-vac").click(function() {
    $("#reason-ta").prop("required", true);
    $(".vac-reasoning").css({ "display": "block" })
    $(".appearing-form-wrap").css({ "display": "block" });
    $('html,body').animate({
        scrollTop: $("#scroll-no").offset().top - 60
    });
})

var fewSeconds = 3;
$('#btnFetch').click(function() {
    var btn = $(this);
    setTimeout(function() {
        btn.prop('disabled', true);
    }, 50);
    setTimeout(function() {
        btn.prop('disabled', false);
    }, fewSeconds * 1000);
})