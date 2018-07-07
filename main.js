$(function() {
    $("a.nav-link").click(function() {
        $("html, body").animate({
            scrollTop: $($(this).attr("href")).offset().top - 56
        });
    });

    $("#rsvpContainer form").submit(function(e) {
        // Prevent default functionality
        e.preventDefault();

        // Get the action URL of the form
        var actionurl = $(this).find("button").prop("formAction");

        // Do our own request and handle the results
        $.ajax({
            url: actionurl,
            type: "POST",
            dataType: "json",
            data: $(this).find("input[name=firstName], input[name=lastName]").serialize(),
            jsonp: false,
            success: function(data) {
                $("#numGuestsInput").attr("value", data["numGuests"]);
                $("#attendingDay1Check").prop("checked", data["presentForDay1"]);
                $("#attendingDay2Check").prop("checked", data["presentForDay2"]);
                $("#rsvpContainer form fieldset:disabled").prop("disabled", false).slideDown();
            }
        });
    });
});
