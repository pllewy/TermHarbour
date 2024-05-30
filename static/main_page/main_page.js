/**
 * This script handles the functionality of uploading and translating text.
 * It includes a function for uploading and translating text.
 */

/**
 * Function to upload and translate text.
 * @param {string} sourceElementId - The id of the HTML element containing the source text. Default is "source_text".
 * @param {string} targetElementId - The id of the HTML element containing the target text. Default is "target_text".
 */
function uploadTranslate(sourceElementId = "source_text", targetElementId = "target_text") {
  // Get the source and target text from the HTML elements
  const source_file = document.getElementById(sourceElementId).innerText;
  const target_file = document.getElementById(targetElementId).innerText;

  // Log the source and target text
  console.log(source_file, target_file)

  // Get the source and target language from the HTML elements
  const source_language = document.getElementById('source_language').value;
  const target_language = document.getElementById('target_language').value;

  // If there is source text, proceed with the upload and translation
  if (source_file) {
    // Create a new FormData object
    const formData = new FormData();

    // Append the source language, source text, target language, and target text to the FormData object
    formData.append("source_language", source_language)
    formData.append("source_text", source_file)
    formData.append("target_language", target_language);
    formData.append("target_text", target_file);

    // Send a POST request to the server with the FormData object
    fetch("/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        // If the response is ok, log a success message and return the response as JSON
        // Otherwise, log an error message
        if (response.ok) {
          console.log("Translate uploaded successfully");
          return response.json();
        } else {
          console.error("Failed to upload translate");
        }
      })
      // Handle the JSON response
      .then((resp) => {
        // Get the source and target terms from the response
        const source_terms = resp['source_text'];
        const target_terms = resp['target_text'];

        // Log the source and target terms
        console.log( source_terms, target_terms)

        // Create a string of the source terms
        let text = "";
        for (let i = 0; i < source_terms.length; i++) {
            text += source_terms[i] + " ";
        }

        // Create a string of the target terms
        let text2 = "";
        for (let i = 0; i < target_terms.length; i++) {
          text2 += target_terms[i] + " ";
        }

        // Update the HTML elements with the source and target terms
        document.getElementById('source_text').innerHTML = text
        document.getElementById('target_text').innerHTML = text2
      })
      // Log any errors
      .catch((error) => {
        console.error("Error:", error);
      });
  }
}