# Use an official Python base image
FROM python:3.8

# Install system dependencies
RUN apt-get update && apt-get install -y \
    fluidsynth \
    ffmpeg \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install flask magenta fluidsynth

# Create directories for input/output
WORKDIR /app
RUN mkdir -p uploads output soundfonts

# Download and add a default SoundFont
RUN wget http://ftp.osuosl.org/pub/musescore/soundfont/MuseScore_General.sf3 -O /soundfonts/FluidR3_GM.sf2

# Copy app files into the container
COPY app.py /app/
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]