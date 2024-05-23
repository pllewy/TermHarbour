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
      });
  }
}
