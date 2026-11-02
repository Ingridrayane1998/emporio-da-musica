/**
 * Web Audio Synthesizer para timbres de instrumentos da Empório da Música
 */
class AudioSynthesizer {
  constructor() {
    this.ctx = null;
    this.isMuted = false;
  }

  initContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || window.webkitAudioContext;
      if (AudioCtx) {
        this.ctx = new AudioCtx();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  toggleMute() {
    this.isMuted = !this.isMuted;
    return this.isMuted;
  }

  playTone(type = 'rock', duration = 2.4) {
    if (this.isMuted) return;
    try {
      this.initContext();
      if (!this.ctx) return;

      const now = this.ctx.currentTime;
      const masterGain = this.ctx.createGain();
      masterGain.gain.setValueAtTime(0.3, now);
      masterGain.connect(this.ctx.destination);

      if (type === 'rock') {
        const freqs = [82.41, 123.47, 164.81, 207.65];
        freqs.forEach((freq, i) => {
          this.createDistortedVoice(freq, now + i * 0.04, duration, masterGain);
        });
      } else if (type === 'acoustic') {
        const freqs = [98.00, 123.47, 146.83, 196.00, 293.66, 392.00];
        freqs.forEach((freq, i) => {
          this.createAcousticString(freq, now + i * 0.045, duration * 1.2, masterGain);
        });
      } else if (type === 'sparkle') {
        const freqs = [164.81, 246.94, 329.63, 493.88];
        freqs.forEach((freq, i) => {
          this.createBellChime(freq, now + i * 0.03, duration, masterGain);
        });
      } else {
        const freqs = [130.81, 164.81, 196.00, 246.94];
        freqs.forEach((freq, i) => {
          this.createJazzWarmVoice(freq, now + i * 0.05, duration * 1.4, masterGain);
        });
      }
    } catch (e) {
      console.warn("AudioContext bloqueado ou não suportado:", e);
    }
  }

  createDistortedVoice(freq, startTime, duration, dest) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const subOsc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, startTime);

    subOsc.type = 'triangle';
    subOsc.frequency.setValueAtTime(freq * 0.5, startTime);

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(2600, startTime);
    filter.Q.setValueAtTime(3, startTime);

    gain.gain.setValueAtTime(0.001, startTime);
    gain.gain.exponentialRampToValueAtTime(0.25, startTime + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.12, startTime + 0.3);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(filter);
    subOsc.connect(filter);
    filter.connect(gain);
    gain.connect(dest);

    osc.start(startTime);
    subOsc.start(startTime);
    osc.stop(startTime + duration);
    subOsc.stop(startTime + duration);
  }

  createAcousticString(freq, startTime, duration, dest) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, startTime);

    filter.type = 'bandpass';
    filter.frequency.setValueAtTime(freq * 2.2, startTime);
    filter.Q.setValueAtTime(1.8, startTime);

    gain.gain.setValueAtTime(0.001, startTime);
    gain.gain.exponentialRampToValueAtTime(0.2, startTime + 0.015);
    gain.gain.exponentialRampToValueAtTime(0.06, startTime + 0.5);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(dest);

    osc.start(startTime);
    osc.stop(startTime + duration);
  }

  createBellChime(freq, startTime, duration, dest) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq * 1.5, startTime);

    gain.gain.setValueAtTime(0.001, startTime);
    gain.gain.exponentialRampToValueAtTime(0.18, startTime + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(gain);
    gain.connect(dest);

    osc.start(startTime);
    osc.stop(startTime + duration);
  }

  createJazzWarmVoice(freq, startTime, duration, dest) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, startTime);

    filter.type = 'lowpass';
    filter.frequency.setValueAtTime(900, startTime);

    gain.gain.setValueAtTime(0.001, startTime);
    gain.gain.exponentialRampToValueAtTime(0.2, startTime + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(filter);
    filter.connect(gain);
    gain.connect(dest);

    osc.start(startTime);
    osc.stop(startTime + duration);
  }
}

window.soundSynth = new AudioSynthesizer();

