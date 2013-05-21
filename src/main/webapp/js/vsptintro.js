$('#next').click(function () { window.location.href = '../vspt/' + dialang.session.al + '/' + dialang.session.tl + '.html'; });
$('#back').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#confirm-skip-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirm-skip-yes').click(dialang.skipVSPT)
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });
$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});
