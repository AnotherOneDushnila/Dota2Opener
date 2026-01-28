import numpy as np
from typing import Optional



class Buffer:


    def __init__(self, sample_rate: int, window_sec: float, max_sec: Optional[float] = None):
        self.sample_rate = sample_rate
        self.window_sec = window_sec
        self.window_samples = int(sample_rate * window_sec)

        self.max_samples = (
            int(sample_rate * max_sec)
            if max_sec else self.window_samples
        )

        self._buffer = np.zeros(0, dtype=np.float32)


    def add(self, chunk: np.ndarray) -> Optional[np.ndarray]:
        self._buffer = np.concatenate([self._buffer, chunk])

        if len(self._buffer) > self.max_samples:
            self._buffer = self._buffer[-self.max_samples:]

        if self.is_ready():
            window = self._buffer[: self.window_samples]
            self._buffer = self._buffer[self.window_samples:]
            return window

        return None


    def is_ready(self) -> bool:
        return len(self._buffer) >= self.window_samples


    def reset(self):
        self._buffer = np.zeros(0, dtype=np.float32)
    
        
        
    