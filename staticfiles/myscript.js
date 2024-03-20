// Function to handle size selection
function handlesize(size) {
  // Get elements related to the selected size
  var checkbox = document.getElementById(size);
  var selected_size = document.getElementById('selected_size');
  var final_size_input = document.querySelector('input[name="final_size"]');
  var label = document.querySelector('label[for="' + size + '"]');

  // Array of available sizes
  var sizes = ['S', 'M', 'L', 'XL'];

  // Uncheck other sizes and reset their styles
  sizes.forEach(function (item) {
    if (item !== size) {
      document.getElementById(item).checked = false;
      var otherLabel = document.querySelector('label[for="' + item + '"]');
      otherLabel.style.backgroundColor = '';
      otherLabel.style.color = '';
    }
  });

  // Handle styling when the size is selected or unselected
  if (checkbox.checked) {
    label.style.backgroundColor = 'black';
    label.style.color = 'white';
    selected_size.innerText = size.toUpperCase();
    final_size_input.value = size.toUpperCase();
    console.log(selected_size.innerText);
  } else {
    label.style.backgroundColor = '';
    label.style.color = '';
  }
}

// Function to handle color selection
function handleColor(color) {
  // Get elements related to the selected color
  var checkbox = document.getElementById(color);
  var selected_color = document.getElementById('selected_color');
  var final_color_input = document.querySelector('input[name="final_color"]');
  var label = document.querySelector('label[for="' + color + '"]');

  // Array of available colors
  var colors = ['gray', 'red', 'blue', 'black'];

  // Uncheck other colors and reset their styles
  colors.forEach(function (item) {
    if (item !== color) {
      document.getElementById(item).checked = false;
      var otherLabel = document.querySelector('label[for="' + item + '"]');
      otherLabel.style.backgroundColor = '';
      otherLabel.style.color = '';
      otherLabel.style.border = ''; // Reset border for other labels
    }
  });

  // Handle styling when the color is selected or unselected
  if (checkbox.checked) {
    selected_color.innerText = color.toUpperCase();
    final_color_input.value = color.toUpperCase();
    console.log(selected_color.innerText);
    label.style.borderColor = 'gray';
    label.style.borderStyle = 'solid';
    label.style.borderWidth = '3px'; // Set the border width
  } else {
    console.log(color + ' unselected');
    label.style.backgroundColor = '';
    label.style.border = ''; // Reset border when unchecked
  }
}

// Function to format a number to Indian currency format
function formatToIndianCurrency(number) {
  // Implement your currency formatting logic here
  // Example: Convert number to string, add commas, and append '₹'
  return '₹' + number.toLocaleString('en-IN');
}

// Your calculateTotals function
function calculateTotals() {
  const items = document.querySelectorAll('.item-price');
  let subtotal = 0;

  // Calculate subtotal based on item prices and quantities
  items.forEach((item) => {
    const price = parseFloat(item.innerText.replace('₹', '').replace(',', ''));
    const quantityId = item.id.replace('itemprice_', '');
    const itemName = item.getAttribute('data-name');
    const quantity = parseInt(document.getElementById(`numberDisplay_${quantityId}`).innerText);

    subtotal += price * quantity;
  });

  // Calculate taxes and total
  const taxRate = 0.1; // Replace with your tax rate
  const taxes = subtotal * taxRate;
  const total = subtotal + taxes;

  // Update HTML elements with formatted currency values
  document.getElementById('subtotal').innerText = formatToIndianCurrency(subtotal);
  document.getElementById('taxes').innerText = formatToIndianCurrency(taxes);
  document.getElementById('total_price').innerText = formatToIndianCurrency(total);
}

// Check if the current URL path includes "/cart/"
if (window.location.pathname.includes('/cart/')) {
  // Call the calculateTotals function when the DOM is ready
  document.addEventListener('DOMContentLoaded', calculateTotals);
}


// Function to format a number to Indian currency format
function formatToIndianCurrency(number) {
  // Implement your currency formatting logic here
  // Example: Convert number to string, add commas, and append '₹'
  return '₹' + number.toLocaleString('en-IN');
}


// Function to handle quantity changes
function handleCount(action, itemId) {
  const numberDisplay = document.getElementById(`numberDisplay_${itemId}`);
  let counts = parseInt(numberDisplay.innerText);

  // Increment or decrement item quantity based on action
  if (action === 'increment') {
    counts++;
  } else if (action === 'decrement' && counts > 1) {
    counts--;
  }

  numberDisplay.innerText = counts;

  // Update totals upon quantity change
  calculateTotals();
}

// Function to prepare and display order data
function displayData() {
  const items = document.querySelectorAll('.item-price');
  const orderDataInput = document.querySelector('input[name="order_data"]');

  let allItemsDetails = [];
  let subtotal = parseInt(document.getElementById('subtotal').innerText.replace('₹', '').replace(',', ''));
  let total = parseInt(document.getElementById('total_price').innerText.replace('₹', '').replace(',', ''));
  let payment_method = document.getElementById('payment_method').innerText;

  // Retrieve details for each item in the cart
  items.forEach((item) => {
    const price = parseFloat(item.innerText.replace('₹', '').replace(',', ''));
    const quantityId = item.id.replace('itemprice_', '');
    const itemName = item.getAttribute('data-name');
    const quantity = parseInt(document.getElementById(`numberDisplay_${quantityId}`).innerText);
    const size = item.getAttribute('data-size');
    const color = item.getAttribute('data-color');

    const itemDetails = {
      itemId: quantityId,
      itemName: itemName,
      itemPrice: price,
      itemQuantity: quantity,
      itemSize: size,
      itemColor: color,
    };
    allItemsDetails.push(itemDetails);
  });
  const finalData = {
    allItemsDetails: allItemsDetails,
    subtotal: subtotal,
    total: total,
    payment_method: payment_method
  };

  orderDataInput.value = JSON.stringify(finalData);
}

// Function to handle payment method selection
function handlePayment(paymentMethod) {
  const payment_method = document.getElementById('payment_method');
  payment_method.innerText = paymentMethod;
  if (paymentMethod === 'Card') {
    document.getElementById('card-holder').style.position = 'static';
    document.getElementById('card-details').style.position = 'static';
  } else {
    document.getElementById('card-holder').style.position = 'absolute';
    document.getElementById('card-details').style.position = 'absolute';
  }
}
// Event listener for card number and expiry input formatting
document.addEventListener('DOMContentLoaded', function () {
  const cardNumberInput = document.querySelector('#card-no');
  const expiryInput = document.querySelector('#credit-expiry');

  document.addEventListener('keyup', function (event) {
    if (event.target === cardNumberInput || event.target === expiryInput) {
      runcard();
    }
  });

  function runcard() {
    let cardNumber = cardNumberInput.value.replace(/\D/g, ''); // Remove non-numeric characters
    cardNumber = cardNumber.replace(/(\d{4})/g, '$1 ').trim(); // Add a space after every 4 characters
    cardNumberInput.value = cardNumber;

    let inputValue = expiryInput.value.replace(/\D/g, ''); // Remove non-numeric characters

    if (inputValue.length > 2) {
      // Insert a slash after the first two characters
      inputValue = inputValue.slice(0, 2) + '/' + inputValue.slice(2);
    }

    expiryInput.value = inputValue;
    }
  });

function submitForm() {
  document.getElementById("categoryForm").submit();
}

function togglePasswordVisibility(passwordInput, eyeIcon) {
  if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      eyeIcon.classList.add('hidden');
  } else {
      passwordInput.type = 'password';
      eyeIcon.classList.remove('hidden');
  }
};

