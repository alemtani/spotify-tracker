let userId;

function getResults() {
    clearResults();
    $.getJSON($SCRIPT_ROOT + '/user/' + userId + '/trackers', {
        item: $('input[name="item"]:checked').val()
    }, processResults);
}

$(function() {
    userId = $('#userId').val();
    $('input[name="item"]').on('change', getResults);
});