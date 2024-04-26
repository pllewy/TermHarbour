function openFileInput() {
  document.getElementById("fileInput").click();
}

function uploadFile() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  if (file) {
    const formData = new FormData();
    formData.append("file", file);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("File uploaded successfully");
          // Optionally, display a success message to the user
        } else {
          console.error("Failed to upload file");
          // Optionally, display an error message to the user
        }
      })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, display an error message to the user
      });
  }
}

function dropHandler(event) {
  event.preventDefault();
  if (event.dataTransfer.items) {
    // Use DataTransferItemList interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.items.length; i++) {
      // If dropped items aren't files, reject them
      if (event.dataTransfer.items[i].kind === "file") {
        const file = event.dataTransfer.items[i].getAsFile();
        console.log("File", file);
        // Handle file upload here
        displayFileName(file.name);
      }
    }
  } else {
    // Use DataTransfer interface to access the file(s)
    for (let i = 0; i < event.dataTransfer.files.length; i++) {
      console.log("File", event.dataTransfer.files[i]);
      // Handle file upload here
      displayFileName(event.dataTransfer.files[i].name);
    }
  }
}

function dragOverHandler(event) {
  event.preventDefault();
  // Set style for the drop zone to indicate valid drop target
  event.target.style.background = "#e9ecef";
  event.target.style.background = "#000000";
}

function fileSelected() {
  const fileInput = document.getElementById("fileInput");
  const file = fileInput.files[0];
  console.log("File", file);
  // Handle file upload here
  displayFileName(file.name);
}

function displayFileName(fileName) {
  document.getElementById("file-name").textContent =
    "Selected file: " + fileName;
}
