document.addEventListener('DOMContentLoaded', () => {
    const access_token = checkAuthentication();
    setupLoginForm();
    setupLogout();
    IndexPageFunction(access_token);
    PlacePageFunction(access_token);
    ReviewPageFunction(access_token);
    ProfilePageFunction(access_token);
});
/*
* Common functions
*/
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

function checkAuthentication() {
    const token = getCookie('access_token');
    const loginLink = document.getElementById('login-link');
    const profileLink = document.getElementById('profile-link');
    const logoutLink = document.getElementById('logout-link');

    if (!token) {
        loginLink.style.display = 'block';
        profileLink.style.display = 'none';
        logoutLink.style.display = 'none';
    } else {
        loginLink.style.display = 'none';
        profileLink.style.display = 'block';
        logoutLink.style.display = 'block';
    }
    return token;
}

    // function for stars in rating
function getStars(rating) {
    return '★'.repeat(rating) + '☆'.repeat(5 - rating);
}

function createPlaceCards(place){
    let card = document.createElement("div");
    let place_title = document.createElement("h2");
    let place_desc = document.createElement("p");
    let place_price = document.createElement("p");
    let place_price_span = document.createElement("span");

    place_title.innerHTML = place.title;
    place_desc.innerHTML = place.description;
    place_desc.classList.add("place-desc");

    place_price.innerHTML = "$";
    place_price_span.innerHTML = place.price;
    place_price.append(place_price_span);
    place_price.innerHTML += " per night";
    place_price.classList.add("place-price");

    card.append(place_title);
    card.append(place_desc);
    card.append(place_price);

    card.classList.add("place-card");
    card.addEventListener("click", OpenPlace, false);
    card.placeId = place.id;

    return card;
}

/*
* Common functions
*/

/*
* Index page functions
*/
function IndexPageFunction(access_token){
    const price_filter = document.getElementById('price-filter');
    if (!price_filter) {
        return;
    }

    const price_filer_values = ['All', 10, 50, 100]
    for (let i = 0; i < price_filer_values.length; i++){
        let option = document.createElement("option");
        option.text = price_filer_values[i];
        price_filter.add(option);
    }

    document.getElementById('price-filter').addEventListener('change', (event) => {
        const price_filter_val = document.getElementById('price-filter').value;
        const places_list = document.body.getElementsByTagName('div')
        for(let i = 0; i < places_list.length; i++)
        {
            if (price_filter_val == "All")
            {
                places_list[i].style.display = "block";
            }
            else
            {
                let place_price = places_list[i].getElementsByTagName('span')[0].innerHTML;
                if (place_price != undefined)
                {
                    if (Number(place_price) > Number(price_filter_val))
                    {
                        places_list[i].style.display = "none";
                    }
                    else
                    {
                        places_list[i].style.display = "block";
                    }
                }
            }
        }
    });
    fetchPlaces(access_token);
}

async function fetchPlaces(token) {
    await fetch("/api/v1/places", {
        method: "GET",
        headers: {'Authorization': token ? `Bearer ${token}` : ''}
    }).then(function (response){
        if (response.ok)
        {
            return response.json();
        }
        else
        {
            showErrorAlert("Error retrieving places - Please try again later");
        }
    }).then(function (response){
        displayPlaces(response)
    });
}

function displayPlaces(places) {
    const places_list = document.getElementById('places-list');
    while(places_list.firstChild){
        places_list.removeChild(places_list.firstChild);
    }

    for(let i = 0; i < places.length; i++)
    {
        places_list.append(createPlaceCards(places[i]));
    }
}

async function OpenPlace(evt){
    window.location.href = "/place?id=" + evt.currentTarget.placeId;
}

/*
* Index page functions
*/

/*
* Place Page Functions
*/
function PlacePageFunction(access_token){
    const placeDetails = document.getElementById('place-details');
    const addReviewSection = document.getElementById('add-review');
    const AddReviewBtn = document.getElementById('add_review_button');
    const placeId = getPlaceIdFromURL();

    if (!placeDetails) return;

    if (!AddReviewBtn) {
        console.error('add_review_button not found in DOM');
        return;
    }

    if (!access_token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
    }
    AddReviewBtn.placeId = placeId;
    AddReviewBtn.addEventListener("click", AddReview, false);
    fetchPlaceDetails(access_token, placeId);
}

async function AddReview(evt){
    window.location.href = "/add_review?id=" + evt.currentTarget.placeId;
}

function getPlaceIdFromURL() {
    const queryParams = new URLSearchParams(window.location.search);
    const placeId = queryParams.get('id');
    return placeId;
}

