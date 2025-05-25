
 const pizzaBg = document.createElement("div");
  pizzaBg.className = "pizza-bg";
  document.body.appendChild(pizzaBg);

  const count = 100;
  for (let i = 0; i < count; i++) {
    const pizza = document.createElement("div");
    pizza.className = "pizza-piece";
    pizza.textContent = "🍕";
    pizza.style.left = Math.random() * 100 + "vw";
    pizza.style.top = Math.random() * 100 + "vh";
    pizza.style.fontSize = 16 + Math.random() * 24 + "px";
    pizza.style.setProperty("--r", Math.random());
    pizzaBg.appendChild(pizza);
  }

document.addEventListener("DOMContentLoaded", function () {
  
  // Fill the form inputs with user info fetched from backend
  fetch("/api/user_info")
      .then(response => response.json())
      .then(data => {
          if (data.error) {
              console.error("Error loading user info:", data.error);
              return;
          }
          document.querySelector('input[name="username"]').value = data.username || "";
          document.querySelector('input[name="email"]').value = data.email || "";
          document.querySelector('input[name="phone"]').value = data.phone || "";
      })
      .catch(error => console.error("Fetch error:", error));

  // Show error messages passed in URL query params (e.g. ?error=...)
  const urlParams = new URLSearchParams(window.location.search);
  const errorMsg = urlParams.get("error");
  const successMsg = urlParams.get("success");
  const myeror = document.getElementById("myeror");

  if (errorMsg) {
    myeror.textContent = errorMsg;
    myeror.classList.add("error-box");
  } else if (successMsg) {
    myeror.textContent = successMsg;
    myeror.style.color = "green";
    myeror.classList.remove("error-box");
  } else {
    myeror.textContent = "";
    myeror.classList.remove("error-box");
  }

  // Password confirmation client-side check: show error inside page, no alert
  document.getElementById('editProfileForm').addEventListener('submit', function(e) {
    const password = this.password.value;
    const confirm = this.confirm_password.value;
    if (password !== confirm) {
      e.preventDefault();
      myeror.textContent = "New password and confirmation do not match.";
      myeror.classList.add("error-box");
      myeror.style.color = "";  // reset color in case it was green
    }
  });
});

