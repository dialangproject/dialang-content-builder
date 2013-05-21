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
        $('#next').click(function () { $('#confirm-send-dialog').dialog('open'); });
        e.preventDefault();
        return false;
    } else if(e.keyCode == '77' && e.ctrlKey) {
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('.incorrect').click();
        $('#next').click(function () { $('#confirm-send-dialog').dialog('open'); });
        e.preventDefault();
        return false;
    } else if(e.keyCode == '76' && e.ctrlKey) {
        $('#send-button').removeAttr('disabled');
        $('#next').removeAttr('disabled');
        $('.incorrect').click();
        $('#next').click(function () { $('#confirm-send-dialog').dialog('open'); });
        e.preventDefault();
        return false;
    }
});

$('#confirm-send-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirm-send-yes').click(function (e) { $('#vsptform').submit(); });
$('#confirm-send-no').click(function (e) { $('#confirm-send-dialog').dialog('close'); });

$('#send-button').click( function (e) { $('#confirm-send-dialog').dialog('open'); });

$('#confirm-skip-dialog').dialog({modal: true, width: 400, height: 250, autoOpen: false});
$('#confirm-skip-yes').click(dialang.skipVSPT)
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });

$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});
