function uploadFile(sourceElementId = "fileInput", targetElementId = "targetFileInput") {
  const source_fileInput = document.getElementById(sourceElementId);
  const source_file = source_fileInput.files[0];

  const target_fileInput = document.getElementById(targetElementId);
  const target_file = target_fileInput.files[0];

  console.log(source_file, target_file)
  const domain = document.getElementById('dropdownMenuButton').innerText;
  const language = getSelectedLanguage();

   if (domain === "Choose glossary") {
        alert("Please choose a glossary before proceeding.");
        return;
    }

  if (source_file) {
    const formData = new FormData();

    formData.append("language", 'english')
    formData.append("domain", domain)

    formData.append("file", source_file);
    formData.append("target_file", target_file);

    showLoadingSpinner();

  fetch("/upload", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(resp => {
            const alignments = resp['alignment'];
            const categories = resp['categories'];

            const tableBody = document.getElementById('translationsTableBody');
            tableBody.innerHTML = ''; // Clear existing rows

         for (let i = 0; i < alignments.length; i++) {
                const row = document.createElement('tr');
                if (language === 'spanish') {
                    row.innerHTML = `
                        <td>${alignments[i][0]}</td>
                        <td>${alignments[i][1]}</td>
                        <td></td>
                        <td class="categories-column" title="${categories}">${categories}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="editRow(this)">Edit</button>
                            <button class="btn btn-danger" onclick="deleteRow(this)">Delete</button>
                        </td>
                    `;
                } else if (language === 'polish') {
                    row.innerHTML = `
                        <td>${alignments[i][0]}</td>
                        <td></td>
                        <td>${alignments[i][1]}</td>
                        <td class="categories-column" title="${categories}">${categories}</td>
                        <td>
                            <button class="btn btn-secondary" onclick="editRow(this)">Edit</button>
                            <button class="btn btn-danger" onclick="deleteRow(this)">Delete</button>
                        </td>
                    `;
                }
                tableBody.appendChild(row);
            }
        })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, display an error message to the user
      })
      .finally(() => {
        hideLoadingSpinner();
      });
  }
}

function showLoadingSpinner() {
  document.getElementById('loading-spinner').style.display = 'block';
}

function hideLoadingSpinner() {
  document.getElementById('loading-spinner').style.display = 'none';
}

function getSelectedLanguage() {
  const dropdown = document.getElementById('languageDropdown');
  return dropdown.value;
}

document.addEventListener('DOMContentLoaded', (event) => {
    fetch('/tables')
        .then(response => response.json())
        .then(data => {
            const dropdownMenu = document.querySelector('.dropdown-menu');

            data.forEach(table => {
                const option = document.createElement('a');
                option.className = 'dropdown-item';
                option.href = '#';
                option.innerText = table;
                option.onclick = () => setSelectedOption(table, 'dropdownMenuButton');
                dropdownMenu.appendChild(option); // Append to dropdown menu
            });
        })
        .catch(error => console.error('Error fetching table names:', error));
});

function setSelectedOption(option, elementId) {
    document.getElementById(elementId).innerText = option;
}

function editRow(button) {
    const row = button.closest('tr');
    const isEditing = button.textContent === 'Confirm';

    if (isEditing) {
        // Save values and switch to non-editable mode
        const inputs = row.querySelectorAll('input');
        inputs.forEach(input => {
            const cell = input.closest('td');
            cell.textContent = input.value;
        });
        button.textContent = 'Edit';
        button.classList.remove('btn-success');
        button.classList.add('btn-secondary');
    } else {
        // Switch to editable mode
        const cells = row.querySelectorAll('td:not(:last-child)');
        cells.forEach(cell => {
            const input = document.createElement('input');
            input.type = 'text';
            input.value = cell.textContent;
            input.classList.add('form-control');
            cell.textContent = '';
            cell.appendChild(input);
        });
        button.textContent = 'Confirm';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-success');
    }
}

function deleteRow(button) {
    const row = button.closest('tr');
    row.remove();
}


document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.querySelector('button[onclick="uploadFile()"]');
    if (uploadButton) {
        uploadButton.textContent = 'Get terms';
    }
});