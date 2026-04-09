document.addEventListener('DOMContentLoaded', () => {
	const access_token = checkAuthentication();
	setupLoginForm();
	IndexPageFunction(access_token);
	PlacePageFunction(access_token);
	ReviewPageFunction(access_token);
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

	if (!token) {
		loginLink.style.display = 'block';
	} else {
		loginLink.style.display = 'none';
	}
	return token;
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
			alert("Error retrieving places - Please try again later")
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

	console.log(places);
	for(let i = 0; i < places.length; i++)
	{
		let place = document.createElement("div");
		let place_title = document.createElement("h2");
		let place_desc = document.createElement("p");
		let place_price = document.createElement("p");
		let place_price_span = document.createElement("span");

		place_title.innerHTML = places[i].title;
		place_desc.innerHTML = places[i].description;
		place_desc.classList.add("place-desc");
		place_price.innerHTML = "Price/night ($): ";
		place_price_span.innerHTML = places[i].price;
		place_price.append(place_price_span);
		place_price.classList.add("place-price");
		place.append(place_title);
		place.append(place_desc);
		place.append(place_price);

		place.classList.add("place-card");
		place.addEventListener("click", OpenPlace, false);
		place.placeId = places[i].id;
		places_list.append(place);
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
	const AddReviewBtn = document.getElementById('add_review_btn');
	const placeId = getPlaceIdFromURL();
	if (!placeDetails) {
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
		displayPlaceDetails(data);
	} catch (error) {
		console.error('Fetch error:', error);
	}
}

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
	images.src = place.place.image_url;
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
		item.textContent = amenity.name;
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
/*
* Place Page Functions
*/

/*
* Add Review Functions
*/
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
		const response = await fetch('/api/v1/reviews', {
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
		console.log(response);
		if (!response.ok)
		{
			throw new Error(response)
		}
		alert('Review submitted successfully!');
		document.getElementById('review-form').reset();
		window.location.href = "/";
	} catch (err) {
		console.error('Error submitting review', err);
		alert(err.status + " - " + err.statusText);
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


