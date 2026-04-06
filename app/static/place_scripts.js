document.addEventListener('DOMContentLoaded', () => {
    checkAuthentication();
  });


const placeId = getPlaceIdFromURL(); // global variable

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
    const extracted_name = token.split('=');
    return extracted_name[1];
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
    title.classList.add('title');
    placeDetails.appendChild(title);

    // images
    const images = document.createElement('img');
    images.src = place.place.image;
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
