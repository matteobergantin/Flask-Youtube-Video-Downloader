// Scroll down if you want to burn your eyes





































// This is an horrible function I wrote like 3 months ago to show a simple alert using bootstrap + jQuery
// No HTML needed, just call the function and it'll show the msg with the given style
function bs_alert(msg, style = 'danger', animation_duration = 1500, expiry_duration = 5000) {
    if ($('.bs-alert-func-wrapper').length == 0)
        $('body').append('<div class="bs-alert-func-wrapper" style="position: fixed; top: 0; left: 0; z-index: 99999999; width: 100%; height: max-content;"></div>');
    let id = Math.floor(Math.random() * 100000);
    if (!animation_duration instanceof Number)
        animation_duration = parseInt(animation_duration)
    if (!expiry_duration instanceof Number)
        expiry_duration = parseInt(expiry_duration)
    $('.bs-alert-func-wrapper').append(`<div class="bs-alert-func-${id} bs-alert-func alert" role="alert" style="position: relative; top: 0px; left: 0px; width: 100%; z-index: 999999; opacity: 0; transition-duration: ${animation_duration}ms; margin-bottom: 10px;"></div>`);
    $(`.bs-alert-func-${id}`).addClass('alert-'+style.toLowerCase())
    $(`.bs-alert-func-${id}`).text(msg)
    
    const destroyAlert = function() {
        $('.bs-alert-func-' + id).css('opacity', '0');
        window.setTimeout(function() {
            $('.bs-alert-func-' + id).remove();
            if ($('.bs-alert-func').length == 0)
                $('.bs-alert-func-wrapper').remove();
        }, animation_duration + 1);
    }
    $('.bs-alert-func-' + id).click(destroyAlert);
    window.setTimeout(function() {
        $('.bs-alert-func-' + id).css('opacity', '1');
    }, 0);
    window.setTimeout(destroyAlert, expiry_duration + animation_duration);
}