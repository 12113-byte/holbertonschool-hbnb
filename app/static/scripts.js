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
	fetchPlaces(token);
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
		headers: {"Authorization": token ? 'Bearer ' + token : ''}
	}).then(function (response){
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
	const places_list = document.getElementById('places-list');
	/*
	while(places_list.firstChild){
		places_list.removeChild(places_list.firstChild);
	}
	*/
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
		place.addEventListener("click", ClickDiv, false);
		place.placeId = places[i].id;
		places_list.append(place);
	}
}

function ClickDiv(evt){
	window.location.href = "/place?id=" + evt.currentTarget.placeId;
}

document.addEventListener('DOMContentLoaded', () => {
	/* DO SOMETHING */
	checkAuthentication()
	SetPriceVals()
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
});
