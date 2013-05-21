$('#progressbar').progressbar({max: dialang.session.totalItems, value: dialang.session.itemsCompleted});

$('#next').click(function() { $('#basketform').submit(); });

$('#confirm-skip-dialog').dialog({modal: true, width: 500, height: 450, autoOpen: false});
$('#confirm-skip-yes').click(function (e) {
    document.location.href = '../../endoftest/' + dialang.session.al + '.html';
});
$('#confirm-skip-no').click(function (e) { $('#confirm-skip-dialog').dialog('close'); });
$('#skipforward').click(function () {
    $('#confirm-skip-dialog').dialog('open');
    return false;
});

$('.review-dialog').dialog({modal: false,
                            width: 500,
                            height: 450,
                            autoOpen: false,
                            close: function(event,ui) {
                                window.location.href = '../../itemreview/' + dialang.session.al + '.html';
                            }});

// If this page has been reached from itemreview, there should be a basket
// in sessionStorage. Let's check.
var basketString = sessionStorage.getItem('basket');
if(basketString) {

    // We're in item review mode


    // Setup the toolbar appropriately
    $('#back')
        .prop("disabled",false)
        .click(function() { window.location.href = '../../itemreview/' + dialang.session.al + '.html'; });
    $('#next').off('click').prop("disabled",true);
    $('#skipforward').prop("disabled",true);

    var basket = JSON.parse(basketString);

    if(basket.type == 'mcq' ) {
        if(basket.items.length == 1) {
            // MCQ baskets only ever have one item.
            var item = basket.items[0];
            $('#mcq-review-dialog').dialog('open');
            $('.ui-dialog-titlebar-close span').removeClass('ui-icon-closethick').addClass('ui-icon-prevButton');
            if(!item.correct) {
                $('.review-smiley > img').attr('src','../../images/frowney.gif');
            }
            $('.review-given-answer p').html(item.responseText);
            for(var i=0,j=item.answers.length;i<j;i++) {
                if(item.answers[i].correct) {
                    $('.review-correct-answer p').html(item.answers[i].text);
                }
            }
            $("input[value=\"" + item.responseId + "\"]").prop("checked",true);
        } else if(basket.items.length > 1) {

            // This is a tabbedpane basket

            var initialItemId = sessionStorage.getItem('itemId');

            // Get the yourAnswer and correctAnswer texts from the hidden form elements.
            var yourAnswerTitle = $('#review-dialog-youranswer-title').val();
            var correctAnswerTitle = $('#review-dialog-correctanswer-title').val();

            $.get('/templates/tabbedpanereview.mustache',function(template) {

                // Render the dialog markup
                var output = Mustache.render(template, {'items':basket.items,'yourAnswerTitle':yourAnswerTitle,'correctAnswerTitle':correctAnswerTitle});
                $('#tp-review-dialog').html(output);

                // Set up the image for each item
                for(var i=0,j=basket.items.length;i<j;i++) {
                    if(!basket.items[i].correct) {
                        $('#reviewtab-' + basket.items[i].id + ' > div > img').attr('src','../../images/frowney.gif');
                    }
                }

                $(document).ready(function() {
                        $("#review-tabs").tabs({
                            select:function(event,ui) {
                                    var itemId = $(ui.panel).attr('item-id');
                                    var index = $('#tabbedpane-tabs a[href="#tabs-' + itemId + '"]').parent().index();
                                    $("#tabbedpane-tabs").tabs('option','active',index);
                                }
                        });
                        var initialIndex = $('#tabbedpane-tabs a[href="#tabs-' + initialItemId + '"]').parent().index();
                        $("#tabbedpane-tabs").tabs('option','active',initialIndex);
                        $("#review-tabs").tabs('option','active',initialIndex);
                    })

                $('#tp-review-dialog').dialog('open');
                $('.ui-dialog-titlebar-close span').removeClass('ui-icon-closethick').addClass('ui-icon-prevButton');
            });

            // This is a tabbebpane basket as it has multiple mcq items
            for(var i=0,j=basket.items.length;i<j;i++) {
                var item = basket.items[i];
                $("input[value=\"" + item.responseId + "\"]").prop("checked",true);
            }
        }
    } else if(basket.type == 'gapdrop') {
        for(var i=0,j=basket.items.length;i<j;i++) {
            var item = basket.items[i];
            $("option[value=\"" + item.responseId + "\"]").prop("selected",true);
        }
    } else if(basket.type == 'shortanswer' || basket.type == 'gaptext') {
        for(var i=0,j=basket.items.length;i<j;i++) {
            var item = basket.items[i];
            $("input[name=\"" + item.id + "-response\"]").val(item.responseText);
        }
    }
}
