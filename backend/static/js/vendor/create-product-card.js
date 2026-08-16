function createProductCard(product) {
    
    const imageUrl = product.image
        ? product.image
        : "https://via.placeholder.com/600x400?text=No+Image";

    const availabilityBadge = product.is_available
        ? `
        <span class="px-4 py-1 bg-green-100 text-green-700 text-xs font-medium rounded-full">
            Available
        </span>
        `
        : `
        <span class="px-4 py-1 bg-red-100 text-red-700 text-xs font-medium rounded-full">
            Unavailable
        </span>
        `;

    const stockStatus = product.stock > 0
        ? `
        <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 bg-emerald-500 rounded-full"></div>
            <span class="text-emerald-600 text-xs font-medium">
                In Stock
            </span>
        </div>
        `
        : `
        <div class="flex items-center gap-1.5">
            <div class="w-2 h-2 bg-red-500 rounded-full"></div>
            <span class="text-red-600 text-xs font-medium">
                Out of Stock
            </span>
        </div>
        `;

    return `
        <div  id="product-${product.id}" class="bg-white rounded-3xl overflow-hidden shadow-sm card-hover">
            <img src="${imageUrl}" class="w-full h-52 object-cover" alt="${product.name}">
            <div class="p-6">
                <div class="flex justify-between items-start">
                    <div>
                        <h3 class="font-semibold text-xl"> ${product.name}</h3>
                        <p class="text-emerald-600 font-medium mt-1">₹${product.price}</p>
                    </div>
                    ${availabilityBadge}
                </div>
                <p class="text-gray-500 text-sm mt-3 line-clamp-2"> ${product.description || ""}</p>
                <div class="mt-4 flex items-center justify-between text-sm">
                    <div class="flex items-center gap-2">
                        <span class="text-gray-500">Stock:</span>
                        <span class="font-medium text-emerald-600"> ${product.stock} units</span>
                    </div>
                    ${stockStatus}
                </div>
                <div class="flex gap-3 mt-6">
                    <button onclick="editMenuItem(${product.id})" class="flex-1 border border-gray-300 hover:bg-gray-50 py-3 rounded-2xl text-sm font-medium flex items-center justify-center gap-2">
                        <i class="fa-solid fa-pen"></i>
                        Edit
                    </button>

                    <button onclick="deleteMenuItem(${product.id})" class="flex-1 border border-red-200 hover:bg-red-50 text-red-600 py-3 rounded-2xl text-sm font-medium flex items-center justify-center gap-2">
                        <i class="fa-solid fa-trash"></i>
                        Delete
                    </button>
                </div>
            </div>
        </div>
    `;
}
