document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const table = document.getElementById('resultsTable');
    const rows = table ? table.getElementsByTagName('tr') : [];
    let offset = 0;
    const limit = 100;
    let loading = false;

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const filter = searchInput.value.toLowerCase();
            for (let i = 1; i < rows.length; i++) {
                const cells = rows[i].getElementsByTagName('td');
                let match = false;
                for (let j = 0; j < cells.length; j++) {
                    if (cells[j].innerText.toLowerCase().includes(filter)) {
                        match = true;
                        break;
                    }
                }
                rows[i].style.display = match ? '' : 'none';
            }
        });
    }

    const nextPageButton = document.getElementById('nextPage');
    const prevPageButton = document.getElementById('prevPage');

    if (nextPageButton) {
        nextPageButton.addEventListener('click', function() {
            if (!loading) {
                loading = true;
                offset += limit;
                fetchPage();
            }
        });
    }

    if (prevPageButton) {
        prevPageButton.addEventListener('click', function() {
            if (!loading && offset > 0) {
                loading = true;
                offset -= limit;
                fetchPage();
            }
        });
    }

    function fetchPage() {
        const filterForm = document.getElementById('filterForm');
        const formData = new FormData(filterForm);
        formData.append('offset', offset);

        fetch('/query', {
            method: 'POST',
            body: new URLSearchParams(formData)
        })
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, 'text/html');
            const newRows = doc.querySelectorAll('#resultsTable tbody tr');
            table.querySelector('tbody').innerHTML = '';
            newRows.forEach(row => table.querySelector('tbody').appendChild(row));
            prevPageButton.disabled = offset === 0;
            loading = false;
        })
        .catch(error => {
            console.error('Error fetching page:', error);
            loading = false;
        });
    }
});

// Variables para la paginación de la consulta de coches
let currentOffset = 0;
const limit = 100;
let loading = false;

function loadCars(offset, append = false) {
    if (loading) return;
    loading = true;
    
    const formData = new FormData(document.getElementById('queryForm'));
    
    // Mostrar estado de carga
    const tbody = document.getElementById('carsTableBody');
    if (!append) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center">Loading...</td></tr>';
    }
    
    fetch(`/query?offset=${offset}&limit=${limit}`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Network response was not ok');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }

        if (!append) {
            tbody.innerHTML = '';
        }
        
        if (data.cars.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="text-center">No results found</td></tr>';
            return;
        }
        
        data.cars.forEach(car => {
            const row = `
                <tr>
                    <td>${car.vin || 'N/A'}</td>
                    <td>
                        <strong>${car.make} ${car.model}</strong><br>
                        ${car.year} ${car.trim || ''}<br>
                        ${car.body_style || 'N/A'}
                    </td>
                    <td>
                        <strong>${car.listing_price ? '$' + Number(car.listing_price).toLocaleString() : 'N/A'}</strong><br>
                        ${car.listing_mileage ? Number(car.listing_mileage).toLocaleString() + ' miles' : 'N/A'}<br>
                        ${car.listing_date || 'N/A'}
                        ${car.is_certified ? '<br><span class="badge bg-success">Certified</span>' : ''}
                    </td>
                    <td>
                        ${car.engine || 'N/A'}<br>
                        ${car.transmission || 'N/A'}<br>
                        ${car.drivetrain || 'N/A'}<br>
                        ${car.fuel_type || 'N/A'}
                    </td>
                    <td>
                        Ext: ${car.exterior_color || 'N/A'}<br>
                        Int: ${car.interior_color || 'N/A'}
                    </td>
                    <td>
                        <strong>${car.dealer_name || 'N/A'}</strong><br>
                        ${car.dealer_city || ''}, ${car.dealer_state || ''} ${car.dealer_zip || ''}
                    </td>
                    <td>
                        ${car.status || 'N/A'}
                        ${car.theft_title ? '<br><span class="badge bg-danger">Theft Title</span>' : ''}
                        ${car.salvage_title ? '<br><span class="badge bg-warning">Salvage Title</span>' : ''}
                    </td>
                </tr>
            `;
            tbody.insertAdjacentHTML('beforeend', row);
        });
        
        // Actualizar información de paginación
        document.getElementById('pageInfo').textContent = 
            `Showing ${offset + 1}-${offset + data.cars.length} of ${data.total_count}`;
        
        document.getElementById('prevButton').disabled = offset === 0;
        document.getElementById('nextButton').disabled = !data.has_more;
        currentOffset = offset;
    })
    .catch(error => {
        console.error('Error:', error);
        if (!append) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center text-danger">
                        ${error.message || 'Error loading data'}
                    </td>
                </tr>
            `;
        }
    })
    .finally(() => {
        loading = false;
    });
}

// Event Listeners para la página de consulta
document.addEventListener('DOMContentLoaded', function() {
    const queryForm = document.getElementById('queryForm');
    if (queryForm) {
        queryForm.addEventListener('submit', function(e) {
            e.preventDefault();
            currentOffset = 0;
            loadCars(0);
        });

        const prevButton = document.getElementById('prevButton');
        if (prevButton) {
            prevButton.addEventListener('click', function() {
                if (currentOffset >= limit) {
                    loadCars(currentOffset - limit);
                }
            });
        }

        const nextButton = document.getElementById('nextButton');
        if (nextButton) {
            nextButton.addEventListener('click', function() {
                loadCars(currentOffset + limit);
            });
        }
    }
}); 