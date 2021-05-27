$('.select-language').select2({
    minimumResultsForSearch: -1
}).on('change', function () {
    console.log('lang');
    $('#select-language').submit()
});

$('.language-select').select2({
    minimumResultsForSearch: -1,
}).on('change', function () {
    $('#select-language').submit()
});