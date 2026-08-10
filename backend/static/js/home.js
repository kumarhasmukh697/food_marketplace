
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
    
function openProfileModal() {
    document.getElementById("profile-modal").classList.remove("hidden");
}

function closeProfileModal() {
    document.getElementById('profile-modal').classList.add('hidden');
}


