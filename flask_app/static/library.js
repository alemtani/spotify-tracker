function getResults(userId) {
    $.getJSON($SCRIPT_ROOT + '/user/' + userId + '/trackers', {
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
    });
}

$(function() {
    const userId = $('#userId').val();
    $('input[name="item"]').on('change', () => getResults(userId));
});