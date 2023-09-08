const openCameraButton = document.getElementById('open-camera-button');
const cameraContainer = document.getElementById('camera-container');
const video = document.getElementById('video-preview');
const canvas = document.getElementById('canvas');
const captureButton = document.getElementById('capture-button');
const closeButton = document.getElementById('close-button');

openCameraButton.addEventListener('click', () => {
    cameraContainer.style.display = 'block';

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;

            video.onloadedmetadata = function () {
                // canvas dimensions to match the video dimensions
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
            };
        })
        .catch(error => {
            console.error('Error accessing webcam:', error);
        });
});

closeButton.addEventListener('click', () => {
    cameraContainer.style.display = 'none';

    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    video.srcObject = null;
});

// capture photo
captureButton.addEventListener('click', () => {
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const photoData = canvas.toDataURL('image/jpeg', 1);

    // send photo
    const csrfToken = getCookie('csrftoken');
    const url = document.getElementById('capture-url').value;

    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrfToken);
        },
        data: {
            photo: photoData
        },
        success: function (response) {
            $(this).parent().remove();
            if (response.redirect_url) {
                window.location.reload();
            } else {
                console.error('Redirect URL not found in the response.');
            }
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
});