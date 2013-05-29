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
$('#confirm-skip-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirm-skip-yes').click(function (e) {
    document.location.href = '../endoftest/' + dialang.session.al + '.html';
});
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });
$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});

