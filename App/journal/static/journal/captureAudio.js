$(document).ready(function () {
    var myRecorder = {
        objects: {
            context: null,
            stream: null,
            recorder: null
        },
        init: function () {
            if (null === myRecorder.objects.context) {
                myRecorder.objects.context = new (
                    window.AudioContext || window.webkitAudioContext
                );
            }
        },
        start: function () {
            var options = { audio: true, video: false };
            navigator.mediaDevices.getUserMedia(options).then(function (stream) {
                myRecorder.objects.stream = stream;
                myRecorder.objects.recorder = new Recorder(
                    myRecorder.objects.context.createMediaStreamSource(stream),
                    { numChannels: 1 }
                );
                myRecorder.objects.recorder.record();
                $("#recording-indicator").show();
            }).catch(function (err) { });
        },
        stop: function () {
            if (null !== myRecorder.objects.stream) {
                myRecorder.objects.stream.getAudioTracks()[0].stop();
            }
            if (null !== myRecorder.objects.recorder) {
                myRecorder.objects.recorder.stop();

                myRecorder.objects.recorder.exportWAV(function (blob) {
                    var formData = new FormData();
                    formData.append('audio', blob, new Date().toUTCString() + '.wav');
                    const csrfToken = getCookie('csrftoken');
                    const url = document.getElementById('recording-url').value;

                    $.ajax({
                        url: url,
                        type: 'POST',
                        beforeSend: function (xhr, settings) {
                            xhr.setRequestHeader("X-CSRFToken", csrfToken);
                        },
                        data: formData,
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            $(this).parent().remove();
                            if (response.redirect_url) {
                                window.location.reload();
                            } else {
                                console.error('Redirect URL not found in the response.');
                            }
                        },
                    }).done(function (response) {
                    }).fail(function () {
                    });

                });
            }
        }
    };

    $('#start').on('click', function () {
        myRecorder.init();
        myRecorder.start();
    });

    $('#stop').on('click', function () {
        $("#recording-indicator").hide();
        myRecorder.stop();
    });
});
