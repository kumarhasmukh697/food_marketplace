
async function fetchCategories(selectId) {
   
    try {

        const response = await fetch(API.categories, {

            method: "GET",

            headers: {
                Authorization: `Bearer ${getAccessToken()}`,
                "Content-Type": "application/json"
            }

        });

        if (!response.ok) {
            throw new Error("Unable to load categories.");
        }

        const categories = await response.json();
        console.log(categories);

        const categorySelect = document.getElementById(selectId);

        categorySelect.innerHTML =
            '<option value="">Select Category</option>';

        categories.forEach(category => {

            const option = document.createElement("option");

            option.value = category.id;

            option.textContent = category.name;

            categorySelect.appendChild(option);

        });

    }
    catch (error) {

        console.error(error);

    }

}
