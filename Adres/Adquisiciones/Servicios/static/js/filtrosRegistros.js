
document.addEventListener('DOMContentLoaded', function () {
    const toggleFiltersButton = document.getElementById('toggle-filters');

    if (toggleFiltersButton) {
        toggleFiltersButton.addEventListener('click', function () {
            const filtersForm = document.getElementById('filters-form');

            if (filtersForm) {
                if (filtersForm.style.display === 'none' || filtersForm.style.display === '') {
                    filtersForm.style.display = 'block';
                } else {
                    filtersForm.style.display = 'none';
                }
            }
        });
    }
});

