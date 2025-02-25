from flask import Flask, request, jsonify, send_file, Response
import os
import subprocess
import time

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"
SOUNDFONT = "/soundfonts/FluidR3_GM.sf2"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

status_messages = ["Waiting for upload..."]

def send_status():
    """Send real-time status updates to the frontend"""
    def event_stream():
        while True:
            if status_messages:
                yield f"data: {status_messages[-1]}\n\n"
            time.sleep(1)
    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/status')
def status():
    return send_status()

@app.route('/process', methods=['POST'])
def process_audio():
    global status_messages
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    input_audio = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(input_audio)

    # Convert MP3 to WAV if needed
    if file.filename.lower().endswith('.mp3'):
        status_messages.append("Converting MP3 to WAV...")
        wav_audio = os.path.join(UPLOAD_FOLDER, "converted.wav")
        mp3_to_wav = subprocess.run(["ffmpeg", "-i", input_audio, "-ar", "16000", wav_audio])
        if mp3_to_wav.returncode != 0:
            return jsonify({"error": "MP3 to WAV conversion failed"}), 500
        input_audio = wav_audio

    output_midi = os.path.join(OUTPUT_FOLDER, "output.mid")
    output_wav = os.path.join(OUTPUT_FOLDER, "output.wav")
    output_mp3 = os.path.join(OUTPUT_FOLDER, "output.mp3")

    # Step 1: Convert Audio to MIDI using Magenta
    status_messages.append("Converting Audio to MIDI...")
    midi_conversion = subprocess.run([
        "onsets_frames_transcription_infer",
        "--acoustic_run_dir=/content/onsets-frames/train",
        "--examples_path=" + input_audio,
        "--output_dir=" + OUTPUT_FOLDER
    ])

    if midi_conversion.returncode != 0 or not os.path.exists(output_midi):
        return jsonify({"error": "MIDI conversion failed"}), 500

    # Step 2: Convert MIDI to Audio using FluidSynth
    status_messages.append("Converting MIDI to Audio...")
    audio_synthesis = subprocess.run([
        "fluidsynth", "-ni", SOUNDFONT, output_midi, "-F", output_wav, "-r", "44100"
    ])

    if audio_synthesis.returncode != 0 or not os.path.exists(output_wav):
        return jsonify({"error": "MIDI to Audio conversion failed"}), 500

    # Step 3: Convert WAV to MP3 using FFmpeg
    status_messages.append("Converting WAV to MP3...")
    mp3_conversion = subprocess.run([
        "ffmpeg", "-i", output_wav, "-q:a", "2", output_mp3
    ])

    if mp3_conversion.returncode != 0 or not os.path.exists(output_mp3):
        return jsonify({"error": "MP3 conversion failed"}), 500

    status_messages.append("Conversion complete! Ready for download.")
    return send_file(output_mp3, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)