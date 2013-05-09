$(document).ready(function() { $("#tabbedpane-tabs").tabs(); })

$("#radios > input").click(function(e) {

    var basketId = $(this).attr('basketId');
    $("#" + basketId + "-tab").addClass("completed-basket");

    var complete = true;
    for(var i=0,j=itemIds.length;i<j;i++) {
        if($('input[name=' + itemIds[i] + '-response]:checked').length == 0) {
            complete = false;
        }
    }

    if(complete) {
        $('#next').removeProp('disabled');
    } else {
        $('#next').prop('disabled',true);
    }
});
