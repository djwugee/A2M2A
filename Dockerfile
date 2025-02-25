# Use an official Python base image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libjack-jackd2-dev \
    fluidsynth \
    ffmpeg \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    magenta \
    midi2audio

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p uploads output soundfonts

# Download and add a default SoundFont
# Download and add a default SoundFont (updated URL)
RUN wget https://github.com/FluidSynth/fluidsynth/raw/724b8c892d8335ad3bc808c675815eb9eaee6bc9/sf2/VintageDreamsWaves-v2.sf2 -O /app/soundfonts/VintageDreamsWaves-v2.sf2
# Copy application files into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Set environment variable for the SoundFont path
ENV SOUNDFONT_PATH=/app/soundfonts/VintageDreamsWaves-v2.sf2

# Run the Flask application
CMD ["python", "app.py"]
