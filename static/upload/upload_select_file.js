/**
 * Function to simulate a click event on a file input element.
 * @param {string} elementId - The id of the file input element.
 */
function openFileInput(elementId) {
  document.getElementById(elementId).click();
}

/**
 * Function to handle the drop event for a file input element.
 * @param {Event} event - The drop event.
 * @param {string} elementId - The id of the file input element.
 */
function dropHandler(event, elementId) {
  event.preventDefault();
  if (event.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (event.dataTransfer.items[i].kind === "file") {
        const file = event.dataTransfer.items[i].getAsFile();
        console.log("File", file);
        // Display the file name
        displayFileName(file.name, elementId);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.files.length; i++) {
      console.log("File", event.dataTransfer.files[i]);
      // Display the file name
      displayFileName(event.dataTransfer.files[i].name, elementId);
    }
  }
}

/**
 * Function to handle the dragover event for a file input element.
 * @param {Event} event - The dragover event.
 * @param {string} elementId - The id of the file input element.
 */
function dragOverHandler(event, elementId) {
  event.preventDefault();
  // Set style for the drop zone to indicate valid drop target
  event.target.style.background = "#e9ecef";
  event.target.style.background = "#000000";
}

/**
 * Function to handle the file selection event for a file input element.
 * @param {string} name - The name of the file input element.
 * @param {string} elementId - The id of the file input element.
 */
function fileSelected(name, elementId ) {
  const fileInput = document.getElementById(name);
  const file = fileInput.files[0];
  console.log("File", file);
  // Display the file name
  displayFileName(file.name, elementId);
}

/**
 * Function to display the name of the selected file.
 * @param {string} fileName - The name of the selected file.
 * @param {string} elementId - The id of the element where the file name should be displayed.
 */
function displayFileName(fileName, elementId ) {
  document.getElementById(elementId).textContent =
    "Selected file: " + fileName;
}

/**
 * Function to set the selected option in a dropdown menu.
 * @param {string} option - The selected option.
 * @param {string} elementId - The id of the dropdown menu.
 */
function setSelectedOption(option, elementId) {
    document.getElementById(elementId).innerText = option;
}