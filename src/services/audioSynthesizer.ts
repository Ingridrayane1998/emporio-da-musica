/**
 * Interactive Web Audio Synthesizer for Empório da Música & Ozzy
 * Generates guitar strums, tube-amp saturation harmonics, acoustic resonance and chord tones.
 */

class AudioSynthesizer {
  private ctx: AudioContext | null = null;
  private isMuted: boolean = false;

  private initContext() {
    if (!this.ctx) {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      this.ctx = new AudioCtx();
    }
    if (this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  public toggleMute() {
    this.isMuted = !this.isMuted;
    return this.isMuted;
  }

  public getMuted() {
    return this.isMuted;
  }

  /**
   * Plays a musical tone based on instrument profile
   */
  public playTone(type: 'rock' | 'acoustic' | 'blues' | 'jazz' | 'sparkle' = 'rock', duration: number = 2.4) {
    if (this.isMuted) return;
    try {
      this.initContext();
      if (!this.ctx) return;

      const now = this.ctx.currentTime;
      const masterGain = this.ctx.createGain();
      masterGain.gain.setValueAtTime(0.3, now);
      masterGain.connect(this.ctx.destination);

      if (type === 'rock') {
        // Power chord with harmonic tube saturation (E2, B2, E3, G#3)
        const freqs = [82.41, 123.47, 164.81, 207.65];
        freqs.forEach((freq, i) => {
          this.createDistortedVoice(freq, now + i * 0.04, duration, masterGain);
        });
      } else if (type === 'acoustic') {
        // Lush open acoustic chord strum (G major: G2, B2, D3, G3, D4, G4)
        const freqs = [98.00, 123.47, 146.83, 196.00, 293.66, 392.00];
        freqs.forEach((freq, i) => {
          this.createAcousticString(freq, now + i * 0.045, duration * 1.2, masterGain);
        });
      } else if (type === 'blues') {
        // Blues bent note & minor 7th lick
        const notes = [
          { freq: 196.00, delay: 0.0, dur: 0.4 },
          { freq: 220.00, delay: 0.35, dur: 0.4 },
          { freq: 246.94, delay: 0.7, dur: 0.6 },
          { freq: 293.66, delay: 1.2, dur: 1.2 }
        ];
        notes.forEach(n => {
          this.createWarmTubeVoice(n.freq, now + n.delay, n.dur, masterGain);
        });
      } else if (type === 'sparkle') {
        // Fender Strat chime with high harmonics (Position 4: neck + middle)
        const freqs = [164.81, 246.94, 329.63, 493.88];
        freqs.forEach((freq, i) => {
          this.createBellChime(freq, now + i * 0.03, duration, masterGain);
        });
      } else {
        // Warm Jazz 7th chord (Cmaj7)
        const freqs = [130.81, 164.81, 196.00, 246.94];
        freqs.forEach((freq, i) => {
          this.createJazzWarmVoice(freq, now + i * 0.05, duration * 1.4, masterGain);
        });
      }
    } catch {
      // AudioContext could be blocked by browser policy until interaction
    }
  }

  private createDistortedVoice(freq: number, startTime: number, duration: number, dest: AudioNode) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const subOsc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();
    const filter = this.ctx.createBiquadFilter();

    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(freq, startTime);

    subOsc.type = 'triangle';
    subOsc.frequency.setValueAtTime(freq * 0.5, startTime);

    // Warm tube amp lowpass
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

  private createAcousticString(freq: number, startTime: number, duration: number, dest: AudioNode) {
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

  private createWarmTubeVoice(freq: number, startTime: number, duration: number, dest: AudioNode) {
    if (!this.ctx) return;
    const osc = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(freq, startTime);
    // Slight vibrato
    osc.frequency.setValueAtTime(freq * 1.01, startTime + duration * 0.5);

    gain.gain.setValueAtTime(0.001, startTime);
    gain.gain.exponentialRampToValueAtTime(0.22, startTime + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, startTime + duration);

    osc.connect(gain);
    gain.connect(dest);

    osc.start(startTime);
    osc.stop(startTime + duration);
  }

  private createBellChime(freq: number, startTime: number, duration: number, dest: AudioNode) {
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

  private createJazzWarmVoice(freq: number, startTime: number, duration: number, dest: AudioNode) {
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

export const soundSynth = new AudioSynthesizer();
