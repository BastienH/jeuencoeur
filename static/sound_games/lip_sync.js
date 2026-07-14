(function() {
    const soundContainer = document.getElementById('sound-container');
    let promptCount = 0;

    document.addEventListener('htmx:afterSwap', (e) => {
        if (e.detail.target === soundContainer) {
            promptCount++;
            checkPlayLimit('lip_sync_legends');
        }
    });

    function checkPlayLimit(currentModule) {
        if (promptCount >= 7) {
            promptCount = 0;
            showSuggestionOverlay(currentModule);
        }
    }

    window.resetCurrentGameCounter = function() { promptCount = 0; };
})();