async function fetchPlaceDetails(token, placeId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    try {
        const response = await fetch('/api/v1/places/' +  placeId, {
            method: 'GET',
            headers: {
                'Authorization': token ? `Bearer ${token}` : '', // if token exists, send it, otherwise send empty string
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();

        //Checks the user
        /*
        let currentUser = null; // fetching current user, if logged in
        if (token) {
            const userResponse = await fetch('/api/v1/users/me', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (userResponse.ok) {
                currentUser = await userResponse.json();
            }
        }*/
        displayPlaceDetails(data);
    } catch (error) {
        console.error('Fetch error:', error);
    }
}



function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');

    // safer than innerHTML = ''
    placeDetails.replaceChildren();

    // title
    const title = document.createElement('h2');
    title.textContent = place.place.title;
    title.classList.add('title');
    placeDetails.appendChild(title);

    // image
    const image = document.createElement('img');
    image.src = place.place.image_url;
    image.classList.add('place-image');
    placeDetails.appendChild(image);

    // place-info div (the two-column row)
    const placeInfoDiv = document.createElement('div');
    placeInfoDiv.classList.add('place-info');

    // left side: description + owner grouped together
    const leftDiv = document.createElement('div');

    const description = document.createElement('p');
    description.textContent = "Description: " + place.place.description;
    description.classList.add('description');

    const owner = document.createElement('p');
    owner.textContent = "Owner: " + place.owner.first_name + " " + place.owner.last_name;
    owner.classList.add('owner');

    leftDiv.appendChild(description);
    leftDiv.appendChild(owner);

    // right side: price
    const price = document.createElement('p');
    price.textContent = "Price per night: $" + place.place.price;
    price.classList.add('price');

    placeInfoDiv.appendChild(leftDiv);
    placeInfoDiv.appendChild(price);
    placeDetails.appendChild(placeInfoDiv);

    if (place.owner.auth == "True") {
        const editButton = document.createElement('button');
        editButton.textContent = 'Edit Place';
        editButton.classList.add('booking-button');
        editButton.addEventListener('click', () => {
            showPlaceEditForm(place, currentUser);
        });
        placeDetails.appendChild(editButton);
    }

    // divider
    const hr = document.createElement('hr');
    placeDetails.appendChild(hr);

    // amenities
    const amenitiesTitle = document.createElement('h3');
    amenitiesTitle.textContent = 'Amenities';
    amenitiesTitle.classList.add('amenities-title');
    placeDetails.appendChild(amenitiesTitle);

    const amenitiesList = document.createElement('ul');
    amenitiesList.classList.add('amenities-list');
    place.amenities.forEach(amenity => {
        const item = document.createElement('li');
        item.textContent = amenity.name;
        item.classList.add('amenity-item');
        amenitiesList.appendChild(item);
    });
    placeDetails.appendChild(amenitiesList);

    // reviews
    const reviewsSection = document.getElementById('reviews');
    reviewsSection.replaceChildren();

    const reviewsTitle = document.createElement('h3');
    reviewsTitle.textContent = 'Reviews';
    reviewsTitle.classList.add('review-title');
    reviewsSection.appendChild(reviewsTitle);

    place.reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        const userReviewer = document.createElement('p');
        userReviewer
        reviewDiv.classList.add('review');
        reviewDiv.textContent = `${getStars(review.rating)} - ${review.text}`;
        reviewsSection.appendChild(reviewDiv);
    });
}

