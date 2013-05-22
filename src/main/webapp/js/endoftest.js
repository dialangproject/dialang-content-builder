$('#next').click(function () { window.location.href = '../feedbackmenu/' + dialang.session.al + '.html'; });

var testsDone = [];
var testsDoneString = sessionStorage.getItem("testsDone");
if(testsDoneString) {
    testsDone = JSON.parse(testsDoneString);
}
testsDone.push(dialang.session.tl + '-' + dialang.session.skill);
sessionStorage.setItem('testsDone',JSON.stringify(testsDone));
