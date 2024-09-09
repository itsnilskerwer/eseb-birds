// card-viewer.js
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.card');
   // const birdCardsContainer = document.querySelector('.bird-cards');
    const totalCards = cards.length;
    let currentIndex = 0;

    function showCard(index) {  // TODO invoke rescale in showCard
        cards.forEach((card, i) => {
            card.style.display = i === index ? 'block' : 'none';
        });
    }

    function showPreviousCard() {
        currentCardIndex = (currentCardIndex - 1 + totalCards) % totalCards;
        showCard(currentCardIndex);
    }

    function showNextCard() {
        currentCardIndex = (currentCardIndex + 1) % totalCards;
        showCard(currentCardIndex);
    }

   /*  function updateCardVisibility() {
        cards.forEach((card, index) => {
            card.style.display = index === currentIndex ? 'block' : 'none';
        });
    } */
/* 
    function updateFixedCard() {
        const fixedCard = document.querySelector('.fixed-card');
        if (fixedCard) {
            fixedCard.classList.remove('fixed-card');
        }
        cards[currentIndex].classList.add('fixed-card');
    }

    document.getElementById('prev-card').addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + cards.length) % cards.length;
        updateCardVisibility();
        updateFixedCard();
    });

    document.getElementById('next-card').addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % cards.length;
        updateCardVisibility();
        updateFixedCard();
    }); */
/*     function updateFixedCard() {
        const fixedCard = document.querySelector('.fixed-card');
        if (fixedCard) {
            fixedCard.classList.remove('fixed-card');
        }
        const currentCard = cards[currentIndex];
        currentCard.classList.add('fixed-card');
        resizeCardIfNeeded(currentCard);
    } */

       
 /*    function resizeCardIfNeeded(card) {
        const birdCardsRect = birdCardsContainer.getBoundingClientRect();
        const cardRect = card.getBoundingClientRect();

        if (cardRect.height > birdCardsRect.height || cardRect.width > birdCardsRect.width) {
            card.style.transform = 'scale(0.8)'; // Scale down if too large
        } else {
            card.style.transform = ''; // Reset scale if it fits
        }
    }
 */
   /*  document.getElementById('prev-card').addEventListener('click', showPreviousCard);
    document.getElementById('next-card').addEventListener('click', showNextCard); */

    // Initialize by showing the first card
/*     showCard(currentCardIndex); */
   /*  updateCardVisibility();
    updateFixedCard(); */
});