function showPlaceEditForm(place, currentUser) {
    const existing = document.getElementById('place-edit-form');
    if (existing) { existing.remove(); return; }

    const form = document.createElement('div');
    form.id = 'place-edit-form';

    const fields = [
        { label: 'Title', field: 'title', value: place.place.title },
        { label: 'Description', field: 'description', value: place.place.description },
        { label: 'Price', field: 'price', value: place.place.price },
    ];

    // additional fields for admin
    if (currentUser.is_admin) {
        fields.push(
        { label: 'Latitude', field: 'latitude', value: place.place.latitude },
        { label: 'Longitude', field: 'longitude', value: place.place.longitude },
        );
    }

    fields.forEach(({ label, field, value }) => {
        const row = document.createElement('p');
        const strong = document.createElement('strong');
        strong.textContent = `${label}: `;

        const input = document.createElement('input');
        input.value = value;
        input.dataset.field = field;

        row.appendChild(strong);
        row.appendChild(input);
        form.appendChild(row);
    });

    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save Changes';
    saveButton.classList.add('booking-button');
    saveButton.addEventListener('click', async () => {
        const inputs = form.querySelectorAll('input');
        const data = {};
        const numericFields = ['price', 'latitude', 'longitude'];
        inputs.forEach(input => {
            const val = input.value;
            data[input.dataset.field] = numericFields.includes(input.dataset.field) ? parseFloat(val) : val;
        });

        const token = getCookie('access_token');
        const response = await fetch(`/api/v1/places/${place.place.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showSuccessAlert('Place updated!');
            form.remove();
            fetchPlaceDetails(token, place.place.id);
        } else {
            const err = await response.json();
            showErrorAlert(err.error || 'Update failed');
        }
    });

    form.appendChild(saveButton);
    document.getElementById('place-details').appendChild(form);
}
/*
* Place Page Functions
*/

/*
* Add Review Functions
*/
// Adding a display message upon successful submission
function showSuccessAlert(message) {
    const toast = document.createElement("div");
    if (message == undefined)
    {
        message = "Success!"
    }
    toast.textContent = message;
    toast.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #4CAF50;
    color: white;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0,2);
    z-index: 9999;
    animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
function showErrorAlert(message) {
    const toast = document.createElement("div");
    if (message == undefined)
    {
        message = "Unexpected Error Occurred"
    }
    toast.textContent = message;
    toast.style.cssText = `
    position: fixed;
    top: 20px;
    left: 50%;
    transform: translateX(-50%);
    background: #CC3535;
    color: white;
    padding: 16px 32px;
    border-radius: 12px;
    font-size: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0,2);
    z-index: 9999;
    animation: fadeIn 0.3s ease;
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 3000);
}
function ReviewPageFunction(access_token){
    const reviewForm = document.getElementById('review-form');
    if (!reviewForm){
        return;
    }
    if (!access_token)
    {
        window.location.href = '/login';
    }
    const placeId = getPlaceIdFromURL();

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const reviewText = document.getElementById('review').value;
            const rating = document.getElementById('rating').value;
            await submitReview(access_token, placeId, reviewText, rating);
        });
    }
}

//Make AJAX request to submit review
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch('/api/v1/reviews/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                place_id: placeId,
                text: reviewText,
                rating: parseInt(rating)
            })
        });
        handleResponse(response);
    } catch (err) {
        console.error(err.message);
    }
}

//Handle API response
async function handleResponse(response) {
    let res = await response.json()
    if (response.ok) {
        showSuccessAlert("Review submitted!");
        document.getElementById('review-form').reset();
    } else {
        console.log(res.error);
        showErrorAlert(res.error);
        //alert(res.error);
    }
}
/*
* Add Review Functions
*/

/*
* login page functions
*/
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
                body: JSON.stringify({email, password })
            });

            const data = await response.json();
            if (!response.ok || !data.access_token) {
                showLoginError(data.error || 'Invalid email or password.');
                return;
            }

            // Keep both names for compatibility with existing scripts.
            setCookie('access_token', data.access_token, 86400);
            window.location.href = '/';
        } catch (error) {
            console.error('Login request failed:', error);
            showLoginError('Unable to login right now. Please try again.');
        }
    });
}

function setCookie(name, value, maxAgeSeconds) {
    document.cookie = `${name}=${value}; path=/; max-age=${maxAgeSeconds}; SameSite=Lax`;
}

function clearLoginError() {
    const errorElement = document.getElementById('login-error');
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}

function showLoginError(message) {
    const errorElement = document.getElementById('login-error');
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}
/*
* login page functions
*/

/*
* Logout page functions
*/

function setupLogout() {
    const logoutLink = document.getElementById('logout-link');
    if (!logoutLink) return;

    logoutLink.addEventListener('click', (event) => {
        event.preventDefault();
        document.cookie = 'access_token=; max-age=0; path=/;';
        window.location.href = '/';
    });
}

/*
* Logout page function
*/

/*
* Profil Page functions
*/

function ProfilePageFunction(access_token) {
    const profileDetails = document.getElementById('profile-details');
    if (!profileDetails) return;

    if (!access_token) {
        window.location.href = '/login';
        return;
    }
    fetchProfile(access_token);
}

