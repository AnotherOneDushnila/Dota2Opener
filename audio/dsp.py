import numpy as np
import yaml
from scipy.fft import rfft, rfftfreq



with open('../config.yml', 'r') as file:
    config = yaml.load_all(file, Loader=yaml.CLoader)


def rms(audio: np.ndarray) -> float:
    if audio.size == 0:
        return 0.0
    return float(np.sqrt(np.mean(audio**2)))
    

def transient_score(audio: np.ndarray) -> float:
    if audio.size < 2:
        return 0.0
    return float(np.mean(abs(np.diff(audio))))


def high_freq_ratio(audio: np.ndarray, sample_rate: int, cutoff_hz: int = 4000) -> float:
    if audio.size == 0:
        return 0.0

    audio = audio * np.hanning(len(audio))

    spectrum = rfft(audio)
    freqs = rfftfreq(len(audio), d=1 / sample_rate)

    energy = np.abs(spectrum) ** 2

    total_energy = np.sum(energy)
    if total_energy == 0:
        return 0.0

    hf_energy = np.sum(energy[freqs >= cutoff_hz])

    return float(hf_energy / total_energy)


def looks_like_can(audio: np.ndarray, sample_rate: int, cfg: dict) -> bool:
    if rms(audio) > cfg['dsp']['rms_treshold']:
        if transient_score(audio) > cfg['dsp']['ts_treshold']:
            if high_freq_ratio(audio, sample_rate) > cfg['dsp']['hf_ratio']:
                return True
    return False