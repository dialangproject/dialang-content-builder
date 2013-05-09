$('#next').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#back').click(function () { window.location.href = '../legend/' + dialang.session.al + '.html'; });

$('.dialog').dialog({autoOpen: false, width: 500, height: 450});

function launchDialog(number) {
    $('.dialog').dialog('close');
    $('#dialog' + number).dialog('open');
}
