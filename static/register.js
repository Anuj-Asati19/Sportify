document.addEventListener("DOMContentLoaded", function() {
    const registrationForm = document.getElementById('registration-form');

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Get form data
        const formData = new FormData(registrationForm);
        const email = formData.get('email');
        const username = formData.get('username');

        // Make an AJAX request to the Flask server
        fetch('/register', {
            method: 'POST',
            body: JSON.stringify({ email: email, username: username }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Log the response from the server
            // You can perform additional actions here based on the server response
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
