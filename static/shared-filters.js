(function() {
    var COOKIE_NAME = 'game_filters';
    var COOKIE_EXPIRY_DAYS = 365;

    function readFilters() {
        var match = document.cookie.match(new RegExp('(?:^|; )' + COOKIE_NAME + '=([^;]*)'));
        if (match) {
            try { return JSON.parse(decodeURIComponent(match[1])); } catch(e) {}
        }
        return {};
    }

    function writeFilters(filters) {
        var cleaned = {};
        if (filters.category) cleaned.category = filters.category;
        if (filters.age && filters.age !== 'all') cleaned.age = filters.age;
        if (filters.energy_level) cleaned.energy_level = filters.energy_level;
        var value = JSON.stringify(cleaned);
        var d = new Date();
        d.setTime(d.getTime() + COOKIE_EXPIRY_DAYS * 24 * 60 * 60 * 1000);
        document.cookie = COOKIE_NAME + '=' + encodeURIComponent(value) +
            ';expires=' + d.toUTCString() + ';path=/;SameSite=Lax';
    }

    function buildFilterURL(base, filters) {
        var params = new URLSearchParams();
        if (filters.category) params.set('category', filters.category);
        if (filters.age) params.set('age_group', filters.age);
        if (filters.energy_level) params.set('energy_level', filters.energy_level);
        var qs = params.toString();
        return qs ? base + '?' + qs : base;
    }

    function readDOMFilters() {
        var cat = document.getElementById('filter-category');
        var age = document.getElementById('filter-age');
        var energy = document.getElementById('filter-energy');
        return {
            category: cat ? cat.value : '',
            age: age ? age.value : '',
            energy_level: energy ? energy.value : ''
        };
    }

    function highlightActiveFilters() {
        var ids = ['filter-category', 'filter-age', 'filter-energy'];
        ids.forEach(function(id) {
            var el = document.getElementById(id);
            if (!el) return;
            var isDefault = el.selectedIndex === 0;
            if (isDefault) {
                el.classList.remove('ring-2', 'ring-primary', 'bg-primary-light');
            } else {
                el.classList.add('ring-2', 'ring-primary', 'bg-primary-light');
            }
        });
    }

    function restoreFromCookie() {
        var filters = readFilters();
        var cat = document.getElementById('filter-category');
        var age = document.getElementById('filter-age');
        var energy = document.getElementById('filter-energy');

        if (!filters.age || filters.age === 'all') {
            var container = document.getElementById('game-filters');
            var defaultAge = container?.dataset.defaultAge;
            if (defaultAge && defaultAge !== 'all') {
                filters.age = defaultAge;
                writeFilters(filters);
            }
        }

        if (cat && filters.category) {
            for (var i = 0; i < cat.options.length; i++) {
                if (cat.options[i].value === filters.category) { cat.selectedIndex = i; break; }
            }
        }
        if (age && filters.age) {
            for (var i = 0; i < age.options.length; i++) {
                if (age.options[i].value === filters.age) { age.selectedIndex = i; break; }
            }
        }
        if (energy && filters.energy_level) {
            for (var i = 0; i < energy.options.length; i++) {
                if (energy.options[i].value === filters.energy_level) { energy.selectedIndex = i; break; }
            }
        }
        highlightActiveFilters();
    }

    function onFilterChange() {
        var filters = readDOMFilters();
        writeFilters(filters);
        highlightActiveFilters();
        var rerollUrl = document.getElementById('game-filters')?.dataset.rerollUrl;
        if (rerollUrl) {
            var url = buildFilterURL(rerollUrl, filters);
            htmx.ajax('GET', url, { target: '#game-content', swap: 'innerHTML' });
        }
    }

    window.gameFilters = {
        read: readFilters,
        write: writeFilters,
        buildURL: buildFilterURL,
        readDOM: readDOMFilters,
        highlight: highlightActiveFilters,
        restore: restoreFromCookie,
        onChange: onFilterChange
    };

    document.addEventListener('DOMContentLoaded', restoreFromCookie);
})();
