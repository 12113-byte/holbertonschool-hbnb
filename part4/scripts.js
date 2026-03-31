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
