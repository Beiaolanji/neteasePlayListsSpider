const URL = 'http://127.0.0.1:8000/';
let getPlaylists = function () {
    $.ajax({
        method: 'GET',
        url: URL + 'playlists/',
        success: function (data) {
            table1.PlayLists = data
        }
    });
};
let table1 = new Vue({
    el: '#table1',
    data: {
        PlayLists: []
    },
});

let divCreate = new Vue({
    el: '#div-create',
    data: {
        name: '',
        url_id: '',
        time: '',
        comment: null,
        singer: '',
        album: '',
    },
    methods: {
        create: function () {
            $.ajax({
                method: 'POST',
                url: URL + 'playlists/',
                data: {
                    name: this.name,
                    url_id: this.url_id,
                    time: this.time,
                    comment: this.comment,
                    singer_name: this.singer,
                    album_name: this.album,
                },
                success: function (data) {
                    getPlaylists();
                    divCreate.name = null;
                    divCreate.url_id = null;
                    divCreate.time = null;
                    divCreate.comment = null;
                    divCreate.singer = null;
                    divCreate.album = null;
                }
            });
        }
    }
});

let divUpdate = new Vue({
    el: '#div-update',
    data: {
        selected: null,
        hidden: true,
    },
    methods: {
        getPlayLists: function () {
            return table1.PlayLists;
        },
        change: function () {
            this.hidden = false;
        },
        update: function () {
            $.ajax({
                method: 'PUT',
                url: URL + 'playlists/',
                data: {
                    id: this.selected.id,
                    name: this.selected.name,
                    url_id: this.selected.url_id,
                    time: this.selected.time,
                    comment: this.selected.comment,
                    singer_name: this.selected.singer,
                    album_name: this.selected.album,
                },
                success: function (data) {
                    getPlaylists();
                    divUpdate.hidden = true;
                }
            });
        },
        destroy: function () {
            $.ajax({
                method: 'DELETE',
                url: URL + 'playlists/',
                data: {
                    id: this.selected.id,
                },
                success: function () {
                    getPlaylists();
                    divUpdate.hidden = true;
                }
            })
        },
    }
});


let divSearch = new Vue({
    el: '#div-search',
    data: {
        key_word: '',
        progressing: false,
    },
    methods: {
        search: function () {
            this.progressing = true;
            $.get(URL + 'getlist/?key_word=' + this.key_word).done(function () {
                getPlaylists();
                divSearch.progressing = false;
            })
        }
    }
});

getPlaylists();