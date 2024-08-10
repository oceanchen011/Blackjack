function login() {
    // Construct the query string for the GET request
    const username = encodeURIComponent(document.getElementById("username-field").value);
    const password = encodeURIComponent(document.getElementById("password-field").value);
    const rememberMe = document.getElementById("remember-field").checked ? 'on' : 'off';
    const queryString = `username=${username}&password=${password}&remember_me=${rememberMe}`;

    // Send the GET request with the query string
    fetch(`/login?${queryString}`, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
    }).then(response => {
        if (response.redirected) {
            window.location.href = response.url; // Follow the redirect manually
        } else if (response.ok) {
            // Handle the 200 OK response
            response.json().then(data => {
                console.log('Login successful:', data);
                // Additional handling here if needed
            });
        } else {
            // Handle other statuses (e.g., 401 Unauthorized)
            response.json().then(data => {
                console.error('Login error:', data);
                alert('Login failed: ' + data.message);
            });
        }
    }).catch(error => {
        console.error('Error during login:', error);
        alert('Login failed due to a network error.');
    });
}

// Attach the event listener to the submit button
document.getElementById("submit").addEventListener("click", login);
