

function uploadTranslate(sourceElementId = "source_text", targetElementId = "target_text") {
  const source_file = document.getElementById(sourceElementId).innerText;

  const target_file = document.getElementById(targetElementId).innerText;

  console.log(source_file, target_file)
  // const domain = document.getElementById('dropdownMenuButton').innerText;
  const source_language = document.getElementById('source_language').value;
    const target_language = document.getElementById('target_language').value;

  if (source_file) {
    const formData = new FormData();
    formData.append("source_language", source_language)
    formData.append("source_text", source_file)

    formData.append("target_language", target_language);
    formData.append("target_text", target_file);

    fetch("/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        if (response.ok) {
          console.log("Translate uploaded successfully");
          return response.json();
          // Optionally, display a success message to the user
        } else {
          console.error("Failed to upload translate");
          // Optionally, display an error message to the user
        }
      })
        // STĄD IDZIE DO PYTHONA, JEST PRZETWARZANE I WRACA Z POWROTEM
        .then((resp) => {
      const source_terms = resp['source_text'];
      const target_terms = resp['target_text'];
      // const alignments = resp['alignment'];

      // const target_content = resp.target_content;
      console.log( source_terms, target_terms)

      let text = "";
      for (let i = 0; i < source_terms.length; i++) {
          text += source_terms[i] + " ";
      }

      let text2 = "";
      for (let i = 0; i < target_terms.length; i++) {
        text2 += target_terms[i] + " ";
      }

      document.getElementById('source_text').innerHTML = text
      document.getElementById('target_text').innerHTML = text2

      // document.getElementById('alignment_content').innerHTML = text3
    })
      .catch((error) => {
        console.error("Error:", error);
        // Optionally, display an error message to the user
      });
  }
}
