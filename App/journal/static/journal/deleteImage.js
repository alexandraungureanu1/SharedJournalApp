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


$(document).on('click', '.alink', function () {
    var url = $(this).next('.delete-url').data('url');

    console.log(url);
    $.ajax({
        type: 'POST',
        url: url,
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: function (response) {
            $(this).parent().remove();
            window.location.reload();
        },
        error: function (xhr, status, error) {
            console.log(error);
        }
    });
});
