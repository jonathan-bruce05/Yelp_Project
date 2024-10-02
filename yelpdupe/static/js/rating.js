document.addEventListener('DOMContentLoaded', function() {
    const stars = document.querySelectorAll('.star');
    const ratingInput = document.getElementById('rating-value');

    stars.forEach(star => {
        // Hover effect: Highlight stars on hover
        star.addEventListener('mouseover', function() {
            resetStars(); // Clear all stars before highlighting on hover
            highlightStars(star);
        });

        // Remove hover effect when the mouse leaves
        star.addEventListener('mouseout', function() {
            resetStars(); // Clear all stars when the mouse leaves
            persistSelectedStars(); // Reapply the selected stars
        });

        // Handle click: Set the rating and maintain selected state
        star.addEventListener('click', function() {
            resetStars();
            highlightStars(star);
            star.classList.add('selected'); // Mark clicked star as selected
            ratingInput.value = star.getAttribute('data-value'); // Update hidden input with rating value
            persistSelectedStars(); // Persist the selected stars after click
        });
    });

    // Reset the star colors
    function resetStars() {
        stars.forEach(star => star.classList.remove('hover', 'selected'));
    }

    // Highlight the stars up to the hovered/clicked one
    function highlightStars(star) {
        const starValue = star.getAttribute('data-value');
        stars.forEach(s => {
            if (s.getAttribute('data-value') <= starValue) {
                s.classList.add('hover');
            }
        });
    }

    // Reapply the selected stars based on the current rating
    function persistSelectedStars() {
        const currentRating = ratingInput.value;
        if (currentRating) {
            stars.forEach(star => {
                if (star.getAttribute('data-value') <= currentRating) {
                    star.classList.add('selected');
                }
            });
        }
    }
});
