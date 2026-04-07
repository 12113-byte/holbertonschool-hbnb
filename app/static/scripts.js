document.addEventListener('DOMContentLoaded', () => {
    setupLoginForm();
    setupPlaceDetailsPage();
});


 // global variable

function getPlaceIdFromURL() {
    const queryParams = new URLSearchParams(window.location.search);
    const placeId = queryParams.get('id');
    return placeId
}

function getCookie(name) {
    const cookies = document.cookie.split('; ');
    const token = cookies.find(cookie => cookie.startsWith(name + '='));
    if (!token) {
      return null;
    }
    return token.split('=')[1];
}

function setCookie(name, value, maxAgeSeconds) {
    document.cookie = `${name}=${value}; path=/; max-age=${maxAgeSeconds}; SameSite=Lax`;
}

function showLoginError(message) {
    const errorElement = document.getElementById('login-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearLoginError() {
    const errorElement = document.getElementById('login-error');
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');
    if (!loginForm) {
        return;
    }

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        clearLoginError();

        const email = document.getElementById('email')?.value.trim();
        const password = document.getElementById('password')?.value;

        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ email, password })
            });

            const data = await response.json();
            if (!response.ok || !data.access_token) {
                showLoginError(data.error || 'Invalid email or password.');
                return;
            }

            // Keep both names for compatibility with existing scripts.
            setCookie('access_token', data.access_token, 86400);
            setCookie('token', data.access_token, 86400);
            window.location.href = '/';
        } catch (error) {
            console.error('Login request failed:', error);
            showLoginError('Unable to login right now. Please try again.');
        }
    });
}

function setupPlaceDetailsPage() {
    const placeDetailsSection = document.getElementById('place-details');
    if (!placeDetailsSection) {
        return;
    }

    const placeId = getPlaceIdFromURL();
    const token = getCookie('access_token') || getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (addReviewSection) {
        addReviewSection.style.display = token ? 'block' : 'none';
    }

    if (placeId) {
        fetchPlaceDetails(token, placeId);
    }
}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    try {
        const headers = { 'Content-Type': 'application/json' };
        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }

        const response = await fetch(`/api/v1/places/${placeId}`, {
            method: 'GET',
            headers
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        displayPlaceDetails(data);
    } catch (error) {
        console.error('Fetch error:', error);
    }
}

// append to the #place-details section.
function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    const placeDetails = document.getElementById('place-details');
    placeDetails.innerHTML = '';
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    // title
    const title = document.createElement('h2');
    title.textContent = place.place.title;
    title.classList.add('title');
    placeDetails.appendChild(title);

    // images
    const images = document.createElement('img');
    images.src = place.image;
    images.classList.add('img');
    placeDetails.appendChild(images);

    // description
    const description = document.createElement('p')
    description.textContent = "Description:" + place.place.description;
    description.classList.add('description');
    placeDetails.appendChild(description);

    // price
    const price = document.createElement('p');
    price.textContent = "Price per night" + place.place.price;
    price.classList.add('price');
    placeDetails.appendChild(price);

    // owner
    const owner = document.createElement('p');
    owner.textContent = "Owner" + place.owner.first_name + " " + place.owner.last_name;
    owner.classList.add('owner');
    placeDetails.appendChild(owner);

    // amenities
    const amenitiesTitle = document.createElement('h3');
    amenitiesTitle.textContent = 'Amenities';
    amenitiesTitle.classList.add('amenities-title');
    placeDetails.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement('ul');
    place.amenities.forEach(amenity => {
      const item = document.createElement('li');
      item.textContent = amenity;
      item.classList.add('amenity-item');
      amenitiesList.appendChild(item);
    });
    placeDetails.appendChild(amenitiesList);

    // reviews
    const reviewsTitle = document.createElement('h3');
    reviewsTitle.textContent = 'Reviews';
    reviewsTitle.classList.add('review-title');
    placeDetails.appendChild(reviewsTitle);

    place.reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.textContent = `Rating: ${review.rating} - ${review.text}`;
        placeDetails.appendChild(reviewDiv);
    });
}

// //Scritpts for add_review
// //Check authentication - redirect if no token
// function checkAuthentication() {
//         const token = getCookie('token');
//         if (!token) {
//             window.location.href = 'index.html';
//         }
//         return token;
//     }

//     //Helper: get cookie by name
//     function getCookie(name) {
//         const cookies = document.cookie.split(';');
//         for (let cookie of cookies) {
//             const [key, value] = cookie.trim().split('=');
//             const value = rest.join('=');
//             if (key == name) return value;
//         }
//         return null;
//     }

//     //Get place ID from URL query parameters
//     function getPlaceIdFromURL() {
//         const params = new URLSearchParams(window.location.search);
//         return params.get('place_id');
//     }

//     //Setup event listener for review form
//         document.addEventListener('DOMContentLoaded', () => {
//         const reviewForm = document.getElementById('review-form');
//             if (!reviewForm) return;

//         const token = checkAuthentication();
//         const placeId = getPlaceIdFromURL();

//         if (reviewForm) {
//             reviewForm.addEventListener('submit', async (event) => {
//                 event.preventDefault();
//                 const reviewText = document.getElementById('review').value;
//                 await submitReview(token, placeId, reviewText);
//             });
//         }
//     });

//     //Make AJAX request to submit review
//         async function submitReview(token, placeId, reviewText) {
//         try {
//             const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                     'Authorization': `Bearer ${token}`
//                 },
//                 body: JSON.stringify({
//                     place_id: placeId,
//                     text: reviewText,
//                     rating: parseInt(rating)
//                 })
//             });
//             handleResponse(response);
//         } catch (err) {
//             console.error('Error submitting review', err);
//             alert('Failed to submit review');
//         }
//     }

//     //Handle API response
//         function handleResponse(response) {
//         if (response.ok) {
//             alert('Review submitted successfully!');
//             document.getElementById('review-form').reset();
//         } else {
//             alert('Failed to submit review');
//         }
//     }
