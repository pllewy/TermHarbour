/**
 * This script handles the functionality of uploading and translating text.
 * It includes a function for uploading and translating text.
 */

/**
 * Function to upload a file and translate its content.
 * @param {string} sourceElementId - The id of the HTML element containing the source file input. Default is "fileInput".
 * @param {string} targetElementId - The id of the HTML element containing the target file input. Default is "targetFileInput".
 */
function uploadFile(sourceElementId = "fileInput", targetElementId = "targetFileInput") {
  // Get the source and target file inputs
  const source_fileInput = document.getElementById(sourceElementId);
  const source_file = source_fileInput.files[0];

  const target_fileInput = document.getElementById(targetElementId);
  const target_file = target_fileInput.files[0];

  if (!source_file || !target_file) {
        alert("Please select both source and target files.");
        return;
    }

  // Log the source and target files
  console.log(source_file, target_file)

  // Get the domain and language from the HTML elements
  const domain = document.getElementById('dropdownMenuButton').innerText;
  const language = getSelectedLanguage();

  // If no domain is selected, alert the user and return
  if (domain === "Choose glossary") {
        alert("Please choose a glossary before proceeding.");
        return;
    }

  // If there is a source file, proceed with the upload and translation
  if (source_file) {
    // Create a new FormData object
    const formData = new FormData();

    // Append the language, domain, source file, and target file to the FormData object
    formData.append("language", language)
    formData.append("domain", domain)
    formData.append("file", source_file);
    formData.append("target_file", target_file);

    // Show the loading spinner
    showLoadingSpinner();

    // Send a POST request to the server with the FormData object
    fetch("/upload", {
            method: "POST",
            body: formData,
        })
        .then(response => response.json())
        .then(resp => {
            // Get the alignments and categories from the response
            const alignments = resp['alignment'];
            const categories = resp['categories'];

            // Get the table body
            const tableBody = document.getElementById('translationsTableBody');
            tableBody.innerHTML = ''; // Clear existing rows

            // For each alignment, create a new row and append it to the table body
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
            document.getElementById('addToGlossaryButton').style.display = 'block';
        })
      .catch((error) => {
        // Log any errors
        console.error("Error:", error);
        // Optionally, display an error message to the user
      })
      .finally(() => {
        // Hide the loading spinner
        hideLoadingSpinner();
      });
  }
}

/**
 * Function to show the loading spinner.
 */
function showLoadingSpinner() {
  document.getElementById('loading-spinner').style.display = 'block';
}

/**
 * Function to hide the loading spinner.
 */
function hideLoadingSpinner() {
  document.getElementById('loading-spinner').style.display = 'none';
}

/**
 * Function to get the selected language from the dropdown.
 * @returns {string} The selected language.
 */
function getSelectedLanguage() {
  const dropdown = document.getElementById('languageDropdown');
  return dropdown.value;
}

/**
 * Event listener for DOMContentLoaded event.
 * Fetches the table names from the server and appends them to the dropdown menu.
 */
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

/**
 * Function to set the selected option in the dropdown menu.
 * @param {string} option - The selected option.
 * @param {string} elementId - The id of the dropdown menu.
 */
function setSelectedOption(option, elementId) {
    document.getElementById(elementId).innerText = option;
}

/**
 * Function to switch a row to editable mode or save the edited values.
 * @param {HTMLElement} button - The button that was clicked.
 */
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

/**
 * Function to delete a row from the table.
 * @param {HTMLElement} button - The button that was clicked.
 */
function deleteRow(button) {
    const row = button.closest('tr');
    if (confirm(`Are you sure you want to delete the term ${row.cells[0].innerText}?`)) {
        row.remove();
    }
}

/**
 * Event listener for DOMContentLoaded event.
 * Changes the text of the upload button to 'Get terms'.
 */
document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.querySelector('button[onclick="uploadFile()"]');
    if (uploadButton) {
        uploadButton.textContent = 'Get terms';
    }
});

/**
 * Function to add the terms to the glossary.
 */
function addToGlossary() {
  // Get the table rows
  const rows = document.querySelectorAll('#translationsTableBody tr');

  // Get the chosen glossary from the dropdown
  const category = document.getElementById('dropdownMenuButton').innerText;

  // Check if a glossary is chosen
  if (category === "Choose glossary") {
    alert("Please choose a glossary before proceeding.");
    return;
  }

  // Create an array to hold the translations
  const translations = [];

  // Iterate through the rows to get the translations
  rows.forEach(row => {
    const english = row.cells[0].innerText;
    const spanish = row.cells[1].innerText;
    const polish = row.cells[2].innerText;
    const categories = row.cells[3].innerText;

    translations.push({english, spanish, polish, categories});
  });

  // Send the translations to the server
  fetch('/add_to_glossary', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({category, translations}),
  })
  .then(response => response.json())
  .then(data => {
    alert(data.message);
    location.reload(); // Reset the page
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}