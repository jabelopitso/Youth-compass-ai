// Simple JavaScript for enhanced UX
document.addEventListener('DOMContentLoaded', function() {
    // Auto-focus on text inputs
    const textInput = document.querySelector('input[type="text"]');
    const textArea = document.querySelector('textarea');
    
    if (textInput) {
        textInput.focus();
    }
    
    if (textArea) {
        textArea.focus();
    }
    
    // Character counter for textarea
    if (textArea) {
        const counter = document.createElement('div');
        counter.className = 'char-counter';
        counter.style.textAlign = 'right';
        counter.style.fontSize = '12px';
        counter.style.color = '#666';
        textArea.parentNode.insertBefore(counter, textArea.nextSibling);
        
        function updateCounter() {
            const length = textArea.value.length;
            counter.textContent = `${length} characters`;
        }
        
        textArea.addEventListener('input', updateCounter);
        updateCounter();
    }
});

// Form validation
function validateForm(form) {
    const required = form.querySelectorAll('[required]');
    for (let field of required) {
        if (!field.value.trim()) {
            field.focus();
            return false;
        }
    }
    return true;
}