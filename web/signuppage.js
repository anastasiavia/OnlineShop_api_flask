const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault();
  const username = document.querySelector('#inputUsername').value;
  const firstname = document.querySelector('#inputName').value;
  const lastname = document.querySelector('#inputSurname').value;
  const email = document.querySelector('#inputEmail').value;
  const password = document.querySelector('#inputPassword').value;
  const phone = document.querySelector('#inputPhone').value;

  const data = {
    username,
    firstname,
    lastname,
    email,
    password,
    phone
  };

  fetch('http://localhost:5000/user', {
    method: 'POST',
    body: JSON.stringify(data),
    headers: {
      'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      console.log('User created:', data.userId);
      // add success message or redirect to another page
    })
    .catch(error => {
      console.error('Error creating user:', error.message);
      // add error message
    });
})