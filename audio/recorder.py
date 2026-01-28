import sounddevice as sd
from queue import Queue


class Recorder:


    def __init__(self, sample_rate: int, channels: int, chunk_size: int, device) -> None:
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_size = chunk_size
        self.device = device
        self._queue = Queue()
        self._stream = None
        self._running = False
    

    def _callback(self, indata, frames, time, status) -> None:
        if status:
            print(f'[Audio]: {status}')
        
        audio = indata.copy().flatten()
        self._queue.put(audio)


    def start(self) -> None:
        if self._running:
            return
        
        self._stream = sd.InputStream(
            samplerate=self.sample_rate, 
            blocksize=self.chunk_size, 
            device=self.device, 
            channels=self.channels,
            callback=self._callback
            )
        
        self._stream.start()
        self._running = True


    def stop(self) -> None:
        if self._stream:
            self._stream.stop()
            self._stream.close()
        self._running = False

    
    def stream(self):
        self.start()

        try:
            while True:
                yield self._queue.get()
        except GeneratorExit:
            self.stop()