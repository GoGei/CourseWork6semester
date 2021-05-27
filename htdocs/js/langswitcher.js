$('.select-language').select2({
    minimumResultsForSearch: -1
}).on('change', function () {
    $('#select-language').submit()
});