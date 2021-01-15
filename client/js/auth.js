const sendRequest = async (url, data) => {
    const response = await fetch(url, {
        method: 'POST',
        credentials: 'same-origin',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    });
    if (response.ok) {
        window.location.href = '/create';
    } else {
        console.error('Request failed');
    }
};

const submitLogin = async () => {
    const formData = {
        email: document.getElementById('username').value,
        password: document.getElementById('password').value,
    };
    sendRequest('api/login', formData);
};

const submitRegister = async () => {
    const formData = {
        email: document.getElementById('username').value,
        password: document.getElementById('password').value,
        name: document.getElementById('name').value,
    };
    sendRequest('api/register', formData);
};
