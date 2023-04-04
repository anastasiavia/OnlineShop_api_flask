const form = document.querySelector('form');
form.addEventListener('submit', (event) => {
  event.preventDefault(); // Prevent the default form submission behavior
  const username = document.querySelector('#inputUsername').value;
  const password = document.querySelector('#inputPassword').value;
  fetch('http://127.0.0.1:5000/user/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  })
    .then(response => response.json())
    .then(data => {
      console.log(data.access_token);
    })
    .catch(error => console.error(error));
});