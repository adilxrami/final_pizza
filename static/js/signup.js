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
})();document.getElementById("signupForm").addEventListener("submit", function (e) {
  const username = document.getElementById("username").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;
  const errorBox = document.getElementById("myeror");

  let errorMessage = "";

  if (username.length < 3) {
    errorMessage = "Username must be at least 3 characters long.";
  } else if (!email.includes("@") || !email.includes(".") || email.indexOf("@") > email.lastIndexOf(".")) {
    errorMessage = "Please enter a valid email address.";
  } else {
    const cleanedPhone = phone.replace(/[\s\-()+]/g, ""); 
    if (!cleanedPhone.match(/^\d+$/) || cleanedPhone.length < 10 || cleanedPhone.length > 15) {
      errorMessage = "Please enter a valid phone number.";
    }
  }

  // Password length and uppercase letter check
  if (!errorMessage) {
    if (password.length < 8) {
      errorMessage = "Password must be at least 8 characters long.";
    } else if (!/[A-Z]/.test(password)) {
      errorMessage = "Password must contain at least one uppercase letter.";
    }
  }

  if (!errorMessage && password !== confirmPassword) {
    errorMessage = "Passwords do not match.";
  }

  if (errorMessage) {
    e.preventDefault();
    errorBox.textContent = errorMessage;
    errorBox.classList.add("error-box");
  }
});
