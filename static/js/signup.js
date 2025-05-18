
    (async function fetchErrorMessage() {
      try {
        const res = await fetch('/geteror');
        const data = await res.json();
        if (data.error) {
          const myeror = document.getElementById("myeror");
          myeror.textContent = data.error;
          myeror.classList.add("error-box");
        }
      } catch (err) {
        console.error("Failed to load error message:", err);
      }
    })();

    document.getElementById("signupForm").addEventListener("submit", function (e) {
      const username = document.getElementById("username").value.trim();
      const email = document.getElementById("email").value.trim();
      const phone = document.getElementById("phone").value.trim();
      const password = document.getElementById("password").value;
      const confirmPassword = document.getElementById("confirm_password").value;
      const errorBox = document.getElementById("myeror");

      let errorMessage = "";

      if (username.length < 3) {
        errorMessage = "Username must be at least 3 characters long.";
      }

      else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        errorMessage = "Please enter a valid email address.";
      }
  
      else if (!/^\+?[0-9\s\-()]{10,}$/.test(phone)) {
        errorMessage = "Please enter a valid phone number.";
      }
    
      else if (password.length < 6) {
        errorMessage = "Password must be at least 6 characters long.";
      }
     
      else if (password !== confirmPassword) {
        errorMessage = "Passwords do not match.";
      }

      if (errorMessage) {
        e.preventDefault(); 
        errorBox.textContent = errorMessage;
        errorBox.classList.add("error-box");
      }
    });