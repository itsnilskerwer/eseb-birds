// tree-viewer.js
document.addEventListener("DOMContentLoaded", function() {
    const birds = document.querySelectorAll('.bird');
    const treeContainer = document.querySelector('.tree'); // Select the tree container

    birds.forEach(bird => {
        bird.addEventListener('click', function(event) {
            event.preventDefault();

            const hideElement = this.nextElementSibling;
            const isVisible = hideElement.style.display === 'block';

            // Hide all other images
            document.querySelectorAll('.hide').forEach(el => {
                el.style.display = 'none';
            });

            // Toggle the visibility of the clicked image
            hideElement.style.display = isVisible ? 'none' : 'block';
        });
    });

    // Add click listener to the document to hide images when clicking outside
    treeContainer.addEventListener('click', function(event) {
        if (!event.target.closest('.bird') && !event.target.closest('.hide')) {
            document.querySelectorAll('.hide').forEach(el => {
                el.style.display = 'none';
            });
        }
    });
});
