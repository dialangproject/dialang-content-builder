$(document).ready(function () {
    $(".valid-button").click(function () {
        var statementId = this.id.substring(0,this.id.indexOf('_'));
        $("[for=" + this.id + "]").html("<img src=\"../../../images/trueselected.gif\"/>");
        $("[for=" + statementId + "_invalid]").html("<img src=\"../../../images/false.gif\"/>");
    });
    $(".invalid-button").click(function () {
        var statementId = this.id.substring(0,this.id.indexOf('_'));
        $("[for=" + this.id + "]").html("<img src=\"../../../images/falseselected.gif\"/>");
        $("[for=" + statementId + "_valid]").html("<img src=\"../../../images/true.gif\"/>");
    });

    $('.statement').click(function () {
        var statementId = this.id.substring(0,this.id.indexOf('_'));
        answered[statementId] = true;
        var statementsSelected = $('.statement');
        if(statementsSelected.length == 27) {
        }
        var allAnswered = true;
        for(var id in answered) {
            if(!answered[id]) allAnswered = false;
        }
        if(allAnswered) {
            $('#send-button').removeAttr('disabled');
            $('#next')
                .removeAttr('disabled')
                .click( function (e) {
                    $('#confirm-send-dialog').dialog('open');
                });
        }
    });
});

$(document).keydown(function (e) {
    if(e.keyCode == '72' && e.ctrlKey) {
        $('.valid-button').attr('checked','checked');
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('#cheatlevel').val('high');
    } else if(e.keyCode == '76' && e.ctrlKey) {
        $('.invalid-button').attr('checked','checked');
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('#cheatlevel').val('low');
    }
});

$('#confirm-send-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirm-send-yes').click(function (e) { $('#saform').submit(); });
$('#confirm-send-no').click(function (e) { $('#confirm-send-dialog').dialog('close'); });

$('#next').click( function (e) {
    $('#confirm-send-dialog').dialog('open');
});
$('#send-button').click( function (e) {
    $('#confirm-send-dialog').dialog('open');
});

$('#confirm-skip-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirm-skip-yes').click(function (e) {
    document.location.href = '../../testintro/' + dialang.session.al + '.html';
});
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });

$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});
