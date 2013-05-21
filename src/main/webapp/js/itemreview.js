$('#back').click(function () {
        window.location.href = '../feedbackmenu/' + dialang.session.al + '.html';
    });

function viewBasket(basketId) {
    window.location.href = "../baskets/" + dialang.session.al + "/" + basketId + ".html";
}

$(document).ready(function() {

    $.ajax({
        url:'/dialang/mysession/items.json',
        dataType:'json',
        success: function(items,textStatus,xhr) {

            var skill = '';

            // Loop through the items and collect them by basket, subskill and correctness
            var subskills = {};
            var baskets = {};
            var itemToBasketMap = {};
            var type = '';
            for(var i=0,j=items.length;i<j;i++) {

                var item = items[i];

                if(item.itemType == 'mcq' || item.itemType == 'gapdrop') {
                    // Set the response text on this item
                    for(var k=0,m=item.answers.length;k<m;k++) {
                        var answer = item.answers[k];
                        if(answer.correct) {
                            item.correctAnswer = answer.text;
                        }
                        if(answer.id == item.responseId) {
                            item.responseText = answer.text;
                        }
                    }
                }
                
                // We use this to display an item number to the user
                item.index = i + 1;

                // These should probably be in a basket object
                skill = item.skill;
                type = item.itemType;

                var subskill = item.subskill;
                if(!subskills[subskill]) {
                    // No subskill keyed yet, ensure that one is.
                    subskills[subskill] = {'correct':[],'incorrect':[]};
                }

                if(item.correct) {
                    subskills[subskill].correct.push(item);
                } else {
                    subskills[subskill].incorrect.push(item);
                }

                // Collect the items into baskets
                var basketId = item.basketId;
                if(!baskets[basketId]) {
                    // No basket keyed yet, ensure that one is.
                    baskets[basketId] = {'type':type,'items':[]};
                }
                baskets[basketId].items.unshift(item);

                // Map the item id onto the basket id for lookup later.
                itemToBasketMap[item.id] = basketId;

            } // end items loop

            var rows = [];
            for(subskillKey in subskills) {
                var fullSubskill = skill + '.' + subskillKey;
                var subskill = subskills[subskillKey];
                rows.push({
                            'description':subskillLookup[fullSubskill],
                            'correct':subskill.correct,
                            'incorrect':subskill.incorrect });
            }

            // Build the table using mustache
            $.get('/templates/itemreviewtable.mustache',function(template) {
                var output = Mustache.render(template, {'rows':rows});
                $('#item-table').html(output);
                $('.itemreview-button').click(function (e) {
                    var clickedItem = null;
                    for(var i=0,j=items.length;i<j;i++) {
                        // The button id is the item id
                        if(items[i].id == this.id) {
                            clickedItem = items[i];
                            break;
                        }
                    }

                    if(clickedItem !== null) {
                        sessionStorage.setItem('basket',JSON.stringify(baskets[itemToBasketMap[clickedItem.id]]));
                        window.location.href = '../baskets/' + dialang.session.al + '/' + clickedItem.basketId + '.html';
                    } else {
                        alert('BOOOO');
                    }
                });
            });
        },
        error: function(jqXHR,textStatus,errorThrown) {
        }
    });
});
