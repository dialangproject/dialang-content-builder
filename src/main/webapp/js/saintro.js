$('#next').click(function() { window.location.href = '../../sa/' + dialang.session.al + '/' + dialang.session.skill + '.html'; });
$('#confirmation-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#skipforward').click(function () {
    $('#confirmation_yes').click(function (e) {
        document.location.href = '../../testintro/' + dialang.session.al + '.html';
    });
    $('#confirmation_no').click(function (e) { $('#confirmation-dialog').dialog('close'); });
    $('#confirmation-dialog').dialog('open');
    return false;
});
