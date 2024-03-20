function showEditModal(modalId, userId, userFirstname, userLastname, userNumber, userEmail, userPassword) {
  document.getElementById(modalId).classList.remove('hidden');
  document.getElementById('id').textContent = userId;
  document.getElementById('first_name').value = userFirstname;
  document.getElementById('last_name').value = userLastname;
  document.getElementById('mobile_number').value = userNumber;
  document.getElementById('email').value = userEmail;
  document.getElementById('password').value = userPassword;
}
function showDeleteModal(modalId, userId) {
  document.getElementById(modalId).classList.remove('hidden');
  document.getElementById('delete-userid').innerText = userId;
}

function closeModal(modalId) {
  document.getElementById(modalId).classList.add('hidden');
}

function confirmDelete() {
  const userId = document.getElementById('delete-userid').innerText;
  const deleteLink = document.createElement('a');
  deleteLink.href = `/delete_user/${userId}`;
  deleteLink.click();
  console.log("Run");
}


