var dialang = { session: {} };

var nameEQ = "DIALANG=";
var ca = document.cookie.split(';');
for(var i=0,j=ca.length;i<j;i++) {
    var c = ca[i];
    // Trim leading whitespace
    c = c.replace(/^\s*/,'');
    // If this is the DIALANG cookie, parse it.
    if (c.indexOf(nameEQ) == 0) {
        var dialangCookie = unescape(c.substring(nameEQ.length,c.length));
        var pairs = dialangCookie.split("|");
        for(var i=0,j=pairs.length;i<j;i++) {
            var pair = pairs[i].split("=");
            dialang.session[pair[0]] = pair[1];
        }
    }
}

dialang.skipVSPT = function () {
    if(dialang.session.skill === 'structures' || dialang.session.skill === 'vocabulary') {
        document.location.href = '../testintro/' + dialang.session.al + '.html';
    } else {
        document.location.href = '../../saintro/' + dialang.session.al + '/' + dialang.session.skill + '.html';
    }
}

/*
$(document).ready(function() {  
          
    //this one line will disable the right mouse click menu  
     $(document)[0].oncontextmenu = function() {return false;}  
});
*/
