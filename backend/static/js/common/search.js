const searchInput = document.getElementById('search-input');
const productSearchInput = document.getElementById('product-search');

function filterItems(input, selector) {
    if (!input) {
        return;
    }

    input.addEventListener('input', function () {
        const searchTerm = this.value.trim().toLowerCase();
        const searchItems = document.querySelectorAll(selector);

        searchItems.forEach(item => {
            const searchableText = item.textContent.trim().toLowerCase();
            item.style.display = searchableText.includes(searchTerm) ? '' : 'none';
        });
    });
}

function focusSearchInput() {
    if (!searchInput) {
        return;
    }

    searchInput.closest('.hidden.md\\:flex')?.classList.remove('hidden');
    searchInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
    searchInput.focus();
}

filterItems(searchInput, '[data-search-item]');
filterItems(productSearchInput, '.product-card');



