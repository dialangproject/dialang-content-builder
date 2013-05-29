$('#disclaimer-button').click(function(e) { $('#disclaimer-dialog').dialog('close'); });

$('#back').click(function () { window.location.href = '../flowchart/' + dialang.session.al + '.html'; });
$('#skipback').click(function () { window.location.href = '../als.html'; });
$('.tls-link').on('click', function () {
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

// We need to do this in case this isn't the first run
sessionStorage.removeItem('reviewBasket');
sessionStorage.removeItem('reviewItemId');
sessionStorage.removeItem('feedbackMenuPageUrl');

// Disable the completed tests
var testsDone = [];
var testsDoneString = sessionStorage.getItem('testsDone');
if(testsDoneString) {
    testsDone = JSON.parse(testsDoneString);
}

for(var i=0,j=testsDone.length;i<j;i++) {
    $('#' + testsDone[i])
        .off('click')
        .attr('href','javascript:;')
        .children('img').attr('src','../../images/done.gif');
}
