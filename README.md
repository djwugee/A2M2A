Audio to MIDI to Audio Converter

Overview

This project converts audio files (MP3/WAV) to MIDI and back to audio using:

FFmpeg (MP3 to WAV conversion)

Magenta (Audio to MIDI conversion)

FluidSynth (MIDI to Audio synthesis)

Flask (Backend API with real-time status updates)

Docker (Containerized deployment)



---

1. Features

✅ Supports MP3 & WAV input
✅ Real-time conversion status updates
✅ Converts MP3 to WAV before processing
✅ MIDI synthesis to MP3 output
✅ Docker support


---

2. Installation & Setup

Run Locally

Step 1: Install Dependencies

pip install flask magenta fluidsynth

Step 2: Run the Flask Server

python app.py

Step 3: Open index.html in a browser


---

Run with Docker

Step 1: Build Docker Image

docker build -t audio-midi-converter .

Step 2: Run Container

docker run -p 5000:5000 -v $(pwd)/uploads:/app/uploads -v $(pwd)/output:/app/output audio-midi-converter

Then open index.html in a browser.


---

3. Usage

Web UI

1. Upload a WAV or MP3 file.


2. Click Convert.


3. Track real-time conversion status.


4. Download the final MP3.




---

4. API Endpoints

Example cURL Request

curl -X POST -F "file=@input.mp3" http://localhost:5000/process


---

5. File Structure

/app
│── app.py         # Flask Backend
│── index.html     # Frontend UI
│── Dockerfile     # Docker Container Setup
│── /uploads       # Uploaded files
│── /output        # Processed files
│── /soundfonts    # SoundFont files


---

6. Technologies Used

FFmpeg (Audio conversion)

Magenta (Audio to MIDI)

FluidSynth (MIDI to Audio)

Flask (API & UI backend)

Docker (Containerization)

