
function toggleRoleModal() {
    const modal = document.getElementById('role-modal');
    modal.classList.toggle('hidden');
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('hidden');
}



function acceptDelivery() {
    alert("🚀 Order accepted! Navigate to pickup location.");
}


function openProfileModal() {
    const modal = document.getElementById("profile-modal");
    modal.classList.remove("hidden");
    
    // Get user role from data attribute
    const userRole = modal.getAttribute("data-user-role");
    // console.log(`User role: ${userRole}`);
    
    // Fetch profile data based on user role
    if (userRole === "vendor") {
        getvendorProfile();
    } else if (userRole === "customer") {
        getCustomerProfile();
    } else if (userRole === "delivery") {
        getDeliveryProfile();
    }
}



function closeProfileModal() {
    document.getElementById('profile-modal').classList.add('hidden');
}


