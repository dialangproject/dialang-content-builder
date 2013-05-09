$('#next').click(function () { window.location.href = '../vspt/' + dialang.session.al + '/' + dialang.session.tl + '.html'; });
$('#back').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#confirmation-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#skipforward').click(function () {
    $('#confirmation_yes').click(function (e) {
        if(dialang.session.skill === 'structures' || dialang.session.skill === 'vocabulary') {
            document.location.href = '../testintro/' + dialang.session.al + '.html';
        } else {
            document.location.href = '../saintro/' + dialang.session.al + '/' + dialang.session.skill + '.html';
        }
    });
    $('#confirmation_no').click(function (e) { $('#confirmation-dialog').dialog('close'); });
    $('#confirmation-dialog').dialog('open');
    return false;
});