async function fetchProfile(token) {
    try {
        const response = await fetch('/api/v1/users/me', {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) throw new Error('Failed to fetch profile');
        const user = await response.json();
        displayProfile(user, token);
    } catch (error) {
        console.error('Profile fetch error', error);
    }
}

function displayProfile(user, token) {
    // User Info
    const profileDetails = document.getElementById('profile-details');
    profileDetails.replaceChildren();

    const heading = document.createElement('h2');
    heading.textContent = `${user.first_name} ${user.last_name}`;
    heading.classList.add('title');

    const email = document.createElement('p');
    email.textContent = `Email: ${user.email}`;

    const userId = document.createElement('p');
    userId.textContent = `User ID: ${user.id}`;
    userId.classList.add('owner');

    const editInfoButton = document.createElement('button');
    editInfoButton.textContent = 'Edit Information';
    editInfoButton.classList.add('booking-button');
    editInfoButton.addEventListener('click', () => {
        showUserEditForm(user, token);
    });

    profileDetails.appendChild(heading);
    profileDetails.appendChild(email);
    profileDetails.appendChild(userId);
    profileDetails.appendChild(editInfoButton);

    displayProfilePlaces(user.places, token);
    displayProfileReviews(user.reviews, token);
}

function displayProfilePlaces(places, token) {
    const section = document.getElementById('profile-places');
    section.replaceChildren();

    const title = document.createElement('h3');
    title.textContent = 'My Places';
    title.classList.add('amenities-title');
    section.appendChild(title);

    places.forEach(place => {
        section.appendChild(createPlaceCards(place));
    });
}

function displayProfileReviews(reviews, token) {
    const section = document.getElementById('profile-reviews');
    section.replaceChildren();

    const title = document.createElement('h3');
    title.textContent = 'My Reviews';
    title.classList.add('review-title');
    section.appendChild(title);

    reviews.forEach(review => {
        const reviewDiv = document.createElement('div');
        reviewDiv.classList.add('review');

        // updateable fields
        const fields = [
            { label: 'Rating', field: 'rating', value: review.rating },
            { label: 'Review', field: 'text', value: review.text }
        ];

        fields.forEach(({ label, field, value }) => {
            const p = document.createElement('p');
            const strong = document.createElement('strong');
            strong.textContent = `${label}: `;

            const span = document.createElement('span');
            span.classList.add('editable');
            span.dataset.field = field;
            span.dataset.id = review.id;
            span.dataset.type ='review';
            span.textContent = field == 'rating' ? getStars(value) : value;

            p.appendChild(strong);
            p.appendChild(span);
            reviewDiv.appendChild(p);
        });

        section.appendChild(reviewDiv);
    });
}

function setupInlineEditing(token) {
    document.querySelectorAll('.editable').forEach(span => {
        span.style.cursor = 'pointer';
        span.title = 'Click to edit';

        span.addEventListener('click', function () {
            if (this.querySelector('input')) return; // already editing

            const original = this.textContent;
            const field = this.dataset.field;
            const id = this.dataset.id;
            const type = this.dataset.type || 'place';

            const input = document.createElement('input');
            input.value = original;
            this.textContent = '';
            this.appendChild(input);
            input.focus();

            input.addEventListener('keydown', async (e) => {
                if (e.key === 'Enter') {
                    const newValue = input.value.trim();
                    const success = await saveEdit(token, type, id, field, newValue);
                    span.textContent = success ? newValue : original;
                }
                if (e.key === 'Escape') {
                    span.textContent = original;
                }
            });

            input.addEventListener('blur', async () => {
                const newValue = input.value.trim();
                const success = await saveEdit(token, type, id, field, newValue);
                span.textContent = success ? newValue : original;
            });
        });
    });
}

async function saveEdit(token, type, id, field, newValue) {
    const url = type === 'review'
        ? `/api/v1/reviews/${id}`
        : `/api/v1/places/${id}`;

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ [field]: newValue })
        });
        if (response.ok) {
            showSuccessAlert('Saved!');
            return true;
        } else {
            const err = await response.json();
            showErrorAlert(err.error || 'Update failed');
            return false;
        }
    } catch (error) {
        showErrorAlert('Something went wrong');
        return false;
    }
}

function showUserEditForm(user, token) {
    const existing = document.getElementById('user-edit-form');
    if (existing) { existing.remove(); return; }

    const form = document.createElement('div');
    form.id = 'user-edit-form';
    form.classList.add('edit-form');

    const fields = [
        { label: 'First Name', field: 'first_name', value: user.first_name },
        { label: 'Last Name', field: 'last_name', value: user.last_name }
    ];

    // extra options for admin
    if (user.is_admin) {
        fields.push({ label: 'Email', field: 'email', value: user.email });
    }

    fields.forEach(({ label, field, value }) => {
        const row = document.createElement('p');
        const strong = document.createElement('strong');
        strong.textContent = `${label}: `;

        const input = document.createElement('input');
        input.value = value;
        input.dataset.field = field;
        input.classList.add('edit-input');

        row.appendChild(strong);
        row.appendChild(input);
        form.appendChild(row);
    });

    const saveButton = document.createElement('button');
    saveButton.textContent = 'Save Changes';
    saveButton.classList.add('booking-button');
    saveButton.addEventListener('click', async () => {
        const inputs = form.querySelectorAll('input');
        const data = {};
        inputs.forEach(input => {
            data[input.dataset.field] = input.value;
        });

        const response = await fetch(`/api/v1/users/${user.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            showSuccessAlert('Information updated!');
            form.remove();
            fetchProfile(token); // reload profile to show updated values
        } else {
            const err = await response.json();
            showErrorAlert(err.error || 'Update failed');
        }
    });

    form.appendChild(saveButton);
    document.getElementById('profile-details').appendChild(form);
}
/*
* Profil Page functions
*/
