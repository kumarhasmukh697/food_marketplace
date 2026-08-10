 //hii hello world
// Tailwind script already loaded via CDN

function switchRole(roleIndex) {
    // Remove active from all tabs
    document.querySelectorAll('.role-tab').forEach(tab => {
        tab.classList.remove('border-orange-500', 'text-orange-600');
        tab.classList.add('border-transparent');
    });
    
    // Activate selected
    document.getElementById(`tab-${roleIndex}`).classList.add('border-orange-500', 'text-orange-600');
    
    // Hide all main sections
    document.getElementById('main-customer').classList.add('hidden');
    document.getElementById('main-vendor').classList.add('hidden');
    document.getElementById('main-delivery').classList.add('hidden');
    
    // Hide all sidebars
    document.getElementById('sidebar-customer').classList.add('hidden');
    document.getElementById('sidebar-vendor').classList.add('hidden');
    document.getElementById('sidebar-delivery').classList.add('hidden');
    
    if (roleIndex === 0) {
        document.getElementById('main-customer').classList.remove('hidden');
        document.getElementById('sidebar-customer').classList.remove('hidden');
        document.getElementById('current-role').textContent = 'Customer';
        document.getElementById('user-role').textContent = 'Customer';
    } else if (roleIndex === 1) {
        document.getElementById('main-vendor').classList.remove('hidden');
        document.getElementById('sidebar-vendor').classList.remove('hidden');
        document.getElementById('current-role').textContent = 'Vendor';
        document.getElementById('user-role').textContent = 'Restaurant Owner';
    } else if (roleIndex === 2) {
        document.getElementById('main-delivery').classList.remove('hidden');
        document.getElementById('sidebar-delivery').classList.remove('hidden');
        document.getElementById('current-role').textContent = 'Delivery';
        document.getElementById('user-role').textContent = 'Delivery Partner';
    }
}

function switchRoleDemo(roleIndex) {
    toggleRoleModal();
    switchRole(roleIndex);
}

function toggleRoleModal() {
    const modal = document.getElementById('role-modal');
    modal.classList.toggle('hidden');
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('hidden');
}

function navigateTo(section) {
    console.log(`Navigating to: ${section}`);
    // In a real app this would load different content
    alert(`📍 Navigation to ${section} section (demo)`);
}

function toggleCart() {
    alert("🛒 Your cart has 3 items.\n\nTotal: ₹689");
}


function acceptDelivery() {
    alert("🚀 Order accepted! Navigate to pickup location.");
}

