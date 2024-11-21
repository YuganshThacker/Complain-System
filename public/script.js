document.addEventListener('DOMContentLoaded', function() {
    const complaintForm = document.getElementById('complaintForm');
    
    complaintForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/api/submit_complaint', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                alert(result.message);
                complaintForm.reset();
                fetchComplaints();
                fetchStats();
            } else {
                const error = await response.json();
                console.error('Server error:', error);
                alert(error.error || 'Failed to submit complaint');
            }
        } catch (error) {
            console.error('Network error:', error);
            alert('An error occurred while submitting the complaint');
        }
    });

    fetchComplaints();
    fetchStats();
});

// ... rest of the code remains the same

document.addEventListener('DOMContentLoaded', function() {
    const complaintForm = document.getElementById('complaintForm');
    
    complaintForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        
        try {
            const response = await fetch('/api/submit_complaint', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                const result = await response.json();
                alert(result.message);
                complaintForm.reset();
                fetchComplaints();
                fetchStats();
            } else {
                const error = await response.json();
                alert(error.error || 'Failed to submit complaint');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while submitting the complaint');
        }
    });

    fetchComplaints();
    fetchStats();
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
    const complaintsListElement = document.getElementById('complaintsList');
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
        `;
        complaintsListElement.appendChild(complaintElement);
    });
}

async function fetchStats() {
    try {
        const response = await fetch('/api/stats');
        const stats = await response.json();
        displayStats(stats);
    } catch (error) {
        console.error('Error fetching stats:', error);
    }
}

function displayStats(stats) {
    document.getElementById('pendingCount').textContent = stats.pending;
    document.getElementById('resolvedCount').textContent = stats.resolved;
    document.getElementById('totalCount').textContent = stats.total;
}

