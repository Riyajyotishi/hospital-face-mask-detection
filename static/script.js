// Access camera
const video = document.getElementById('video');

navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing the camera: ", err);
    });

// Capture image and send to backend for mask detection
document.getElementById('capture').addEventListener('click', async () => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    const imageData = canvas.toDataURL('image/jpeg'); // Get the captured image as a base64 string

    // Send the captured image to the Flask backend for mask detection
    const response = await fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ image: imageData }) // Send base64 image data to Flask
    });

    // Handle the response from Flask backend
    const data = await response.json();

    // Get the result div to display the outcome
    const resultDiv = document.getElementById('result');

    if (data.label === 'Mask') {
        resultDiv.innerHTML = "✅ Access Granted - Mask Detected";
        resultDiv.style.color = "green";
    } else {
        resultDiv.innerHTML = "❌ Access Denied - No Mask Detected";
        resultDiv.style.color = "red";
    }
});
