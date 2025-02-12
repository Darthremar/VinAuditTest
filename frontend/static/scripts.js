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
        fetch(`/query?offset=${offset}`, {
            method: 'POST',
            body: new URLSearchParams(new FormData(document.getElementById('queryForm')))
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