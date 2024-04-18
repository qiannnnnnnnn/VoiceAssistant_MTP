import subprocess
import os
import math

# Define a function to calculate the tempo factor based on semitones
def get_tempo_factor(semitones):
  """
  This function calculates the tempo factor for a given number of semitones.
  """
  return math.pow(2, semitones / 12)

# Load audio data
with open(os.path.join("output", "output_audio.mp3"), "rb") as f:
    audio_data = f.read()

# Define semitone values
semitones_list = [2.5, 3, 4]  # You can adjust this list for different semitones

for semitones in semitones_list:
  # Calculate tempo factor
  tempo_factor = get_tempo_factor(semitones)

  # Construct the ffmpeg command with calculated tempo factor
  ffmpeg_command = [
      "ffmpeg",
      "-i", "-",
      "-af", f"atempo={tempo_factor},asetrate=44100*{tempo_factor}",
      "-f", "wav", "-"]

  # Define output filename based on semitones
  output_file = os.path.join("output", f"output_pitch_changed_{semitones}.wav")

  # Execute ffmpeg command with subprocess
  with subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
      output_data, _ = process.communicate(input=audio_data)
      with open(output_file, 'wb') as f:
          f.write(output_data)

  print(f"Finished processing audio with {semitones} semitones")
