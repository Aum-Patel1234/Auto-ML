let file_id = null;

function showTick(selected) {
  const classificationRadioTick = document.getElementById(
    "classification-tick"
  );
  const regressionRadioTick = document.getElementById("regression-tick");

  classificationRadioTick.classList.add("hidden");
  regressionRadioTick.classList.add("hidden");

  if (selected === "classification") {
    classificationRadioTick.classList.remove("hidden");
  } else {
    regressionRadioTick.classList.remove("hidden");
  }
}

document.getElementById("file").addEventListener("change", async (event) => {
  event.preventDefault();

  const fileInput = document.getElementById("file");
  const form = document.getElementById("myForm");
  const formData = new FormData(form);
  const file = formData.get("dataset");

  if (!file || file.name == "") {
    alert("Please provide the dataset.");
    return;
  }

  const allowedExtensions = ["csv", "xlsx", "xls"];
  const fileExtension = file.name.split(".").pop().toLowerCase();
  if (!allowedExtensions.includes(fileExtension)) {
    alert(
      `Invalid file type. Only ${allowedExtensions.join(
        ", "
      )} files are allowed.`
    );

    // Clear the file input field
    fileInput.value = "";
    return;
  }

  try {
    const response = await fetch(window.location.href, {
      method: "POST",
      body: formData,
      headers: {
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"), // Add CSRF token if using Django
      },
    });

    if (response.ok) {
      const res = await response.json();
      file_id = `${res["file_id"]}_${file.name}`; // set file id to send it to backend during sumbit
      const data = JSON.parse(res["data"]);

      if (data.length > 0) {
        const customDropdown = document.getElementById("feature_selection");
        customDropdown.innerHTML = null;

        const label = document.createElement("label");
        label.textContent =
          "Choose a Feature: (If the feature is not valid then last col will be assumed the target variable)";
        label.setAttribute("for", "dropdown-input");
        label.className = "w-full text-gray-700 font-semibold mb-4";

        const redTick = document.createElement("span");
        redTick.className = "text-red-500";
        redTick.textContent = "*";
        label.appendChild(redTick);

        customDropdown.appendChild(label);

        const inputElement = document.createElement("input");
        const dataList = document.createElement("datalist");
        dataList.id = "dropdown-options";

        data.forEach((element) => {
          const option = document.createElement("option");
          option.value = element; // Value for the datalist option
          dataList.appendChild(option);
        });

        inputElement.setAttribute("list", "dropdown-options");
        inputElement.setAttribute("placeholder", "Select or type an option...");
        inputElement.setAttribute("aria-label", "Feature Selection");
        inputElement.setAttribute("required", "");
        inputElement.className =
          "w-full p-3 text-sm border rounded-lg shadow-sm focus:ring-2 focus:ring-blue-500 focus:outline-none";

        customDropdown.appendChild(inputElement);
        customDropdown.appendChild(dataList);
      } else {
        console.log("No data available.");
      }
    } else if (response.status === 400) {
      // Handle 400 Bad Request
      alert("Invalid file uploaded. Please upload a valid dataset file.");
    } else {
      console.log("Error in the response!");
    }
  } catch (error) {
    console.error("An error occurred while processing the file:", error);
    alert("An error occurred. Please try again.");
  }
});

document.getElementById("myForm").addEventListener("submit", function (event) {
  if (file_id) {
    let hiddenInput = document.querySelector('input[name="file_id"]');
    if (!hiddenInput) {
      hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "file_id";
      this.appendChild(hiddenInput);
    }
    hiddenInput.value = file_id; // here is the value assigned to it
  } else {
    event.preventDefault();
    alert("Please upload a file first!");
  }
  showAlert('We are analyzing the dataset it may take some time if data is huge...');
});
function showAlert(message, duration = 10000) {      // 10s
  const alertBox = document.getElementById("customAlert");
  alertBox.textContent = message; // Set alert message
  alertBox.classList.remove("hide"); // Show alert

  setTimeout(() => {
    alertBox.classList.add("hide"); // Hide alert with animation
  }, duration);
}