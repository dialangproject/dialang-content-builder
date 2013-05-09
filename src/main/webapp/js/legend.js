$('#next').click(function () { window.location.href = '../flowchart/' + dialang.session.al + '.html'; });
$('#back').click(function () { window.location.href = '../als.html'; });

// This is intended for the vspt feedback screen, so it knows to
// navigate back to the feedback menu.
sessionStorage.removeItem('feedbackMenuPage');
