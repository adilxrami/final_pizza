async function submitEditOrder(event, orderId, type) {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  const endpoint = type === 'regular' ? `/edit_order/${orderId}` : `/edit_custom_order/${orderId}`;
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Server responded with error:", errorData);
      alert(`Failed to update ${type}:\n${JSON.stringify(errorData)}`);
      return;
    }

    alert(`${type} updated!`);
    await fetchOrders();
    if (type === 'regular') cancelEdit(orderId);
    else cancelEditCustomOrder(orderId);

  } catch (error) {
    console.error("Fetch error:", error);
    alert('Network error or server problem.');
  }
}

function toggleEditForm(orderId, type) {
  const formRowId = type === 'regular' ? `editForm${orderId}` : `editCustomForm${orderId}`;
  const formRow = document.getElementById(formRowId);
  if (!formRow) return;
  formRow.style.display = formRow.style.display === 'none' ? 'table-row' : 'none';
}

function cancelEdit(orderId) {
  const formRow = document.getElementById(`editForm${orderId}`);
  if (formRow) formRow.style.display = 'none';
}

function cancelEditCustomOrder(orderId) {
  const formRow = document.getElementById(`editCustomForm${orderId}`);
  if (formRow) formRow.style.display = 'none';
}

async function fetchOrders() {
  try {
    const [regularResponse, customResponse] = await Promise.all([
      fetch('/api/orders'),
      fetch('/api/custom_orders'),
    ]);

    if (!regularResponse.ok || !customResponse.ok) {
      throw new Error('Failed to fetch data from server.');
    }

    const orders = await regularResponse.json();
    const customOrders = await customResponse.json();

    const regularBody = document.getElementById('regularOrdersBody');
    const customBody = document.getElementById('customOrdersBody');

    regularBody.innerHTML = orders.map(order => `
      <tr>
        <td>${order.quantity}</td>
        <td>${order.size}</td>
        <td>${order.crust}</td>
        <td>${order.pizza_type}</td>
        <td>$${order.price}</td>
        <td>
          <button type="button" class="edit" data-id="${order.id}" data-type="regular">Edit</button>
          <form action="/delete_order/${order.id}" method="post" style="display:inline;">
            <button class="delete" type="submit" onclick="return confirm('Are you sure?')">Delete</button>
          </form>
        </td>
      </tr>
      <tr id="editForm${order.id}" style="display:none;">
        <td colspan="7">
          <form data-id="${order.id}" data-type="regular" class="editorderform">
            <label>Pizza:</label>
            <select name="pizza_type" required>
              <option value="">-- Select Pizza --</option>
              <option value="margherita" ${order.pizza_type === "margherita" ? "selected" : ""}>Margherita</option>
              <option value="pepperoni" ${order.pizza_type === "pepperoni" ? "selected" : ""}>Pepperoni</option>
              <option value="bbq_chicken" ${order.pizza_type === "bbq_chicken" ? "selected" : ""}>BBQ Chicken</option>
              <option value="veggie" ${order.pizza_type === "veggie" ? "selected" : ""}>Veggie</option>
            </select><br>
        
              <label for="size1">Size:</label>
              <select id="size1" name="size" required>
                <option value="small" ${order.size === 'small' ? 'selected' : ''}>Small</option>
                <option value="medium" ${order.size === 'medium' ? 'selected' : ''}>Medium</option>
                <option value="large" ${order.size === 'large' ? 'selected' : ''}>Large</option>
              </select><br><br>
                <label for="size1">Crust Type:</label>
            <select id="crust1" name="crust" required>
              <option value="thin" ${order.crust === 'thin' ? 'selected' : ''}>Thin</option>
              <option value="thick" ${order.crust === 'thick' ? 'selected' : ''}>Thick</option>
              <option value="stuffed" ${order.crust === 'stuffed' ? 'selected' : ''}>Stuffed</option>
            </select><br><br>
            <label>Quantity:</label>
            <input type="number" name="quantity" value="${order.quantity}" required><br>
            <button type="submit">Save Changes</button>
            <button type="button" class="canceledit" data-id="${order.id}" data-type="regular">Cancel</button>
          </form>
        </td>
      </tr>
    `).join('');

    customBody.innerHTML = customOrders.map(order => `
      <tr id="custom-order-${order.id}">
        <td>${order.quantity}</td>
        <td>${order.size}</td>
        <td>${order.crust}</td>
        <td>${order.cheese}</td>
        <td>${order.toppings}</td>
        <td>$${order.price}</td>
        <td>
          <button type="button" class="edit" data-id="${order.id}" data-type="custom">Edit</button>
          <form action="/delete_custom_order/${order.id}" method="post" style="display:inline;">
            <button type="submit" class="delete" onclick="return confirm('Are you sure?')">Delete</button>
          </form>
        </td>
      </tr>
      <tr id="editCustomForm${order.id}" style="display:none;">
        <td colspan="8">
          <form data-id="${order.id}" data-type="custom" class="editorderform">
            <label for="size1">Size:</label>
            <select id="size1" name="size" required>
              <option value="small" ${order.size === 'small' ? 'selected' : ''}>Small</option>
              <option value="medium" ${order.size === 'medium' ? 'selected' : ''}>Medium</option>
              <option value="large" ${order.size === 'large' ? 'selected' : ''}>Large</option>
            </select><br><br>
            <label>Crust:</label>
            <select id="crust1" name="crust" required>
              <option value="thin" ${order.crust === 'thin' ? 'selected' : ''}>Thin</option>
              <option value="thick" ${order.crust === 'thick' ? 'selected' : ''}>Thick</option>
              <option value="stuffed" ${order.crust === 'stuffed' ? 'selected' : ''}>Stuffed</option>
            </select><br><br>
          <label for="cheese">Cheese:</label>
<select id="cheese" name="cheese" required>
  <option value="0" ${order.cheese === '0' ? 'selected' : ''}>Swiss</option>
  <option value="1" ${order.cheese === '1' ? 'selected' : ''}>Cheddar (+$1)</option>
  <option value="1.5" ${order.cheese === '1.5' ? 'selected' : ''}>Mozzarella (+$1.5)</option>
  <option value="2" ${order.cheese === '2' ? 'selected' : ''}>Vegan (+$2)</option>
</select><br>
            <label>Toppings:</label>
            <input type="text" name="toppings" value="${order.toppings}" required><br>
            <label>Quantity:</label>
            <input type="number" name="quantity" value="${order.quantity}" required><br>
            <button type="submit">Save Changes</button>
            <button type="button" class="canceledit" data-id="${order.id}" data-type="custom">Cancel</button>
          </form>
        </td>
      </tr>
    `).join('');

  } catch (error) {
    alert('Failed to fetch orders.');
    console.error(error);
  }
}

document.addEventListener('click', (event) => {
  const target = event.target;
  if (target.matches('button.edit')) {
    const id = target.dataset.id;
    const type = target.dataset.type;
    toggleEditForm(id, type);
  }
  if (target.matches('button.canceledit')) {
    const id = target.dataset.id;
    const type = target.dataset.type;
    if (type === 'regular') cancelEdit(id);
    else if (type === 'custom') cancelEditCustomOrder(id);
  }
});

document.addEventListener('submit', async (event) => {
  const form = event.target;
  if (form.classList.contains('editorderform')) {
    const id = form.dataset.id;
    const type = form.dataset.type;
    await submitEditOrder(event, id, type);
  }
});

fetchOrders();
