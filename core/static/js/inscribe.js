const keywords = {
  values: [],
};

// Function to handle keydown event
function handleAddKeyword(event) {
  // Check if the pressed key is Enter (key code 13)
  if (
    event.keyCode === 13 &&
    document.getElementById("keywordInput").value != ""
  ) {
    if (keywords.values.length >= 5) {
      const keywordMax5Only = document.getElementById("keywordMax5Only");
      keywordMax5Only.classList.remove("hidden");

      return false;
    } else {
      const keywordInput = document.getElementById("keywordInput");
      const inputValue = keywordInput.value;

      const keywordMin3Required = document.getElementById(
        "keywordMin3Required"
      );

      if (keywords.values.length >= 3) {
        keywordMin3Required.classList.add("hidden");
      } else {
      }

      if (keywords.values.length >= 5) {
        keywordMax5Only.classList.remove("hidden");
      } else {
        keywordMax5Only.classList.add("hidden");
      }

      // Get the input element and its value
      // const keywordInput = document.getElementById("keywordInput");
      // const inputValue = keywordInput.value;

      // Add the value to the JavaScript object
      keywords.values.push(inputValue);

      // Update the div with the list of values
      updateKeywordsContainer();

      // Clear the input field
      keywordInput.value = "";
    }
  }
}

function handleKeywordClick(index) {
  keywords.values.splice(index, 1);

  // Update the div with the updated list of values
  updateKeywordsContainer();
}

// Function to update the div with the list of values
function updateKeywordsContainer() {
  // Get the output div element
  const keywordsContainer = document.getElementById("keywordsContainer");

  // Clear the existing content
  keywordsContainer.innerHTML = "";

  // Loop through the values in the object and append them to the div
  keywords.values.forEach((value, index) => {
    const valueElement = document.createElement("div");
    valueElement.classList.add(
      "bg-gray-100",
      "font-bold",
      "text-gray-600",
      "px-3",
      "py-1",
      "cursor-pointer",
      "hover:bg-gray-100",
      "border"
    );
    valueElement.textContent = value;
    valueElement.addEventListener("click", () => handleKeywordClick(index));
    keywordsContainer.appendChild(valueElement);
  });
}

async function handleSaveAndContinue() {
  if (keywords.values.length > 2 && keywords.values.length <= 5) {
    console.log("saving...");
    // save here
    const csrfToken = document.getElementsByName("csrfmiddlewaretoken")[0]
      .value;
    const payload = {
      values: keywords.values,
      // add any other data you need to send
      csrfmiddlewaretoken: csrfToken,
    };

    fetch("", {
      method: "POST",
      mode: "cors", // no-cors, *cors, same-origin
      cache: "no-cache",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify(payload),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((responseData) => {
        // Handle the response data as needed
        console.log("Response:", responseData);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
  return false;
}

function validateCategoryAndSubmit() {
  const checkboxes = document.querySelectorAll(".categoryCheckbox");
  let atLeastOneChecked = false;

  checkboxes.forEach(checkbox => {
      if (checkbox.checked) {
          atLeastOneChecked = true;
      }
  });

  if (atLeastOneChecked) {
      document.getElementById('aeCategoryForm').submit();
  } else {
      alert('Please select at least one category.');
  }
}
