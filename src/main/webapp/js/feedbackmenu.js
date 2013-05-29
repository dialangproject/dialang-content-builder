$('#skipback').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#skipforward').click(function () {
    $('#confirm-restart-dialog').dialog('open');
    return false;
});

$('#confirm-restart-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirm-restart-yes').click(function (e) {
    document.location.href = '../tls/' + dialang.session.al + '.html';
});
$('#confirm-restart-no').click(function (e) { $('#confirm-restart-dialog').dialog('close'); });
$('#confirm-restart-quit').click(function (e) { window.close(); });

$('#about-sa-button').prop('disabled',true)

if(dialang.session.itemsCompleted) {
    $('#check-answers-button').click(function(e) {
        window.location.href = '../itemreview/' + dialang.session.al + '.html';
    });
} else {
    $('#check-answers-button').prop('disabled',true)
}

if(dialang.session.testDone) {
    $('#your-level-button').click(function(e) {
        window.location.href = '../testresults/' + dialang.session.al + '/' + dialang.session.skill + '/' + dialang.session.itemLevel + '.html';
    });
} else {
    $('#your-level-button').prop('disabled',true)
    $('#sa-feedback-button').prop('disabled',true);
    $('#advice-button').prop('disabled',true);
}


if(dialang.session.vsptDone) {
    $('#placement-test-button').click(function(e) {
        // Set a sessionStorage variable to let the vspt feedback page wire up the back button correctly
        sessionStorage.setItem('feedbackMenuPageUrl',window.location.href);
        window.location.href = '../vsptfeedback/' + dialang.session.al + '/' + dialang.session.vsptLevel + '.html';
    });
} else {
    $('#placement-test-button').prop('disabled',true);
}

if(dialang.session.saDone) {
    $('#sa-feedback-button').click(function(e) {
        window.location.href = '../safeedback/' + dialang.session.al + '/' + dialang.session.itemLevel + '/' + dialang.session.saLevel + '.html';
    });
} else {
    $('#sa-feedback-button').prop('disabled',true);
}
