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
                    $('#confirmation-dialog').dialog('open');
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

$('#send-button').click( function (e) {
    $('#confirmation-dialog').dialog('open');
});
$('#next').click( function (e) {
    $('#confirmation-dialog').dialog('open');
});
$('#confirmation-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirmation_yes').click(function (e) { $('#saform').submit(); });
$('#confirmation_no').click(function (e) { $('#confirmation-dialog').dialog('close'); });
$('#skipforward').click(function () { window.location.href = '/{{al}}/sa'; });