// Populate demo data
function populateDemoData() {
    // Restaurants
    const restaurantsHTML = `
        <div class="bg-white rounded-3xl overflow-hidden card-hover cursor-pointer">
            <img src="https://picsum.photos/id/201/400/220" class="w-full h-48 object-cover" alt="">
            <div class="p-5">
                <div class="flex justify-between">
                    <div>
                        <div class="font-semibold">Spice Garden</div>
                        <div class="text-xs text-gray-500">North Indian • 25 min</div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center gap-1 text-emerald-500 text-sm">
                            <i class="fa-solid fa-star"></i> 4.8
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-3xl overflow-hidden card-hover cursor-pointer">
            <img src="https://picsum.photos/id/292/400/220" class="w-full h-48 object-cover" alt="">
            <div class="p-5">
                <div class="flex justify-between">
                    <div>
                        <div class="font-semibold">Bella Napoli</div>
                        <div class="text-xs text-gray-500">Italian • 32 min</div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center gap-1 text-emerald-500 text-sm">
                            <i class="fa-solid fa-star"></i> 4.6
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-3xl overflow-hidden card-hover cursor-pointer">
            <img src="https://picsum.photos/id/431/400/220" class="w-full h-48 object-cover" alt="">
            <div class="p-5">
                <div class="flex justify-between">
                    <div>
                        <div class="font-semibold">Tokyo Ramen</div>
                        <div class="text-xs text-gray-500">Japanese • 18 min</div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center gap-1 text-emerald-500 text-sm">
                            <i class="fa-solid fa-star"></i> 4.9
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="bg-white rounded-3xl overflow-hidden card-hover cursor-pointer">
            <img src="https://picsum.photos/id/669/400/220" class="w-full h-48 object-cover" alt="">
            <div class="p-5">
                <div class="flex justify-between">
                    <div>
                        <div class="font-semibold">Green Bowl</div>
                        <div class="text-xs text-gray-500">Healthy • 22 min</div>
                    </div>
                    <div class="text-right">
                        <div class="flex items-center gap-1 text-emerald-500 text-sm">
                            <i class="fa-solid fa-star"></i> 4.7
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    document.getElementById('restaurant-grid').innerHTML = restaurantsHTML;
    
    // Vendor orders demo
    const vendorOrders = `
        <tr class="border-b hover:bg-gray-50">
            <td class="py-6 px-8 font-medium">#FH-3921</td>
            <td class="py-6 px-8">Priya Sharma</td>
            <td class="py-6 px-8">Butter Chicken ×2, Naan</td>
            <td class="py-6 px-8 font-medium">₹680</td>
            <td class="py-6 px-8"><span class="bg-emerald-100 text-emerald-700 px-4 py-1 rounded-3xl text-xs font-medium">Ready</span></td>
        </tr>
        <tr class="border-b hover:bg-gray-50">
            <td class="py-6 px-8 font-medium">#FH-3920</td>
            <td class="py-6 px-8">Rahul Mehra</td>
            <td class="py-6 px-8">Paneer Tikka Masala</td>
            <td class="py-6 px-8 font-medium">₹420</td>
            <td class="py-6 px-8"><span class="bg-amber-100 text-amber-700 px-4 py-1 rounded-3xl text-xs font-medium">Preparing</span></td>
        </tr>
    `;
    document.getElementById('vendor-orders-table').innerHTML = vendorOrders;
    
    // Delivery jobs
    const deliveryHTML = `
        <div class="bg-white border border-gray-200 rounded-3xl p-6 card-hover">
            <div class="flex justify-between items-start">
                <div>
                    <div class="flex items-center gap-2 text-emerald-600">
                        <i class="fa-solid fa-clock"></i>
                        <span class="font-medium">12 min ago</span>
                    </div>
                    <div class="font-semibold text-lg mt-3">Domino's Pizza</div>
                    <div class="text-gray-500">2.4 km • ₹85 payout</div>
                </div>
                <div class="text-5xl">🍕</div>
            </div>
            <div class="mt-8 flex gap-3">
                <button onclick="acceptDelivery()" class="flex-1 bg-emerald-600 text-white py-4 rounded-3xl font-medium">Accept</button>
                <button class="flex-1 border py-4 rounded-3xl">Skip</button>
            </div>
        </div>
        
        <div class="bg-white border border-gray-200 rounded-3xl p-6 card-hover">
            <div class="flex justify-between items-start">
                <div>
                    <div class="flex items-center gap-2 text-emerald-600">
                        <i class="fa-solid fa-clock"></i>
                        <span class="font-medium">8 min ago</span>
                    </div>
                    <div class="font-semibold text-lg mt-3">KFC - Fried Chicken</div>
                    <div class="text-gray-500">3.1 km • ₹110 payout</div>
                </div>
                <div class="text-5xl">🍗</div>
            </div>
            <div class="mt-8 flex gap-3">
                <button onclick="acceptDelivery()" class="flex-1 bg-emerald-600 text-white py-4 rounded-3xl font-medium">Accept</button>
                <button class="flex-1 border py-4 rounded-3xl">Skip</button>
            </div>
        </div>
    `;
    document.getElementById('delivery-jobs').innerHTML = deliveryHTML;
}

// Initialize
window.onload = function() {
    populateDemoData();
    
    // Make sidebar visible on desktop by default
    document.getElementById('sidebar').classList.remove('hidden');
    
    // Keyboard shortcut hint
    console.log('%c✅ FoodHub Multi-role Template Ready!\n\nUse tabs in navbar to switch between Customer, Vendor & Delivery views.', 'color:#f97316; font-size:13px');
};


function switchRole(roleIndex) { /* ... existing code ... */ 
    // Update profile button text
    const roles = ["Customer", "Vendor", "Delivery Partner"];
    document.getElementById('current-role').textContent = roles[roleIndex];
}

function openProfileModal() {
    const modal = document.getElementById('profile-modal');
    modal.classList.remove('hidden');
    
    // Get current active role
    const activeTab = document.querySelector('.role-tab.border-orange-500');
    const roleIndex = parseInt(activeTab.id.split('-')[1]);
    
    // Show correct profile content
    document.getElementById('profile-customer-content').classList.add('hidden');
    document.getElementById('profile-vendor-content').classList.add('hidden');
    document.getElementById('profile-delivery-content').classList.add('hidden');
    
    if (roleIndex === 0) {
        document.getElementById('profile-customer-content').classList.remove('hidden');
        document.getElementById('profile-subtitle').textContent = "Customer since March 2024";
    } else if (roleIndex === 1) {
        document.getElementById('profile-vendor-content').classList.remove('hidden');
        document.getElementById('profile-subtitle').textContent = "Spice Garden • Verified";
    } else {
        document.getElementById('profile-delivery-content').classList.remove('hidden');
        document.getElementById('profile-subtitle').textContent = "Pro Rider • 4.9 ★";
    }
}

function closeProfileModal() {
    document.getElementById('profile-modal').classList.add('hidden');
}



function toggleCart() {
    alert("🛒 Cart: 3 items • ₹689");
}

// Initialize
// window.onload = function() {
//     // Populate demo content (same as before)
//     console.log("%c✅ FoodHub Template with Profile Settings Loaded!", "color:#f97316;font-size:14px");
// };



