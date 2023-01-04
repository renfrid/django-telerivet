//document.ready
$(document).ready(function () {
    //Initialize Select2 Elements
    // $('.select2').select2();

    //Initialize Select2 Elements
    // $('.select2bs4').select2({
    //     theme: 'bootstrap4'
    // });

    //dropdown districts
    $('#region_id').on('change', function (e) {
        region_id = $(this).val();
        baseURL = window.location.origin;

        console.log(region_id)

        $.ajax({
            url: baseURL + '/location/get_districts/' + region_id,
            type: "get",
            success: function (data) {
                $('#district_id').html(data);
            }
        });
    });

    //dropdown wards
    $('#district_id').on('change', function (e) {
        district_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/location/get_wards/' + district_id,
            type: "get",
            success: function (data) {
                $('#ward_id').html(data);
            }
        });
    });

    $('#ward_id').on('change', function (e) {
        ward_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/location/get_villages/' + ward_id,
            type: "get",
            success: function (data) {
                $('#village_id').html(data);
            }
        });
    });

    $('#village_id').on('change', function (e) {
        village_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/location/get_neighborhood/' + village_id,
            type: "get",
            success: function (data) {
                $('#neighborhood_id').html(data);
            }
        });
    });

    $('#keyword_id').on('change', function (e) {
        keyword_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/setup/menu-lists/' + keyword_id,
            type: "get",
            success: function (data) {
                $('#menu_id').html(data);
            }
        });
    });

    $('#menu_id').on('change', function (e) {
        menu_id = $(this).val();
        baseURL = window.location.origin;

        $.ajax({
            url: baseURL + '/setup/sub-menu-lists/' + menu_id,
            type: "get",
            success: function (data) {
                $('#sub_menu_id').html(data);
            }
        });
    });

    /*========================= DELETE ==============================*/
    $('.delete').on('click', function (event) {
        event.preventDefault();
        const url = $(this).attr('href');
        swal({
            title: 'Are you sure?',
            text: 'This record and it`s details will be permanantly deleted!',
            icon: 'error',
            buttons: {
                cancel: 'Cancel',
                confirm: { text: 'Yes', className: 'btn-danger' }
            },
        }).then(function (value) {
            if (value) {
                window.location.href = url;
            }
        });
    });
});