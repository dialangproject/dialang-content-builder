$('#next').click(function() { window.location.href = '/dialang/starttest'; });
$('#feedback-button').click(function() {
    var img = $(this).find('img');
    if(img.attr('src') == "../../images/instantFeedbackOff.gif") {
        $(this).attr('title','{{instantfeedbackofftooltip}}');
        img.attr('src',"../../images/instantFeedbackOn.gif");
    } else {
        $(this).attr('title','{{instantfeedbackontooltip}}');
        img.attr('src',"../../images/instantFeedbackOff.gif");
    }
});
