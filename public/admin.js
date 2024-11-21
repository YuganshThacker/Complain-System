document.addEventListener('DOMContentLoaded', function() {
    fetchComplaints();
});

async function fetchComplaints() {
    try {
        const response = await fetch('/api/complaints');
        const complaints = await response.json();
        displayComplaints(complaints);
    } catch (error) {
        console.error('Error fetching complaints:', error);
    }
}

function displayComplaints(complaints) {
    const complaintsListElement = document.getElementById('adminComplaintsList');
    complaintsListElement.innerHTML = '';

    complaints.forEach(complaint => {
        const complaintElement = document.createElement('div');
        complaintElement.className = 'complaint-item';
        complaintElement.innerHTML = `
            <p><strong>Description:</strong> ${complaint.description}</p>
            <p><strong>Department:</strong> ${complaint.department}</p>
            <img src="/uploads/${complaint.image_filename}" alt="Complaint image">
            <p><strong>Status:</strong> ${complaint.status}</p>
            <p><strong>Submitted:</strong> ${new Date(complaint.created_at).toLocaleString()}</p>
            ${complaint.status === 'Pending' ? `<button onclick="resolveComplaint(${complaint.id})">Mark as Resolved</button>` : ''}
        `;
        complaintsListElement.appendChild(complaintElement);
    });
}

async function resolveComplaint(id) {
    try {
        const response = await fetch(`/api/resolve_complaint/${id}`, {
            method: 'PUT'
        });
        if (response.ok) {
            fetchComplaints();
        } else {
            console.error('Failed to resolve complaint');
        }
    } catch (error) {
        console.error('Error resolving complaint:', error);
    }
}

// admin.js

function markAsResolved(button) {
    // Get the parent element (complaint-item) and mark it as resolved
    const complaintItem = button.parentElement;
    
    // Optional: Add a "resolved" class for visual indication (you can style this class in CSS)
    complaintItem.classList.add('resolved');

    // Change the button text and disable it
    button.textContent = "Resolved";
    button.disabled = true;

    // Change background color or any other styling
    complaintItem.style.backgroundColor = "#d4edda";  // light green for resolved
    complaintItem.style.borderColor = "#c3e6cb";      // green border
}
    