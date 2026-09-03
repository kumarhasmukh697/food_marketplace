const searchInput = document.getElementById("product-search");

searchInput.addEventListener("input", function () {

    const searchTerm = this.value.trim().toLowerCase();

    const productCards = document.querySelectorAll(".product-card");

    productCards.forEach(card => {

        const productName = card.dataset.productName;
        const productDescription = card.dataset.productDescription;

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