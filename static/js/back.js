
 const pizzaBg = document.createElement("div");
  pizzaBg.className = "pizza-bg";
  document.body.appendChild(pizzaBg);

  const count = 100; // number of pizza slices
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
  