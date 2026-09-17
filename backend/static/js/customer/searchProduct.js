const searchInput = document.getElementById("product-search");

if (searchInput) {
searchInput.addEventListener("input", function () {

    const searchTerm = this.value.trim().toLowerCase();

    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach(card => {

        const productName = (card.dataset.productName || '').toLowerCase();
        const productDescription = (card.dataset.productDescription || '').toLowerCase();

        const matches =
            productName.includes(searchTerm) ||
            productDescription.includes(searchTerm);

        if (matches) {
            card.style.display = "";
        } else {
            card.style.display = "none";
        }

    });

});
}


