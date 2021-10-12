var position = 0;
$(document).scroll(function() {
    position = $(this).scrollTop();
    console.log(position);
    if (position > 140) {
        $(".navbar").css('background-color', 'white');
    } else {
        $(".navbar").css('background-color', 'transparent');
    }
});

$(".navbar-toggler").click(function() {
    if ($(".navbar").css('background-color', 'white') == false && position <= 140) {
        $(".navbar").css('background-color', 'white');
    }
    // if ($(".navbar").css('background-color', 'white') == true && position <= 140) {
    //     $(".navbar").css('background-color', 'transparent');
    // }
})