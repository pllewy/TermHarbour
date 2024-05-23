function uploadFile(sourceElementId = "fileInput", targetElementId = "targetFileInput") {
  const source_fileInput = document.getElementById(sourceElementId);
  const source_file = source_fileInput.files[0];

  const target_fileInput = document.getElementById(targetElementId);
  const target_file = target_fileInput.files[0];

  console.log(source_file, target_file)
  const domain = document.getElementById('dropdownMenuButton').innerText;
  const language = 'en'

  if (source_file) {
    const formData = new FormData();

    formData.append("language", language)
    formData.append("domain", domain)

    formData.append("file", source_file);
    formData.append("target_file", target_file);

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
      }).then((resp) => {
      // resp.target_content = undefined;
      const source_terms = resp['source_terms'];
      const target_terms = resp['target_terms']
      // const target_content = resp.target_content;
      console.log( source_terms, target_terms)

      let text = "";
      for (let i = 0; i < source_terms.length; i++) {
        text += source_terms[i] + "<br>";
      }
      document.getElementById('added_content').innerHTML = text

      let text2 = "";
      for (let i = 0; i < target_terms.length; i++) {
        text2 += target_terms[i] + "<br>";
      }
      document.getElementById('added_content_2').innerHTML = text2

    })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, display an error message to the user
      });
  }
}
