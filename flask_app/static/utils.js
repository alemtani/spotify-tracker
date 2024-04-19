function addAlbum(result) {
    $('#album-list').append(`
        <a class="col link-underline link-underline-opacity-0" href="${$SCRIPT_ROOT}/player/${result['id']}?item=album">
            <div class="card shadow-sm">
                <img class="bd-placeholder-img card-img-top" width="100%" src="${result['image']}">
                <div class="card-body">
                    <h5 class="card-title">${result['name']}</h5>
                    <p class="card-text">${result['artists']}</p>
                    <small class="text-body-secondary">${result['release_date']}</small>
                </div>
            </div>
        </a>
    `);
}

function addTrack(result) {
    $('#track-list').append(`
        <a href="${$SCRIPT_ROOT}/player/${result['id']}?item=track" class="list-group-item list-group-item-action d-flex gap-3 py-3" aria-current="true">
            <img src="${result['image']}" alt="twbs" width="32" height="32" class="rounded-circle flex-shrink-0">
            <div class="row w-100">
                <div class="col-md-5">
                    <h6 class="mb-0">${result['name']}</h6>
                    <p class="mb-0 opacity-75">${result['artists']}</p>
                </div>
                <div class="col-md-5">
                    <p class="mb-0">${result['album']}</p>
                </div>
                <div class="col-md-2 text-end">
                    <small class="opacity-50 text-nowrap">${result['duration']}</small>
                </div>
            </div>
        </a>
    `);
}

function processResults(results) {
    $('#spinner').addClass('invisible');
    if (results.data.length === 0) return;
    results.data.forEach(function(result) {
        if (results['type'] == 'album') {
            addAlbum(result);
        } else {
            addTrack(result);
        }
    });
}

function clearResults() {
    $('#album-list').empty();
    $('#track-list').empty();
    $('#spinner').removeClass('invisible');
}