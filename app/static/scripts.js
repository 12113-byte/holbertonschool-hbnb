/* 
    This is a SAMPLE FILE to get you started.
    Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    /* DO SOMETHING */
    });


const placeId = getPlaceIdFromURL(); // global variable

function getPlaceIdFromURL() {
    const queryParams = new URLSearchParams(window.location.search);
    const placeId = queryParams.get('id');
    return placeId
}

function checkAuthentication() {
    const token = getCookie('token');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
    }
    // fetching place details independently of guest or admin
    fetchPlaceDetails(token, placeId);
}

function getCookie(name) {
    // Function to get a cookie value by its name
    const cookies = document.cookie.split('; ');
    const token = cookies.find(cookie => cookie.startsWith(name + '='));
    if (!token) {
        return null
    }
    const extracted_name = token.split('=');
    return extracted_name[1]
}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    try {
        const response = await fetch(`http://127.0.1:5000/api/v1/places/${placeId}`, {
        method: 'GET',
        headers: {
          'Authorization': token ? `Bearer ${token}` : '', // if token exists, send it, otherwise send empty string
            'Content-Type': 'application/json'
        }
        });

        if (!response.ok) {
        throw new Error(`HHTP error! Status: ${response.status}`);
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
    placeDetails.appendChild(title);

    // description
    const description = document.createElement('p')
    description.textContent = `Description: ${place.place.description}`;
    placeDetails.appendChild(description);

    // price
    const price = document.createElement('p');
    price.textContent = `Price per night: ${place.place.price}`;
    placeDetails.appendChild(price);

    // owner
    const owner = document.createElement('p');
    owner.textContent = `Owner: ${place.owner.first_name} ${place.owner.last_name}`;
    placeDetails.appendChild(owner);

    // amenities
    const amenitiesTitle = document.createElement('h3');
    amenitiesTitle.textContent = 'Amenities';
    placeDetails.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement('ul');
    place.amenities.forEach(amenity => {
        const item = document.createElement('li');
        item.textContent = amenity;
        amenitiesList.appendChild(amenitiesList);
    });
    placeDetails.appendChild(amenitiesList);

    // reviews
    const reviewsTitle = document.createElement('h3');
    reviewsTitle.textContent = 'Reviews';
    placeDetails.appendChild(reviewsTitle);

    place.reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.textContent = `Rating: ${review.rating} - ${review.text}`;
        placeDetails.appendChild(reviewDiv);
    });
}

//Scritpts for add_review
//Check authentication - redirect if no token
function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            window.location.href = 'index.html';
        }
        return token;
    }

    //Helper: get cookie by name
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key == name) return value;
        }
        return null;
    }

    //Get place ID from URL query parameters
    function getPlaceIdFromURL() {
        const params = new URLSearchParams(window.location.search);
        return params.get('place_id');
    }

    //Setup event listener for review form
        document.addEventListener('DOMContentLoaded', () => {
        const reviewForm = document.getElementById('review-form');
        const token = checkAuthentication();
        const placeId = getPlaceIdFromURL();

        if (reviewForm) {
            reviewForm.addEventListener('submit', async (event) => {
                event.preventDefault();
                const reviewText = document.getElementById('review').value;
                await submitReview(token, placeId, reviewText);
            });
        }
    });

    //Make AJAX request to submit review
        async function submitReview(token, placeId, reviewText) {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({
                    place_id: placeId,
                    text: reviewText
                })
            });
            handleResponse(response);
        } catch (err) {
            console.error('Error submitting review', err);
            alert('Failed to submit review');
        }
    }

    //Handle API response
        function handleResponse(response) {
        if (response.ok) {
            alert('Review submitted successfully!');
            document.getElementById('review-form').reset();
        } else {
            alert('Failed to submit review');
        }
    }
