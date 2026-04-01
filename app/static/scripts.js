function checkAuthentication() {
	const token = getCookie('token');
	const loginLink = document.getElementById('login-link');

	if (!token) {
		loginLink.style.display = 'block';
		fetchPlaces("testing items");
	} else {
		loginLink.style.display = 'none';
		// Fetch places data if the user is authenticated
		fetchPlaces(token);
	}
}
function getCookie(name) {
	// Function to get a cookie value by its name
	// Your code here
}

function SetPriceVals(){
	const price_filer_values = ['All', 10, 50, 100]
	const price_filter = document.getElementById('price-filter');
	for (let i = 0; i < price_filer_values.length; i++){
		let option = document.createElement("option");
		option.text = price_filer_values[i];
		price_filter.add(option);
	}
}

async function fetchPlaces(token) {
	// Make a GET request to fetch places data
	// Include the token in the Authorization header
	// Handle the response and pass the data to displayPlaces function
	await fetch("/api/v1/places", {
		method: "GET",
		headers: {"Authorization": token}
	}).then(function (response){
		console.log(response.status)
		return response.json();
	}).then(function (response){
		displayPlaces(response)
	});
}
function displayPlaces(places) {
	// Clear the current content of the places list
	// Iterate over the places data
	// For each place, create a div element and set its content
	// Append the created element to the places list
	const place_list = document.getElementById('places-list');
	for(let i = 0; i < places.length; i++)
	{
		console.log(places);
		let place = document.createElement("div");
		let place_txt = document.createElement("p");
		let place_price = document.createElement("p");
		place_txt.innerHTML = "name: " + places[i].title;
		place_price.innerHTML = "price: " + places[i].price;
		place.append(place_txt);
		place.append(place_price);
		place_list.append(place);
	}
}

document.addEventListener('DOMContentLoaded', () => {
	/* DO SOMETHING */
	checkAuthentication()
	SetPriceVals()
	document.getElementById('price-filter').addEventListener('change', (event) => {
		console.log("price-filter changed");
		// Get the selected price value
		// Iterate over the places and show/hide them based on the selected price
	});
});


