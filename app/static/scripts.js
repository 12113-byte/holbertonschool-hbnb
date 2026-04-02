function checkAuthentication() {
	const token = getCookie('access_token');
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
	let x = document.cookie;
	console.log(x);
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
		let place_title = document.createElement("p");
		let place_desc = document.createElement("p");
		let place_price = document.createElement("p");
		let place_lat = document.createElement("p");
		let place_long = document.createElement("p");
		place_title.innerHTML = "name: " + places[i].title;
		place_desc.innerHTML = "description: " + places[i].description;
		place_price.innerHTML = "price: " + places[i].price;
		place_lat.innerHTML = "lat: " + places[i].latitude;
		place_long.innerHTML = "long: " + places[i].longitude;
		place.append(place_txt);
		place.append(place_desc);
		place.append(place_price);
		place.append(place_lat);
		place.append(place_long);
		place.classList.add("place-card");
		place_list.append(place);
	}
}

document.addEventListener('DOMContentLoaded', () => {
	/* DO SOMETHING */
	checkAuthentication()
	SetPriceVals()
	document.getElementById('price-filter').addEventListener('change', (event) => {
		const price_set = document.getElementById('price-filter').value;
		const place_list = document.body.getElementsByTagName('div')
		for(let i = 0; i < place_list.length; i++)
		{
			if (price_set == 10)
			{

			}
			else if (price_set == 50)
			{

			}
			else if (price_set == 100)
			{

			}
			else
			{
				place_list[i].style.display = "block";
			}
		}

		// Get the selected price value
		// Iterate over the places and show/hide them based on the selected price
	});
});
