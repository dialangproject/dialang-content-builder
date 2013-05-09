$('#skipback').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#skipforward').click(function () { window.location.href = '../tls/' + dialang.session.al + '.html'; });
$('#your-level-button').click(function(e) {
    window.location.href = '../testresults/' + dialang.session.al + '/' + dialang.session.skill + '/' + dialang.session.itemLevel + '.html';
});
$('#placement-test-button').click(function(e) {
    // Set a cookie variable to let the vspt feedback page wire up the back button correctly
    sessionStorage.setItem('feedbackMenuPage',window.location.href);
    window.location.href = '../vsptfeedback/' + dialang.session.al + '/' + dialang.session.vsptLevel + '.html';
});
$('#sa-feedback-button').click(function(e) {
    window.location.href = '../safeedback/' + dialang.session.al + '/' + dialang.session.itemLevel + '/' + dialang.session.saLevel + '.html';
});
