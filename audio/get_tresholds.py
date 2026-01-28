import time, sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.logger import log
from audio.recorder import Recorder
from audio.buffer import Buffer
from audio.dsp import rms, transient_score, high_freq_ratio



SAMPLE_RATE = 44100
WINDOW_SEC = 0.5
PRINT_EVERY = 0.5


def main():
    logger = log('debug_tresholds')
    recorder = Recorder(
        sample_rate=SAMPLE_RATE,
        chunk_size=1024,
        channels=1,
        device=None
    )

    buffer = Buffer(
        sample_rate=SAMPLE_RATE,
        window_sec=WINDOW_SEC
    )

    last_print = time.time()

    print("Debug DSP started")
    print("Open a can")
    print("-" * 50)

    for chunk in recorder.stream():
        window = buffer.add(chunk)

        if window is None:
            continue

        now = time.time()
        if now - last_print < PRINT_EVERY:
            continue

        last_print = now

        r = rms(window)
        t = transient_score(window)
        hf = high_freq_ratio(window, SAMPLE_RATE)

        logger.info(f"RMS: {r:.4f} | "f"Transient: {t:.5f} | "f"HF ratio: {hf:.3f}")
            
        
if __name__ == "__main__":
    main()