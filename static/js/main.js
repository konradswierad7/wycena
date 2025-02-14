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

// Price calculations
function calculateVAT() {
    const nettoInput = document.getElementById('price_netto');
    const bruttoInput = document.getElementById('price_brutto');

    if (nettoInput.value) {
        const netto = parseFloat(nettoInput.value);
        const brutto = Math.round(netto * 1.08 * 100) / 100; // VAT 8% with rounding to 2 decimal places
        bruttoInput.value = brutto;
        bruttoInput.setAttribute('readonly', true);
    } else {
        bruttoInput.removeAttribute('readonly');
    }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    const nettoInput = document.getElementById('price_netto');
    const bruttoInput = document.getElementById('price_brutto');

    nettoInput.addEventListener('input', calculateVAT);

    bruttoInput.addEventListener('input', function() {
        if (this.value) {
            nettoInput.setAttribute('readonly', true);
        } else {
            nettoInput.removeAttribute('readonly');
        }
    });

    // Validate postal code format
    const postalCodeInput = document.getElementById('postal_code');
    postalCodeInput.addEventListener('input', function(e) {
        let value = e.target.value.replace(/\D/g, '');
        if (value.length > 2) {
            value = value.slice(0, 2) + '-' + value.slice(2);
        }
        e.target.value = value;
    });

    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('date').value = today;
});

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