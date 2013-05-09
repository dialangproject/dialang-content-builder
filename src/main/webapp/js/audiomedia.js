$(document).ready(function() {
    var audio = document.getElementById('audio');
    var playButton = $('#playaudio');
    audio.oncanplaythrough = playButton.removeProp('disabled');
    playButton.click(function(e) {
        audio.play();
        $(this).prop('disabled',true);
    });
});
