$(function() {
    $("a.nav-link").click(function() {
        $("html, body").animate({
            scrollTop: $($(this).attr("href")).offset().top - 56
        });
    });
});
