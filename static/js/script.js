document.getElementById('imageForm').addEventListener('submit', function(e) {
    e.preventDefault();
    var submitBtn = document.getElementById("submitBtn");
    var previousValue = submitBtn.value;

    submitBtn.disabled = true;
    submitBtn.value = "Ładowanie...";

    var formData = new FormData(this);
    formData.append('mode', document.getElementById('mode').value);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let descriptionText = document.getElementById('descriptionText');
        descriptionText.innerText = data.description;

        let descriptionDiv = document.querySelector('.description');
        descriptionDiv.style.display = 'block';
        submitBtn.disabled = false;
        submitBtn.value = previousValue;
    })
    .catch(error => console.error('Error:', error));
});

function previewImage() {
    var oFReader = new FileReader();
    oFReader.readAsDataURL(document.getElementById("image").files[0]);

    oFReader.onload = function (oFREvent) {
        document.getElementById("imageDisplay").style.display = "block";
        document.getElementById("imageDisplay").src = oFREvent.target.result;
    };
}
function updateMode() {
    var switchValue = document.getElementById("switch").value;
    document.getElementById("mode").value = switchValue;

    var submitBtn = document.getElementById("submitBtn");
    var descriptionHeader = document.getElementById("descriptionHeader")
    if (switchValue === "description") {
        submitBtn.value = "Generuj Opis";
        descriptionHeader.textContent = "Opis Obrazu:"
    } else if (switchValue === "caption") {
        submitBtn.value = "Generuj Podpis";
        descriptionHeader.textContent = "Podpis Obrazu:"
    }
}