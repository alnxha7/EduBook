

document.addEventListener("DOMContentLoaded", () => {
    const micButton = document.getElementById("mic-button");
    const cameraButton = document.getElementById("camera-button");
    const endCallButton = document.getElementById("end-call-button");
    const shareScreenButton = document.getElementById("share-screen-button");
    const notesButton = document.getElementById("notes-button");
    const notesArea = document.getElementById("notes-area");
    const sendNotesButton = document.getElementById("send-notes-button");
    const notesInput = document.getElementById("notes-input");
    const chatDisplay = document.getElementById("chat-display");
    const liveVideo = document.getElementById("live-video");

    let stream;

    micButton.addEventListener("click", () => {
        micButton.classList.toggle("active");
        micButton.textContent = micButton.classList.contains("active") ? "Mic On" : "Mic Off";
        if (stream) {
            const audioTracks = stream.getAudioTracks();
            audioTracks.forEach(track => track.enabled = micButton.classList.contains("active"));
        }
    });

    cameraButton.addEventListener("click", async () => {
        cameraButton.classList.toggle("active");
        cameraButton.textContent = cameraButton.classList.contains("active") ? "Camera On" : "Camera Off";

        if (cameraButton.classList.contains("active")) {
            try {
                stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
                liveVideo.srcObject = stream;
            } catch (error) {
                console.error("Error accessing media devices.", error);
            }
        } else {
            const videoTracks = stream.getVideoTracks();
            videoTracks.forEach(track => track.stop());
            liveVideo.srcObject = null;
        }
    });

    endCallButton.addEventListener("click", () => {
        window.location.href = '/dashboard ';
    });

    notesButton.addEventListener("click", () => {
        notesArea.classList.toggle("hidden");
    });

    sendNotesButton.addEventListener("click", () => {
        const message = notesInput.value.trim();
        if (message) {
            const messageElement = document.createElement("div");
            messageElement.classList.add("chat-message");
            messageElement.textContent = message;
            chatDisplay.appendChild(messageElement);
            notesInput.value = "";
            chatDisplay.scrollTop = chatDisplay.scrollHeight;
        }
    });

    shareScreenButton.addEventListener("click", async () => {
        shareScreenButton.classList.toggle("active");
        if (shareScreenButton.classList.contains("active")) {
            try {
                const screenStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
                liveVideo.srcObject = screenStream;

                screenStream.getVideoTracks()[0].addEventListener('ended', () => {
                    liveVideo.srcObject = stream;
                    shareScreenButton.classList.remove("active");
                    shareScreenButton.textContent = "Share Screen";
                });

                shareScreenButton.textContent = "Stop Sharing";
            } catch (error) {
                console.error("Error accessing display media.", error);
            }
        } else {
            liveVideo.srcObject = stream;
            shareScreenButton.textContent = "Share Screen";
        }
    });
});
