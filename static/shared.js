(function() {

window.showError = function(msg) {
    var el = document.createElement('div');
    el.className = 'fixed bottom-4 left-1/2 -translate-x-1/2 bg-red-600 text-white px-6 py-3 rounded-xl shadow-lg z-50 text-sm font-medium';
    el.textContent = msg;
    document.body.appendChild(el);
    setTimeout(function() { el.remove(); }, 3000);
};

window.resetCurrentGameCounter = function() {};

window.showSuggestionOverlay = function(currentModule) {
    var genresData = document.getElementById('genres-data');
    if (!genresData) return;
    var allGenres;
    try { allGenres = JSON.parse(genresData.textContent); } catch(e) { return; }
    var lang = document.documentElement.lang || 'en';
    var others = allGenres.filter(function(g) { return g.module !== currentModule; });
    var shuffled = others.sort(function() { return Math.random() - 0.5; }).slice(0, 3);
    var overlay = document.createElement('div');
    overlay.id = 'suggestion-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.6);display:flex;align-items:center;justify-content:center;z-index:9999;';
    overlay.innerHTML = '<div class="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center">' +
        '<h2 class="text-xl font-bold text-gray-800 mb-2">\uD83C\uDF89 ' + (lang === 'fr' ? 'Bien jou\u00e9!' : lang === 'es' ? '\u00a1Bien hecho!' : 'Well played!') + '</h2>' +
        '<p class="text-gray-500 mb-6">' + (lang === 'fr' ? 'Tu as jou\u00e9 quelques parties! Tu veux essayer autre chose?' : lang === 'es' ? '\u00bfHas jugado unas cuantas veces? \u00bfPruebas algo m\u00e1s?' : 'You have played a few rounds! Try something else?') + '</p>' +
        '<div class="space-y-3 mb-6">' +
        shuffled.map(function(g) { return '<a href="/' + lang + '/' + g.slug + '/" class="block w-full bg-purple-50 hover:bg-purple-100 border-2 border-purple-200 rounded-xl p-3 text-purple-700 font-medium transition-all">' + g.name + '</a>'; }).join('') +
        '</div>' +
        '<button onclick="window.resetCurrentGameCounter();this.closest(\'#suggestion-overlay\').remove()" class="text-gray-400 hover:text-gray-600 text-sm underline">' + (lang === 'fr' ? 'Continuer \u00e0 jouer' : lang === 'es' ? 'Seguir jugando' : 'Keep playing') + '</button>' +
        '<br><br>' +
        '<a href="/' + lang + '/" class="text-red-400 hover:text-red-600 text-sm underline">' + (lang === 'fr' ? 'Arr\u00eater' : lang === 'es' ? 'Parar' : 'Stop playing') + '</a>' +
        '</div>';
    document.body.appendChild(overlay);
};

})();
