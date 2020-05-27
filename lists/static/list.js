window.Superlists = {};
window.Superlists.initialize = function () {
    $('input[name="text"]').on('keypress', function() {
        console.log('in keypress handler');
        $('.has-error').hide();
    });
};