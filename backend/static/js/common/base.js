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

// Initialize
// window.onload = function() {
  
    
    // Make sidebar visible on desktop by default
    // document.getElementById('sidebar').classList.remove('hidden');
    
   
// };


function switchRole(roleIndex) { /* ... existing code ... */ 
    // Update profile button text
    const roles = ["Customer", "Vendor", "Delivery Partner"];
    document.getElementById('current-role').textContent = roles[roleIndex];
}




function toggleCart() {
    alert("🛒 Cart: 3 items • ₹689");
}


