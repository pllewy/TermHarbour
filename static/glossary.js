document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.dataset.id;
            const table = document.getElementById('currentTable').value;
            fetch(`/delete/${id}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded'
                },
                body: `table=${table}`
            })
            .then(response => response.json())
            .then(data => {
                if (data.result === 'success') {
                    window.location.reload();
                } else {
                    alert('Error deleting record');
                }
            });
        });
    });

    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function () {
            const id = this.dataset.id;
            const row = this.closest('tr');
            const english = row.children[0].innerText;
            const spanish = row.children[1].innerText;
            const polish = row.children[2].innerText;

            if (this.innerText === 'Edit') {
                row.children[0].innerHTML = `<input type="text" class="form-control" value="${english}">`;
                row.children[1].innerHTML = `<input type="text" class="form-control" value="${spanish}">`;
                row.children[2].innerHTML = `<input type="text" class="form-control" value="${polish}">`;
                this.innerText = 'Confirm';
                this.classList.remove('btn-secondary');
                this.classList.add('btn-success');
            } else {
                const newEnglish = row.children[0].children[0].value;
                const newSpanish = row.children[1].children[0].value;
                const newPolish = row.children[2].children[0].value;
                const table = document.getElementById('currentTable').value;

                fetch(`/edit/${id}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: `table=${table}&english=${newEnglish}&spanish=${newSpanish}&polish=${newPolish}`
                })
                .then(response => {
                    if (response.ok) {
                        row.children[0].innerText = newEnglish;
                        row.children[1].innerText = newSpanish;
                        row.children[2].innerText = newPolish;
                        this.innerText = 'Edit';
                        this.classList.remove('btn-success');
                        this.classList.add('btn-secondary');
                        window.location.reload();
                    } else {
                        alert('Error updating record');
                    }
                });
            }
        });
    });

    document.getElementById('addRecordButton').addEventListener('click', function () {
        document.getElementById('addEditForm').style.display = 'block';
    });

    document.getElementById('cancelButton').addEventListener('click', function () {
        document.getElementById('addEditForm').style.display = 'none';
        document.getElementById('addEditForm').reset();
    });

    document.getElementById('addEditForm').addEventListener('submit', function (e) {
        e.preventDefault();
        const form = e.target;
        const table = document.getElementById('currentTable').value;
        const english = document.getElementById('english').value;
        const spanish = document.getElementById('spanish').value;
        const polish = document.getElementById('polish').value;

        fetch(form.action, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `table=${table}&english=${english}&spanish=${spanish}&polish=${polish}`
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                alert('Error adding record');
            }
        });
    });

    document.querySelectorAll('.sort-btn').forEach(button => {
        button.addEventListener('click', function () {
            const column = this.dataset.column;
            const order = this.dataset.order;
            const table = document.getElementById('glossaryTableBody');
            const rows = Array.from(table.querySelectorAll('tr'));
            const sortedRows = rows.sort((a, b) => {
                const aText = a.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.toLowerCase();
                const bText = b.querySelector(`td:nth-child(${getColumnIndex(column)})`).innerText.toLowerCase();
                if (order === 'asc') {
                    return aText.localeCompare(bText);
                } else {
                    return bText.localeCompare(aText);
                }
            });
            while (table.firstChild) {
                table.removeChild(table.firstChild);
            }
            sortedRows.forEach(row => table.appendChild(row));
            this.dataset.order = order === 'asc' ? 'desc' : 'asc';
        });
    });

    document.querySelectorAll('.search-btn').forEach(button => {
        button.addEventListener('click', function () {
            const column = this.dataset.column;
            document.querySelectorAll('.search-input').forEach(input => {
                input.style.display = input.dataset.column === column ? 'block' : 'none';
            });
        });
    });

    document.querySelectorAll('.search-input').forEach(input => {
        input.addEventListener('input', function () {
            const column = this.dataset.column;
            const query = this.value.toLowerCase();
            const table = document.getElementById('glossaryTableBody');
            const rows = table.querySelectorAll('tr');
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

    function getColumnIndex(column) {
        switch (column) {
            case 'english': return 1;
            case 'spanish': return 2;
            case 'polish': return 3;
            default: return 1;
        }
    }
});
