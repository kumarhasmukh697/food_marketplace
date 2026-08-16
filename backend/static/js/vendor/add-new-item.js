async function addNewItem() {
    document.getElementById('add-item-modal').classList.remove('hidden'); 
   

    // Call the function
    await fetchCategories("dish-category");

}