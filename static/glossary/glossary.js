/**
 * This script handles the functionality of a glossary page.
 * It includes event listeners for DOMContentLoaded, click and submit events.
 * It also includes functions for sorting, searching, adding, editing, and deleting glossary records.
 */

document.addEventListener('DOMContentLoaded', function () {
    // Event listener for delete button
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            // Fetches the English term and current table from the dataset
            const english = this.dataset.english;
            const table = document.getElementById('currentTable').value;

            // Show confirmation dialog
            if (confirm(`Are you sure you want to delete the term "${english}"?`)) {
                // Sends a POST request to delete the term
                fetch(`/delete/${english}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `table=${table}`
                })
                    .then(response => response.json())
                    .then(data => {
                        // If the deletion was successful, reloads the page
                        // Otherwise, alerts the user of an error
                        if (data.result === 'success') {
                            window.location.reload();
                        } else {
                            alert('Error deleting record');
                        }
                    });
            }
        });
    });

    // Event listener for edit button
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function () {
            // Fetches the English term and row from the dataset
            const english = this.dataset.english;
            const row = this.closest('tr');

            // Fetches the Spanish, Polish, and categories terms from the row
            const spanish = row.children[1].innerText;
            const polish = row.children[2].innerText;
            const categories = row.children[3].innerText;

            // If the button text is 'Edit', changes the row to input fields
            // Otherwise, sends a POST request to edit the term
            if (this.innerText === 'Edit') {
                row.children[0].innerHTML = `<input type="text" class="form-control" value="${english}">`;
                row.children[1].innerHTML = `<input type="text" class="form-control" value="${spanish}">`;
                row.children[2].innerHTML = `<input type="text" class="form-control" value="${polish}">`;
                row.children[3].innerHTML = `<input type="text" class="form-control" value="${categories}">`;
                this.innerText = 'Confirm';
                this.classList.remove('btn-secondary');
                this.classList.add('btn-success');
            } else {
                const newEnglish = row.children[0].children[0].value;
                const newSpanish = row.children[1].children[0].value;
                const newPolish = row.children[2].children[0].value;
                const newCategory = row.children[3].children[0].value;
                const table = document.getElementById('currentTable').value;

                fetch(`/edit/${english}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `table=${table}&new_english=${newEnglish}&spanish=${newSpanish}&polish=${newPolish}&categories=${newCategory}`
                })
                .then(response => response.json())
                .then(data => {
                    // If the edit was successful, updates the row and reloads the page
                    // Otherwise, alerts the user of an error
                    if (data.result === 'success') {
                        row.children[0].innerText = newEnglish;
                        row.children[1].innerText = newSpanish;
                        row.children[2].innerText = newPolish;
                        row.children[3].innerText = newCategory;
                        this.innerText = 'Edit';
                        this.classList.remove('btn-success');
                        this.classList.add('btn-secondary');
                        window.location.reload();
                    } else if (data.result === 'error') {
                        alert(data.message);
                    }
                });
            }
        });
    });

    // Event listener for add record button
    document.getElementById('addRecordButton').addEventListener('click', function () {
        // Displays the add/edit form
        document.getElementById('addEditForm').style.display = 'block';
    });

    // Event listener for cancel button
    document.getElementById('cancelButton').addEventListener('click', function () {
        // Hides the add/edit form and resets it
        document.getElementById('addEditForm').style.display = 'none';
        document.getElementById('addEditForm').reset();
    });

    // Event listener for add/edit form submit
    document.getElementById('addEditForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const form = e.target;
        const table = document.getElementById('currentTable').value;
        const english = document.getElementById('english').value;
        const spanish = document.getElementById('spanish').value;
        const polish = document.getElementById('polish').value;
        const categories = document.getElementById('categories').value;

        // Sends a POST request to add/edit the term
        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `table=${table}&english=${english}&spanish=${spanish}&polish=${polish}&categories=${categories}`
        })
        .then(response => response.json())
        .then(data => {
            // If the add/edit was successful, reloads the page
            // Otherwise, displays an error message
            if (data.result === 'success') {
                window.location.reload();
            } else if (data.result === 'error') {
                document.getElementById('errorMessage').innerText = data.message;
                document.getElementById('errorMessage').style.display = 'block';
            }
        });
    });

    // Event listener for sort button
    document.querySelectorAll('.sort-btn').forEach(button => {
        button.addEventListener('click', function () {
            // Fetches the column and order from the dataset
            const column = this.dataset.column;
            const order = this.dataset.order;

            // Fetches the table and rows
            const table = document.getElementById('glossaryTableBody');
            const rows = Array.from(table.querySelectorAll('tr'));

            // Sorts the rows based on the column and order
            const sortedRows = rows.sort((a, b) => {
                const aText = a.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.toLowerCase();
                const bText = b.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.toLowerCase();
                if (order === 'asc') {
                    return aText.localeCompare(bText);
                } else {
                    return bText.localeCompare(aText);
                }
            });

            // Removes all rows from the table
            while (table.firstChild) {
                table.removeChild(table.firstChild);
            }

            // Appends the sorted rows to the table
            sortedRows.forEach(row => table.appendChild(row));

            // Toggles the order for the next sort
            this.dataset.order = order === 'asc' ? 'desc' : 'asc';
        });
    });

    // Event listener for search button
    document.querySelectorAll('.search-btn').forEach(button => {
        button.addEventListener('click', function () {
            // Fetches the column from the dataset
            const column = this.dataset.column;

            // Displays the search input for the column and hides the others
            document.querySelectorAll('.search-input').forEach(input => {
                input.style.display = input.dataset.column === column ? 'block' : 'none';
            });
        });
    });

    // Event listener for search input
    document.querySelectorAll('.search-input').forEach(input => {
        input.addEventListener('input', function () {
            // Fetches the column and query from the dataset
            const column = this.dataset.column;
            const query = this.value.toLowerCase();

            // Fetches the table and rows
            const table = document.getElementById('glossaryTableBody');
            const rows = table.querySelectorAll('tr');

            // Displays rows that match the query and hides the others
            rows.forEach(row => {
                const cellText = row.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.toLowerCase();
                if (cellText.includes(query)) {
                    row.style.display = '';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    });

    // Function to get the column index based on the column name
    function getColumnIndex(column) {
        switch (column) {
            case 'english': return 1;
            case 'spanish': return 2;
            case 'polish': return 3;
            case 'categories': return 4;
            default: return 1;
        }
    }
});