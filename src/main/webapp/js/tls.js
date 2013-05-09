$('#disclaimer-button').click(function(e) { $('#disclaimer-dialog').dialog('close'); });

$('#back').click(function () { window.location.href = '../flowchart/' + dialang.session.al + '.html'; });
$('#skipback').click(function () { window.location.href = '../als.html'; });
$('.tls-link').click(function () {
    var langskill = $(this).attr('title');
    $('#confirmation_langskill').html(langskill);
    var href = $(this).attr('href');
    $('#confirmation_yes').click(function (e) { document.location.href = href; });
    $('#confirmation-dialog').dialog('open');
    return false;
});
$('#disclaimer-dialog').dialog({modal: true, width: 500, height: 450});
$('#confirmation-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirmation_no').click(function (e) { $('#confirmation-dialog').dialog('close'); });
