// Form validation and preview functionality
function validateForm() {
    const form = document.getElementById('offerForm');
    return form.checkValidity();
}

function previewDocument() {
    if (!validateForm()) {
        alert('Proszę wypełnić wszystkie wymagane pola przed generowaniem podglądu.');
        return;
    }

    const form = document.getElementById('offerForm');
    const formData = new FormData(form);
    const previewModal = new bootstrap.Modal(document.getElementById('previewModal'));
    
    previewModal.show();

    fetch('/preview', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(html => {
        document.getElementById('previewContent').innerHTML = html;
    })
    .catch(error => {
        document.getElementById('previewContent').innerHTML = 
            '<div class="alert alert-danger">Wystąpił błąd podczas generowania podglądu.</div>';
        console.error('Preview error:', error);
    });
}

// Price input formatting
document.getElementById('price').addEventListener('input', function(e) {
    let value = e.target.value;
    if (value !== '') {
        value = parseFloat(value).toFixed(2);
        if (!isNaN(value)) {
            e.target.value = value;
        }
    }
});

// Set default date to today
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
});
