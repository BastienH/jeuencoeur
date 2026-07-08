(function() {
    const actionBtn = document.getElementById('action-btn');
    const countdownDisplay = document.getElementById('countdown-display');
    const reverseToggle = document.getElementById('reverse-toggle');
    const reverseOptions = document.getElementById('reverse-options');
    const soundContainer = document.getElementById('sound-container');
    let promptCount = 0;

    if (actionBtn) {
        actionBtn.addEventListener('click', () => {
            if (!countdownDisplay) return;
            actionBtn.disabled = true;
            countdownDisplay.classList.remove('hidden');
            let count = 3;
            countdownDisplay.textContent = count;
            const interval = setInterval(() => {
                count--;
                if (count > 0) {
                    countdownDisplay.textContent = count;
                } else if (count === 0) {
                    countdownDisplay.textContent = 'GO!';
                } else {
                    clearInterval(interval);
                    countdownDisplay.classList.add('hidden');
                    actionBtn.disabled = false;
                }
            }, 1000);
        });
    }

    if (reverseToggle) {
        reverseToggle.addEventListener('click', () => {
            const isReverse = !reverseToggle.classList.contains('bg-purple-600');
            reverseToggle.classList.toggle('bg-purple-600');
            reverseToggle.classList.toggle('text-white');
            reverseToggle.classList.toggle('bg-gray-200');
            reverseToggle.classList.toggle('text-gray-700');
            reverseToggle.textContent = isReverse ? 'Reverse Mode: ON' : 'Reverse Mode: OFF';
            if (reverseOptions) reverseOptions.classList.toggle('hidden');

            if (isReverse && soundContainer) {
                const nameEl = soundContainer.querySelector('.text-2xl');
                const name = nameEl?.textContent?.trim() || '';
                const words = name.split(/\s+/).filter(Boolean);
                const options = reverseOptions?.querySelectorAll('.reverse-option');
                if (options && words.length >= 4) {
                    options.forEach((opt, i) => {
                        opt.textContent = words[i] || '???';
                    });
                }
            }
        });
    }

    document.querySelectorAll('.reverse-option').forEach(opt => {
        opt.addEventListener('click', () => {
            opt.classList.add('ring-4', 'ring-green-400');
        });
    });

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
