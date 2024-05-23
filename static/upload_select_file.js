function openFileInput(elementId) {
  document.getElementById(elementId).click();
}


function dropHandler(event, elementId) {
  event.preventDefault();
  if (event.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (event.dataTransfer.items[i].kind === "file") {
        const file = event.dataTransfer.items[i].getAsFile();
        console.log("File", file);
        // Handle file upload here
        displayFileName(file.name, elementId);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.files.length; i++) {
      console.log("File", event.dataTransfer.files[i]);
      // Handle file upload here
      displayFileName(event.dataTransfer.files[i].name, elementId);
    }
  }
}

function dragOverHandler(event, elementId) {
  event.preventDefault();
  // Set style for the drop zone to indicate valid drop target
  event.target.style.background = "#e9ecef";
  event.target.style.background = "#000000";
}

function fileSelected(name, elementId ) {
  const fileInput = document.getElementById(name);
  const file = fileInput.files[0];
  console.log("File", file);
  // Handle file upload here
  displayFileName(file.name, elementId);
}

function displayFileName(fileName, elementId ) {
  document.getElementById(elementId).textContent =
    "Selected file: " + fileName;
}

function setSelectedOption(option, elementId) {
    document.getElementById(elementId).innerText = option;
}