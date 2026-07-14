(function () {
  var CACHE_KEY = 'prompts_cache';
  var lang = document.documentElement.lang || 'en';

  function getCache() {
    try {
      return JSON.parse(localStorage.getItem(CACHE_KEY));
    } catch (e) {
      return null;
    }
  }

  function setCache(version, prompts) {
    try {
      localStorage.setItem(CACHE_KEY, JSON.stringify({version: version, prompts: prompts}));
    } catch (e) {
    }
  }

  function fetchPrompts() {
    var current = getCache();
    var url = '/' + lang + '/api/prompts/';

    fetch(url)
      .then(function (res) { return res.json(); })
      .then(function (data) {
        if (!current || current.version !== data.version) {
          setCache(data.version, data.prompts);
        }
      })
      .catch(function () {
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fetchPrompts);
  } else {
    fetchPrompts();
  }
})();
