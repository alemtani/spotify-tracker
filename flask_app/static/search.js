let counter = 0;

function appendAlbum(result) {
    $('#album-list').append(`
        <div class="col">
            <div class="card shadow-sm">
                <img class="bd-placeholder-img card-img-top" width="100%" src="${result['image']['url']}">
                <div class="card-body">
                    <h5 class="card-title">${result['name']}</h5>
                    <p class="card-text">${result['artists'].join()}</p>
                    <div class="d-flex justify-content-between align-items-center">
                        <a href="player/${result['id']}" class="btn btn-primary">Explore</a>
                        <small class="text-body-secondary">${result['release_date']}</small>
                    </div>
                </div>
            </div>
        </div>
    `);
}

function appendTrack(result) {
    const duration = Math.round(result['duration'] / 1000.0);
    const [minutes, seconds] = [Math.floor(duration / 60), duration % 60];
    $('#track-list').append(`
        <a href="player/${result['id']}" class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">
            <img src="${result['image']['url']}" alt="twbs" width="32" height="32" class="rounded-circle flex-shrink-0">
            <div class="row w-100">
                <div class="col-5">
                    <h6 class="mb-0">${result['name']}</h6>
                    <p class="mb-0 opacity-75">${result['artists'].join()}</p>
                </div>
                <div class="col-5">
                    <p class="mb-0">${result['album']}</p>
                </div>
                <div class="col-2 text-end">
                    <small class="opacity-50 text-nowrap">${minutes}:${seconds.toString().padStart(2, '0')}</small>
                </div>
            </div>
        </a>
    `);
}

function getSearchResults() {
    counter = 0; // reset counter
    $('#loader').hide();
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val()
    }, function(results) {
        if (results.data.length === 0) return;
        $('#album-list').empty();
        $('#track-list').empty();
        results.data.forEach(function(result) {
            if (results['type'] == 'album') {
                appendAlbum(result);
            } else {
                appendTrack(result);
            }
        });
        $('#loader').show();
        counter += results.data.length;
    });
}

function loadMoreSearchResults() {
    $.getJSON($SCRIPT_ROOT + '/search', {
        q: $('#q').val(),
        item: $('input[name="item"]:checked').val(),
        offset: counter
    }, function(results) {
        if (results.data.length === 0) return;
        results.data.forEach(function(result) {
            if (results['type'] == 'album') {
                appendAlbum(result);
            } else {
                appendTrack(result);
            }
        });
        counter += results.data.length;
    });
}

$(function() {
    $('#q').bind('change', getSearchResults);
    $('input[name="item"]').bind('change', getSearchResults);
    $('#loader').bind('click', loadMoreSearchResults);
    $('#loader').hide();
});