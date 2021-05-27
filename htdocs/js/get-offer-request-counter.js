const updateOfferRequestItemCount = async () => {
    console.log('load updateRegistrationRequestItemCount');
    const url = '/offer-requests/counter/';
    const data = await $.get(url);
    const hasSummaryIcon = $('.offer-requests-counter').children('.summary').length;
    const count = data.counter || 0;
    console.log('count', count);
    if (count!== 0) {
        if (hasSummaryIcon) {
            $('.summary span').text(count);
        } else {
            $('.offer-requests-counter').append(`
            <div class="summary">
                <span>${count}</span>
            </div>
        `)
        }
    }
};

$(window).on('load', updateOfferRequestItemCount);
