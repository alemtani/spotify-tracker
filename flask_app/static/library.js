let userId;

function getResults() {
    clearResults();
    const filters = [];
    $('input[name="status"]:checked').each(function() {
        filters.push($(this).val());
    });
    $.getJSON($SCRIPT_ROOT + '/user/' + userId + '/trackers', {
        item: $('input[name="item"]:checked').val(),
        status: filters.join(',')
    }, processResults);
}

$(function() {
    userId = $('#userId').val();
    $('input[name="item"]').on('change', getResults);
    $('input[name="status"]').on('change', getResults);
});