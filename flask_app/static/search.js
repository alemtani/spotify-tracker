let counter = 0;

function getResults() {
    counter = 0; // reset counter
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val()
    }, function(results) {
        if (results.data.length === 0) return;
        $('#album-list').empty();
        $('#track-list').empty();
        results.data.forEach(function(result) {
            if (results['type'] == 'album') {
                addAlbum(result);
            } else {
                addTrack(result);
            }
        });
        $('#loader').removeClass('invisible');
        counter += results.data.length;
    });
}

function loadMoreResults() {
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val(),
        offset: counter
    }, function(results) {
        if (results.data.length === 0) return;
        results.data.forEach(function(result) {
            if (results['type'] == 'album') {
                addAlbum(result);
            } else {
                addTrack(result);
            }
        });
        counter += results.data.length;
    });
}

$(function() {
    $('#q').on('change', getResults);
    $('input[name="item"]').on('change', getResults);
    $('#loader').on('click', loadMoreResults);
});