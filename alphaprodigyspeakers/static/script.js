document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('input[name="q"]');
    const suggestionsBox = document.querySelector('.suggestions');
    if (searchInput && suggestionsBox) {
        searchInput.addEventListener("input", function() {
            const query = this.value;
            if (query.length > 2) {
                fetch(`/search_suggestions/?q=${query}`)
                    .then(response => response.json())
                    .then(data => {
                        suggestionsBox.innerHTML = '';
                        data.results.forEach(item => {
                            const suggestion = document.createElement('div');
                            suggestion.textContent = item;
                            suggestionsBox.appendChild(suggestion);
                        });
                    });
            }
        });
    }
});
