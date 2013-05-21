$('#next').click(function() { window.location.href = '../../sa/' + dialang.session.al + '/' + dialang.session.skill + '.html'; });
$('#confirm-skip-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirm-skip-yes').click(function (e) {
    document.location.href = '../../testintro/' + dialang.session.al + '.html';
});
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });
$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});
