$('#back').click(function () { window.location.href = '../../../feedbackmenu/' + dialang.session.al + '.html'; });

$('.dialog').dialog({autoOpen: false, width: 500, height: 450});

function launchDialog(number) {
    $('.dialog').dialog('close');
    $('#dialog' + number).dialog('open');
}
