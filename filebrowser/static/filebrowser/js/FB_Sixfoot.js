if(window.opener){
    document.addEventListener('DOMContentLoaded', function(e) {
        // hook an event on the select button
        var selectButtons, button, i, img, message;

        function onImageButtonClick(e) {
            message = {
                event: 'selected',
                file: e.target.getAttribute('data-file'),
                type: e.target.getAttribute('data-type')
            }
            window.opener.postMessage(message, '*');
            window.close();
        }

        selectButtons = document.querySelectorAll('button[name="sixfoot-select"]');
        console.log(selectButtons);
        for (i = selectButtons.length - 1; i >= 0; i--) {
            button = selectButtons[i];

            button.addEventListener('click', onImageButtonClick);
        };

        window.addEventListener('unload', function(e) {
            message = {
                event: 'close',
                file: null,
                type: null
            }
            window.opener.postMessage(message, '*');
        });
    });
}