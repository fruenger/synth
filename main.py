import numpy as np
import matplotlib.pyplot as plt

from scipy.io import wavfile
def damped_sine(times, freq, damping=1):
    return np.exp(-times/damping) * np.sin(np.pi*2*freq*times)

ENVELOPES = {
    "exp" : lambda t: 1
}


class spectrum():

    def __init__(self, freq, amp):

        self.frequencies = freq
        self.amp         = amp



class instrument():

    def __init__(self, name, spectrum):

        self.name     = name
        self.spectrum = spectrum



class play_event():

    def __init__(self, time, instrument, envelope, duration, **kwargs):

        self.time       = time
        self.instrument = instrument
        self.envelope   = envelope
        self.duration   = duration


    def event2samples(self, sampling_rate):

        times       = np.linspace(0., self.duration, self.duration * sampling_rate)
        raw_samples = np.zeros_like(times)
        env         = self.envelope(times)

        # paste the ifft code here ...
        raw_samples = np.sin(np.pi*2.*500.* times)

        return raw_samples



class timeline():

    def __init__(self, **kwargs):

        self.play_events = []


    def find_last_event(self):

        """Find the last play event in the current timeline."""
        times = [pe.time for pe in self.play_events]

        return np.max(times)


    def add_event(self, pe):

        self.play_events.append(pe)


    def generate_samples(self, sampling_rate):

        samples = np.full(
            sampling_rate * self.find_last_event(),
            0,
            dtype=np.float32
        )


if __name__ == "__main__":
  times = np.linspace(0., 5., 10000, dtype=np.float32)
  
  data = np.zeros_like(times)
  
  N_overtones = 20
  
  amps = 0.5*np.exp(-np.arange(N_overtones, dtype=np.float32) / 7.)
  freqs = 440. * np.arange(1, 1 + len(amps), 1, dtype=np.float32)
  
  freqs[::2] /= np.pi*3
  
  for amp, freq in zip(amps, freqs):
  
      data += amp * damped_sine(times, freq, damping=10000)
  
  wavfile.write("sound_file.wav", 2000, data)
