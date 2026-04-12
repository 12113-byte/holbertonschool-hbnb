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


// Adding a display message upon successful submission
function showSuccessAlert(message = "Rewview submitted!") {
	const toast = document.createElement("div");
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
	// 	document.addEventListener('DOMContentLoaded', () => {
	// 	const reviewForm = document.getElementById('review-form');
	// 		if (!reviewForm) return;

	// 	const token = checkAuthentication();
	// 	const placeId = getPlaceIdFromURL();

	// 	if (reviewForm) {
	// 		reviewForm.addEventListener('submit', async (event) => {
	// 			event.preventDefault();
	// 			const reviewText = document.getElementById('review').value;
	// 			const rating = document.getElementById('rating').value;
	// 			await submitReview(token, placeId, reviewText, rating);
	// 		});
	// 	}
	// });
	document.addEventListener('DOMContentLoaded', () => {
		const token = checkAuthentication();
		if (!token) return;

		const placeId = getPlaceIdFromURL();
		const reviewForm = document.getElementById('review-form');
		if (!reviewForm) return;

		reviewForm.addEventListener('submit', async (event) => {
			event.preventDefault();
			const reviewText = document.getElementById('review').value;
			const rating = document.getElementById('rating').value;
			await submitReview(token, placeId, reviewText, rating);
		});
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
			showSuccessAlert('Your review was successfully submitted!');
			document.getElementById('review-form').reset();
		} else {
			const data = await response.json();
			const message = data.error || 'Failed to submit review';
			showErrorAlert(message);
		}
	}

	function showErrorAlert(message) {
		const toast = document.createElement('div');
		toast.textContent = message;
		toast.style.cssText = `
			position: fixed;
			top: 20px;
			left: 50%;
			transform: translateX(-50%);
			background: #e74c3c;
			color: white;
			padding: 16px 32px;
			border-radius: 12px;
			font-size: 16px;
			box-shadow: 0 rpx 12px rgba(0,0,0,0,2);
			z-index: 9999;
			animation: fadeIn 0.3s ease;
		`;
		document.body.appendChild(toast);
		setTimeout(() => toast.remove(), 3000);
	}
