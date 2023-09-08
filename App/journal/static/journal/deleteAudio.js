function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$(document).on('click', '.delete-audio', function () {
    var url = $(this).next('.delete-audio-url').data('url');
    $('#loading-spinner').show();

    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function (xhr, settings) {
            $('#loading-spinner').show();
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function (response) {
            $('#loading-spinner').hide();
            window.location.reload();
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
});
