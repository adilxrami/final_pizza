document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('.login form');
    if (!form) return;
  
    const inputs = form.querySelectorAll('input');
  
    function showError(input, message) {
      clearError(input);
      const error = document.createElement('div');
      error.className = 'error-msg';
      error.style.color = '#e2491e';
      error.style.fontSize = '0.8em';
      error.style.marginTop = '4px';
      error.textContent = message;
      input.setAttribute('aria-invalid', 'true');
      input.parentElement.appendChild(error);
    }
  
    function clearError(input) {
      const existing = input.parentElement.querySelector('.error-msg');
      if (existing) existing.remove();
      input.setAttribute('aria-invalid', 'false');
    }
  
    function validateForm() {
      let isValid = true;
  
      inputs.forEach(input => {
        clearError(input);
        if (!input.value.trim()) {
          showError(input, `${input.placeholder || input.name || 'Field'} is required`);
          isValid = false;
        } else if (input.type === 'password' && input.value.length < 6) {
          showError(input, 'Password must be at least 6 characters');
          isValid = false;
        }
      });
  
      return isValid;
    }
  
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      if (validateForm()) {
        alert('Login successful!');
        form.reset();
        inputs.forEach(clearError);
      }
    });
  });