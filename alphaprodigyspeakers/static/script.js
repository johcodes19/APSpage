document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.querySelector('input[name="q"]');
    const suggestionsBox = document.querySelector('.suggestions');
    
    const toggleButton = document.getElementById("dark-mode-toggle");
    const body = document.body;
    
    if (toggleButton) {
        toggleButton.addEventListener("click", function() {
            body.classList.toggle("dark-mode");
        
            // Toggle class for header and footer
            document.querySelector("header").classList.toggle("dark-mode");
            document.querySelector("footer").classList.toggle("dark-mode");
            document.querySelector("nav").classList.toggle("dark-mode");
        });
    }
    
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
