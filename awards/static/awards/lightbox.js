/**
 * Screenshot Lightbox Modal
 * Handles opening, closing, and navigating through game screenshots.
 */
document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('screenshotModal');
    if (!modal) return;

    const modalImg = document.getElementById('modalImage');
    const modalCounter = document.getElementById('modalCounter');
    const screenshotGrid = document.querySelector('.screenshots-grid');

    // Read screenshot URLs from data attributes on each thumbnail
    const screenshots = [];
    if (screenshotGrid) {
        screenshotGrid.querySelectorAll('.screenshot-thumb').forEach(function (thumb) {
            screenshots.push(thumb.dataset.full);
        });
    }

    if (screenshots.length === 0) return;

    let currentIndex = 0;

    window.openLightbox = function (index) {
        currentIndex = index;
        modalImg.src = screenshots[currentIndex];
        modalCounter.textContent = (currentIndex + 1) + ' / ' + screenshots.length;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    };

    window.closeLightbox = function () {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    };

    window.closeLightboxOutside = function (e) {
        if (e.target === modal) window.closeLightbox();
    };

    window.navigateLightbox = function (direction) {
        currentIndex = (currentIndex + direction + screenshots.length) % screenshots.length;
        modalImg.src = screenshots[currentIndex];
        modalCounter.textContent = (currentIndex + 1) + ' / ' + screenshots.length;
    };

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
        if (!modal.classList.contains('active')) return;
        if (e.key === 'Escape') window.closeLightbox();
        if (e.key === 'ArrowLeft') window.navigateLightbox(-1);
        if (e.key === 'ArrowRight') window.navigateLightbox(1);
    });
});
