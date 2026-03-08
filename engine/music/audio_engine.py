import math
import wave
import struct


SAMPLE_RATE = 44100
BASE_FREQ = 293.66  # D4


def semitone_to_freq(base, semitone):
    return base * (2 ** (semitone / 12))


def render_from_snapshot(snapshot, filename="organism_cognitive.wav"):

    harmony = snapshot["harmony"]
    melody = snapshot["melody"]
    rhythm = snapshot["rhythm"]
    instrumentation = snapshot["instrumentation"]
    form = snapshot["form"]

    scale = harmony["scale"]
    progression = harmony["progression"]
    bpm = rhythm["bpm"]

    seconds_per_section = 60.0 / bpm * 8
    samples_per_section = int(SAMPLE_RATE * seconds_per_section)

    audio = []

    for section in form["timeline"]:

        section_intensity = section["intensity"]
        section_tension = section["tension"]

        for n in range(samples_per_section):

            t = n / SAMPLE_RATE
            v = 0.0

            # Harmonic Layer
            for chord in progression:
                for note in chord.split("-"):
                    if note in scale:
                        semitone = scale.index(note)
                    else:
                        semitone = 0

                    freq = semitone_to_freq(BASE_FREQ, semitone * 2)
                    v += math.sin(2 * math.pi * freq * t)

            # Melody Layer
            for note in melody["melody"]:
                if note in scale:
                    semitone = scale.index(note)
                    freq = semitone_to_freq(BASE_FREQ, semitone * 2 + 12)
                    v += 0.5 * math.sin(2 * math.pi * freq * t)

            v /= (len(progression) + len(melody["melody"]) + 1)

            envelope = math.sin(math.pi * n / samples_per_section)

            v *= envelope * section_intensity * (0.5 + section_tension)

            audio.append(v)

    if not audio:
        print("No audio generated.")
        return

    mx = max(abs(x) for x in audio)
    if mx > 0:
        audio = [x / mx for x in audio]

    wav = wave.open(filename, "w")
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(SAMPLE_RATE)

    for s in audio:
        wav.writeframes(struct.pack("h", int(s * 32767)))

    wav.close()

    print(f"Cognitive organism audio rendered: {filename}")
