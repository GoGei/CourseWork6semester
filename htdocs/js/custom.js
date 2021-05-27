SPINNER_CONTENT = '' +
    '<div class="loader-demo">' +
        '<div class="ball-grid-pulse">' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
            '<div></div>' +
        '</div>' +
    '</div>';

$.fn.loaderOverlay = function(action) {
    if (action === 'show') {
        this.each(function () {
            var container = $(this);
            if (!container.hasClass('loader-overlay-wrapper')) {
                container.addClass('loader-overlay-wrapper');
                container.append('<div class="loader-overlay-spinner">' + SPINNER_CONTENT + '</div>');
                setTimeout(function () {
                    container.find('.loader-overlay-spinner').addClass('visible');
                }, 200);
            }
        });
    }
    if (action === 'hide') {
        this.removeClass('loader-overlay-wrapper');
        this.find('.loader-overlay-spinner').remove();
    }
    return this;
};


$(document).ready(function () {

    // ajax select2 in modal fix
    $.fn.modal.Constructor.prototype.enforceFocus = function() {};

    $.extend($.fn.select2.defaults.defaults.language, {
        noResults: function() { return 'No results found'; },
        searching: function() { return 'Searching...'; },
        errorLoading: function() { return 'The results could not be loaded.'; }
    });

    $('.select2').not('.no-search').select2({
        allowClear: true,
        placeholder: "Select from the list"
    });

    var $select2nosearch = $('select.select2.no-search');

    $select2nosearch.select2({
        minimumResultsForSearch: -1,
        allowClear: true,
        placeholder: "Select an option"
    });

    $('.language-select').select2({
        minimumResultsForSearch: -1,
    }).on('change', function () {
        $('#select-language').submit()
    });

    $select2nosearch.on("select2:unselecting", function (e) {
             $(this).val(null).trigger("change");
             e.preventDefault();
    });

    $('.nav-tabs').not('.no-history').find('li').find('a').click(function () {
        console.log('Click');
        var _url = this.getAttribute('href').replace('#', '');
        window.history.pushState({}, "", '?tab=' + _url);
    });

    $(":input").inputmask();
    $('.timepicker').datetimepicker({
        format: "HH:mm",
        stepping: 5
    });

    // $('.datepicker').datetimepicker();
    $('.datetimepicker').datetimepicker({
        locale: _locale.defaultLocale,
        sideBySide: true,
        stepping: 10,
        useCurrent: 'day',
    });


    $('.multiple-datepicker').each(function () {
        var $dateField = $(this);
        var dateFormat = $dateField.data('date-format');
        $dateField.datepicker({
            multidate: true,
            format: dateFormat,
            language: $.cookie('_language') || 'uk'
        })
    });


    $(document).on('click', '.show-actions', function(event) {
        $('.show-actions').not(this).removeClass('is-active').next('.block-action-holder').removeClass('is-open');
        $(this).toggleClass('is-active');
        $(this).next('.block-action-holder').toggleClass('is-open');

        event.preventDefault();
        event.stopPropagation();
        $(document).on('click.block-action', function() {
            $('.show-actions').removeClass('is-active').next('.block-action-holder').removeClass('is-open');
            $(document).off('click.block-action');
        });
    });

});

// $(function() {
//     $('#result_list').DataTable({
//         "scrollY": "62vh",
//         "scrollX": true,
//         "scrollCollapse": true,
//         "bLengthChange": false,
//         "bFilter": false,
//         "bPaginate": false,
//         "bInfo": false,
//         "bProcessing": false
//     });
// });