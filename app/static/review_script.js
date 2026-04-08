//Scritpts for add_review
	//Helper: get cookie by name
	function getCookie(name) {
		const cookies = document.cookie.split(';');
		for (let cookie of cookies) {
			const [key, ...rest] = cookie.trim().split('=');
			const value = rest.join('=');
			if (key == name) return value;
		}
		return null;
	}

//Check authentication - redirect if no token
function checkAuthentication() {
		const token = getCookie('access_token');
		if (!token) {
			window.location.href = '/';
		}
		return token;
	}

	//Get place ID from URL query parameters
	function getPlaceIdFromURL() {
		const params = new URLSearchParams(window.location.search);
		return params.get('id');
	}

	//Setup event listener for review form
		document.addEventListener('DOMContentLoaded', () => {
		const reviewForm = document.getElementById('review-form');
			if (!reviewForm) return;

		const token = checkAuthentication();
		const placeId = getPlaceIdFromURL();

		if (reviewForm) {
			reviewForm.addEventListener('submit', async (event) => {
				event.preventDefault();
				const reviewText = document.getElementById('review').value;
				const rating = document.getElementByID('rating').value;
				await submitReview(token, placeId, reviewText, rating);
			});
		}
	});

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
			console.error('Error submitting review', err);
			alert('Failed to submit review');
		}
	}

	//Handle API response
		async function handleResponse(response) {
		if (response.ok) {
			alert('Review submitted successfully!');
			document.getElementById('review-form').reset();
		} else {
			alert('Failed to submit review');
		}
	}
