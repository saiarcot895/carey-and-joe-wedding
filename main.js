$(function() {
    $(document).ready(function() {
        $(".container-fluid").load("home.html");
    });

    $("ul.navbar-nav li").each(function() {
        $(this).on("click", function(){
            $(".container-fluid").load($(this).attr("data-page")+".html");
        });
    });


    //$("a.nav-link").click(function() {
    //    $("html, body").animate({
    //        scrollTop: $($(this).attr("href")).offset().top - 56
    //    });
    //});

    $("#nameLookupForm").submit(function(e) {
        // Prevent default functionality
        e.preventDefault();

        // Get the action URL of the form
        var actionurl = $(this).find("button").prop("formAction");

        // Do our own request and handle the results
        $.ajax({
            url: actionurl,
            type: "POST",
            dataType: "json",
            data: $("#nameLookupForm").find("input[name=firstName], input[name=lastName]").serialize(),
            jsonp: false,
            success: function(data) {
                $("#numGuestsInput").attr("value", data["numGuests"]);
                $("#attendingDay1Check").prop("checked", data["presentForDay1"]);
                $("#attendingDay2Check").prop("checked", data["presentForDay2"]);
                $("#rsvpEditForm").prop("disabled", false).slideDown();
            }
        });
    });

    $("#rsvpEditForm").submit(function(e) {
        // Prevent default functionality
        e.preventDefault();

        // Get the action URL of the form
        var actionurl = $(this).find("button").prop("formAction");

        // Do our own request and handle the results
        $.ajax({
            url: actionurl,
            type: "POST",
            dataType: "json",
            data: $("#nameLookupForm, #rsvpEditForm").find("input[name=firstName], input[name=lastName], input[name=numGuests], input[name=presentForDay1], input[name=presentForDay2], input[name=vegetarian]").serialize(),
            jsonp: false,
            success: function(data) {
            }
        });
    });
});
