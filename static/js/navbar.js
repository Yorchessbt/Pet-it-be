document.addEventListener('DOMContentLoaded', () => {
    const checkbox = document.getElementById('check-icon');
    const navFullscreen = document.getElementById('navbarNav');

    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            navFullscreen.classList.add('show');
        } else {
            navFullscreen.classList.remove('show');
        }
    });
});
