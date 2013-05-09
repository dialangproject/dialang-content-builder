$(document).ready(function () {
    $(".valid-button").click(function () {
        var wordId = this.id.substring(0,this.id.indexOf('_'));
        $("[for=" + this.id + "]").html("<img src=\"../../../images/trueselected.gif\"/>");
        $("[for=" + wordId + "_incorrect]").html("<img src=\"../../../images/false.gif\"/>");
     });

     $(".invalid-button").click(function () {
        var wordId = this.id.substring(0,this.id.indexOf('_'));
        $("[for=" + this.id + "]").html("<img src=\"../../../images/falseselected.gif\"/>");
        $("[for=" + wordId + "_correct]").html("<img src=\"../../../images/true.gif\"/>");
     });

     $('.word').click(function () {
        var wordId = this.id.substring(0,this.id.indexOf('_'));
        answered[wordId] = true;
        var wordsSelected = $('.word');
        if(wordsSelected.length == 27) {
        }
        var allAnswered = true;
        for(var id in answered) {
            if(!answered[id]) allAnswered = false;
        }
        if(allAnswered) {
            $('#send-button').removeAttr('disabled');
            $('#next').removeAttr('disabled');
        }
    });
});

$(document).keydown(function (e) {
    if(e.keyCode == '72' && e.ctrlKey) {
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('.correct').click();
        $('#next').click(function () { $('#confirmation-dialog').dialog('open'); });
    } else if(e.keyCode == '77' && e.ctrlKey) {
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('.incorrect').click();
        $('#next').click(function () { $('#confirmation-dialog').dialog('open'); });
    } else if(e.keyCode == '76' && e.ctrlKey) {
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('.incorrect').click();
        $('#next').click(function () { $('#confirmation-dialog').dialog('open'); });
    }
});

$('#send-button').click( function (e) { $('#confirmation-dialog').dialog('open'); });
$('#confirmation-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirmation_yes').click(function (e) { $('#vsptform').submit(); });
$('#confirmation_no').click(function (e) { $('#confirmation-dialog').dialog('close'); });
$('#skipforward').click(function () { window.location.href = '/{{al}}/sa'; });
