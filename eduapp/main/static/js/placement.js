function showDescription(id) {
    const desc = document.getElementById(id);
    if (desc.style.display === "none" || desc.style.display === "") {
        desc.style.display = "block";
    } else {
        desc.style.display = "none";
    }
}

async function downloadApplicationForm() {
    const { jsPDF } = window.jspdf;

    const formData = {
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        contactno: document.getElementById('contactno').value,
        linkedinlink: document.getElementById('linkedinlink').value,
        gender: document.getElementById('gender').value,
        address: document.getElementById('address').value,
        state: document.getElementById('state').value,
        citizenship: document.getElementById('citizenship').value,
        dob: document.getElementById('dob').value,
        experience: document.getElementById('experience').value,
        currentctc: document.getElementById('currentctc').value,
        expectedctc: document.getElementById('expectedctc').value,
        consent: document.getElementById('consent').checked,
        resume: document.getElementById('resume').value
    };

    // Check if any field is empty
    for (let key in formData) {
        if (formData.hasOwnProperty(key) && !formData[key]) {
            alert("Please fill all the fields.");
            return;
        }
    }

    if (!formData.consent) {
        alert("Please agree to the terms and conditions.");
        return;
    }

    const registrationId = Math.random().toString(36).substring(2, 15);

    const doc = new jsPDF();

    doc.text(`Registration ID: ${registrationId}`, 10, 10);
    doc.text(`Full Name: ${formData.name}`, 10, 20);
    doc.text(`Email: ${formData.email}`, 10, 30);
    doc.text(`Contact Number: ${formData.contactno}`, 10, 40);
    doc.text(`LinkedIn Profile: ${formData.linkedinlink}`, 10, 50);
    doc.text(`Gender: ${formData.gender}`, 10, 60);
    doc.text(`Communication Address: ${formData.address}`, 10, 70);
    doc.text(`State: ${formData.state}`, 10, 80);
    doc.text(`Citizenship: ${formData.citizenship}`, 10, 90);
    doc.text(`Date of Birth: ${formData.dob}`, 10, 100);
    doc.text(`Years of Experience: ${formData.experience}`, 10, 110);
    doc.text(`Current CTC: ${formData.currentctc}`, 10, 120);
    doc.text(`Expected CTC: ${formData.expectedctc}`, 10, 130);
    doc.text(`Resume: ${formData.resume}`, 10, 140);

    doc.save(`Application_${registrationId}.pdf`);

    // Clear the form fields after PDF is downloaded
    document.getElementById('registrationForm').reset();
}
