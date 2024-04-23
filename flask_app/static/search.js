let counter = 0;

function processResultsSearch(results) {
    processResults(results);
    if (results.data.length === 0) return;
    $('#loader').removeClass('invisible');
    counter += results.data.length;
}

function getResults() {
    counter = 0; // reset counter
    clearResults();
    if (!$('#loader').hasClass('invisible')) $('#loader').addClass('invisible');
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val()
    }, processResultsSearch);
}

function loadMoreResults() {
    $('#spinner').removeClass('invisible');
    $('#loader').addClass('invisible');
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val(),
        offset: counter
    }, processResultsSearch);
}

$(function() {
    $('#q').on('change', getResults);
    $('input[name="item"]').on('change', getResults);
    $('#loader').on('click', loadMoreResults);
});