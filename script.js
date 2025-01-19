function getRecommendations() {
    // Get the user input
    const user_id = document.getElementById('user_id').value;
    const top_n = document.getElementById('top_n').value || 5; // default to 5 if empty

    if (!user_id) {
        alert('Please enter a valid User ID.');
        return;
    }

    // Fetch recommendations from the Flask API
    fetch(`http://127.0.0.1:5000/recommend?user_id=${user_id}&top_n=${top_n}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
            } else {
                displayRecommendations(data.recommendations, data.user_id);
            }
        })
        .catch(error => {
            alert('Error fetching recommendations: ' + error);
        });
}

function displayRecommendations(recommendations, user_id) {
    const recommendationsContainer = document.getElementById('recommendations');
    recommendationsContainer.innerHTML = ''; // Clear previous recommendations

    const userHeading = document.createElement('h2');
    userHeading.textContent = `Recommendations for User ${user_id}`;
    recommendationsContainer.appendChild(userHeading);

    recommendations.forEach(([item_id, predicted_rating]) => {
        const recommendationDiv = document.createElement('div');
        recommendationDiv.classList.add('recommendation');

        const itemTitle = document.createElement('h3');
        itemTitle.textContent = `Item ID: ${item_id}`;
        recommendationDiv.appendChild(itemTitle);

        const ratingText = document.createElement('p');
        ratingText.textContent = `Predicted Rating: ${predicted_rating.toFixed(2)}`;
        recommendationDiv.appendChild(ratingText);

        recommendationsContainer.appendChild(recommendationDiv);
    });
}
