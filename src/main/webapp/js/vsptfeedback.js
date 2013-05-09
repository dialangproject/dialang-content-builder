$('#score').html(dialang.session.vsptMearaScore);
$("#vsptfeedback-tabs").tabs({ active: activeTab }).addClass( "ui-tabs-vertical ui-helper-clearfix" );
$( "#vsptfeedback-tabs li" ).removeClass( "ui-corner-top" ).addClass( "ui-corner-left" );

var fbMenuPage = sessionStorage.getItem('feedbackMenuPage');

if(fbMenuPage) {
    $('#next').prop('disabled',true);
    $('#back').removeProp('disabled');
    $('#back').click(function() { window.location.href = fbMenuPage; });
} else {
    // There is no SA for structures or vocabulary tests
    if(dialang.session.skill === 'vocabulary' || dialang.session.skill === 'structures') {
        $('#next').click(function() { window.location.href = '../../testintro/' + dialang.session.al + '.html'; });
    } else {
        $('#next').click(function() { window.location.href = '../../saintro/' + dialang.session.al + '/' + dialang.session.skill + '.html'; });
    }
}
