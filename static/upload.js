function uploadFile(sourceElementId = "fileInput", targetElementId = "targetFileInput") {
  const source_fileInput = document.getElementById(sourceElementId);
  const source_file = source_fileInput.files[0];

  const target_fileInput = document.getElementById(targetElementId);
  const target_file = target_fileInput.files[0];

  console.log(source_file, target_file)
  const domain = document.getElementById('dropdownMenuButton').innerText;
  const language = getSelectedLanguage();

  if (source_file) {
    const formData = new FormData();

    formData.append("language", 'en')
    formData.append("domain", domain)

    formData.append("file", source_file);
    formData.append("target_file", target_file);

    showLoadingSpinner();

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("File uploaded successfully");
          return response.json();
          // Optionally, display a success message to the user
        } else {
          console.error("Failed to upload file");
          // Optionally, display an error message to the user
        }
      })
        // STĄD IDZIE DO PYTHONA, JEST PRZETWARZANE I WRACA Z POWROTEM
        .then((resp) => {
      const source_terms = resp['source_terms'];
      const target_terms = resp['target_terms'];
      const alignments = resp['alignment'];

      // const target_content = resp.target_content;
      console.log( source_terms, target_terms, alignments)

      let text = "";
      for (let i = 0; i < source_terms.length; i++) {
        text += source_terms[i] + "<br>";
      }

      let text2 = "";
      for (let i = 0; i < target_terms.length; i++) {
        text2 += target_terms[i] + "<br>";
      }

      text = "";
      text2 = "";
      let text3 = "";
      for (let i = 0; i < alignments.length; i++) {
        text += alignments[i][0] + "<br>";
        text2 += alignments[i][1] + "<br>";
        text3 += alignments[i][0] + "     " + alignments[i][1] + "<br>";
      }

      document.getElementById('added_content').innerHTML = text
      document.getElementById('added_content_2').innerHTML = text2

      document.getElementById('alignment_content').innerHTML = text3

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
