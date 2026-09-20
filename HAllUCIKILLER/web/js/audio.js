/* ==========================================================================
   RAZOR-SHARP SAMURAI KATANA SOUND SYNTHESIZER (Web Audio API)
   Authentic procedural physical modeling of Japanese katana sword mechanics:
   - Koiguchi-Kiri (鯉口切り): Razor-sharp thumb unlock & tsuba click
   - Saya-Biki & Nukimi (鞘引き・抜き身): Ultra-sharp blade drawing from scabbard (SHIIIIING!)
   - Iai Slash & Ring (居合斬り・残心): Razor blade slice & crystalline steel resonance
   - Tsubazeriai (鍔迫り合い): Harsh blade clash, parry sparks & jarring steel friction
   ========================================================================== */

class SamuraiKatanaSound {
  constructor() {
    this.enabled = true;
    this.ctx = null;
    this.noiseBuffer = null;
  }

  initAudio() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      if (AudioContext) {
        this.ctx = new AudioContext();
        this._buildNoiseBuffer();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  }

  _buildNoiseBuffer() {
    if (!this.ctx || this.noiseBuffer) return;
    const bufferSize = this.ctx.sampleRate * 2;
    this.noiseBuffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const output = this.noiseBuffer.getChannelData(0);
    for (let i = 0; i < bufferSize; i++) {
      output[i] = Math.random() * 2 - 1;
    }
  }

  toggle() {
    this.enabled = !this.enabled;
    return this.enabled;
  }

  // 1. Koiguchi-Kiri: Razor-sharp thumb unlock & tsuba click ("TCHK-TING!")
  playClick() {
    if (!this.enabled) return;
    this.initAudio();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;

    // A. Ultra-crisp razor metal snap (High FM ping)
    const carrier = this.ctx.createOscillator();
    const carrierGain = this.ctx.createGain();
    const mod = this.ctx.createOscillator();
    const modGain = this.ctx.createGain();

    carrier.type = 'sine';
    carrier.frequency.setValueAtTime(4200, t);
    carrier.frequency.exponentialRampToValueAtTime(2100, t + 0.035);

    mod.type = 'sawtooth';
    mod.frequency.setValueAtTime(1400, t);
    modGain.gain.setValueAtTime(1800, t);
    modGain.gain.exponentialRampToValueAtTime(1, t + 0.035);

    carrierGain.gain.setValueAtTime(0.18, t);
    carrierGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.04);

    mod.connect(carrier.frequency);
    carrier.connect(carrierGain);
    carrierGain.connect(this.ctx.destination);

    mod.start(t);
    carrier.start(t);
    mod.stop(t + 0.045);
    carrier.stop(t + 0.045);

    // B. Wood/lacquer saya latch click (Crisp highpass impulse)
    if (this.noiseBuffer) {
      const noise = this.ctx.createBufferSource();
      noise.buffer = this.noiseBuffer;
      const filter = this.ctx.createBiquadFilter();
      filter.type = 'bandpass';
      filter.frequency.setValueAtTime(3200, t);
      filter.Q.setValueAtTime(8.0, t);

      const noiseGain = this.ctx.createGain();
      noiseGain.gain.setValueAtTime(0.22, t);
      noiseGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.03);

      noise.connect(filter);
      filter.connect(noiseGain);
      noiseGain.connect(this.ctx.destination);
      noise.start(t);
      noise.stop(t + 0.035);
    }
  }

  // 2. Saya-Biki & Nukimi: Ultra-Sharp Katana Blade Unsheathing from Cover ("SHIIII-IIIING!")
  playScanSweep() {
    if (!this.enabled) return;
    this.initAudio();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;

    // A. High-Friction Steel Sliding Out of Scabbard (Razor edge scraping throat)
    if (this.noiseBuffer) {
      const rasp = this.ctx.createBufferSource();
      rasp.buffer = this.noiseBuffer;

      // Highpass to eliminate muddiness and give that razor-sharp metallic bite
      const hpFilter = this.ctx.createBiquadFilter();
      hpFilter.type = 'highpass';
      hpFilter.frequency.setValueAtTime(2200, t);

      // Sweeping sharp resonant bandpass (imitating blade acceleration out of saya)
      const bpFilter = this.ctx.createBiquadFilter();
      bpFilter.type = 'bandpass';
      bpFilter.frequency.setValueAtTime(2800, t);
      bpFilter.frequency.exponentialRampToValueAtTime(6800, t + 0.18);
      bpFilter.frequency.exponentialRampToValueAtTime(3400, t + 0.38);
      bpFilter.Q.setValueAtTime(10.0, t);

      const raspGain = this.ctx.createGain();
      raspGain.gain.setValueAtTime(0.001, t);
      raspGain.gain.exponentialRampToValueAtTime(0.28, t + 0.07);
      raspGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.38);

      rasp.connect(hpFilter);
      hpFilter.connect(bpFilter);
      bpFilter.connect(raspGain);
      raspGain.connect(this.ctx.destination);
      rasp.start(t);
      rasp.stop(t + 0.4);
    }

    // B. Metallic FM "SHIIING" Sheen (Simulates razor steel edge resonance)
    const fmCarrier = this.ctx.createOscillator();
    const fmCarrierGain = this.ctx.createGain();
    const fmMod = this.ctx.createOscillator();
    const fmModGain = this.ctx.createGain();

    fmCarrier.type = 'sine';
    fmCarrier.frequency.setValueAtTime(3400, t);
    fmCarrier.frequency.exponentialRampToValueAtTime(5200, t + 0.14);
    fmCarrier.frequency.exponentialRampToValueAtTime(2600, t + 0.42);

    fmMod.type = 'triangle';
    fmMod.frequency.setValueAtTime(840, t);
    fmMod.frequency.exponentialRampToValueAtTime(1420, t + 0.14);
    fmModGain.gain.setValueAtTime(1200, t);
    fmModGain.gain.exponentialRampToValueAtTime(0.001, t + 0.38);

    fmCarrierGain.gain.setValueAtTime(0.001, t);
    fmCarrierGain.gain.exponentialRampToValueAtTime(0.18, t + 0.08);
    fmCarrierGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.45);

    fmMod.connect(fmCarrier.frequency);
    fmCarrier.connect(fmCarrierGain);
    fmCarrierGain.connect(this.ctx.destination);

    fmMod.start(t);
    fmCarrier.start(t);
    fmMod.stop(t + 0.46);
    fmCarrier.stop(t + 0.46);

    // C. Free Blade Vibrato Ring (High crystalline steel glint ringing in air)
    const harmonics = [3200, 4800, 7100];
    harmonics.forEach((freq, idx) => {
      const ringOsc = this.ctx.createOscillator();
      const ringGain = this.ctx.createGain();

      ringOsc.type = 'sine';
      ringOsc.frequency.setValueAtTime(freq, t + 0.06);
      ringOsc.frequency.exponentialRampToValueAtTime(freq * 0.95, t + 0.55);

      ringGain.gain.setValueAtTime(0.0001, t);
      ringGain.gain.setValueAtTime(0.08 / (idx + 1), t + 0.08);
      ringGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.55);

      ringOsc.connect(ringGain);
      ringGain.connect(this.ctx.destination);

      ringOsc.start(t + 0.06);
      ringOsc.stop(t + 0.56);
    });
  }

  // 3. Iai Slash & Shimmering Tempered Steel Resonance (Pass Chime)
  playPassChime() {
    if (!this.enabled) return;
    this.initAudio();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;

    // Fast razor-sharp air slicing whoosh
    if (this.noiseBuffer) {
      const slice = this.ctx.createBufferSource();
      slice.buffer = this.noiseBuffer;

      const hpFilter = this.ctx.createBiquadFilter();
      hpFilter.type = 'highpass';
      hpFilter.frequency.setValueAtTime(3000, t);

      const bpFilter = this.ctx.createBiquadFilter();
      bpFilter.type = 'bandpass';
      bpFilter.frequency.setValueAtTime(5400, t);
      bpFilter.frequency.exponentialRampToValueAtTime(1200, t + 0.12);
      bpFilter.Q.setValueAtTime(6.0, t);

      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.3, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.13);

      slice.connect(hpFilter);
      hpFilter.connect(bpFilter);
      bpFilter.connect(gain);
      gain.connect(this.ctx.destination);
      slice.start(t);
      slice.stop(t + 0.14);
    }

    // High crystalline Tamahagane harmonic chime (Pure pentatonic bell tones)
    const steelPitches = [880.0, 1318.51, 1760.0, 2637.02, 3520.0];
    steelPitches.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sine';
      osc.frequency.setValueAtTime(freq, t + 0.02);

      const peakGain = 0.12 / (idx + 1);
      gain.gain.setValueAtTime(0.001, t);
      gain.gain.exponentialRampToValueAtTime(peakGain, t + 0.035);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.75 + idx * 0.08);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(t + 0.02);
      osc.stop(t + 0.8 + idx * 0.08);
    });
  }

  // 4. Katana Blade Clash & Steel Sparks (Alert Fail)
  playAlertFail() {
    if (!this.enabled) return;
    this.initAudio();
    if (!this.ctx) return;

    const t = this.ctx.currentTime;

    // A. Piercing razor-sharp steel clash impact & grating spark noise
    if (this.noiseBuffer) {
      const clashNoise = this.ctx.createBufferSource();
      clashNoise.buffer = this.noiseBuffer;

      const hp = this.ctx.createBiquadFilter();
      hp.type = 'highpass';
      hp.frequency.setValueAtTime(2400, t);

      const bp = this.ctx.createBiquadFilter();
      bp.type = 'bandpass';
      bp.frequency.setValueAtTime(4200, t);
      bp.frequency.exponentialRampToValueAtTime(1400, t + 0.18);
      bp.Q.setValueAtTime(5.0, t);

      const gain = this.ctx.createGain();
      gain.gain.setValueAtTime(0.4, t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.18);

      clashNoise.connect(hp);
      hp.connect(bp);
      bp.connect(gain);
      gain.connect(this.ctx.destination);
      clashNoise.start(t);
      clashNoise.stop(t + 0.19);
    }

    // B. Low-end blade weight impact
    const thud = this.ctx.createOscillator();
    const thudGain = this.ctx.createGain();
    thud.type = 'sine';
    thud.frequency.setValueAtTime(220, t);
    thud.frequency.exponentialRampToValueAtTime(55, t + 0.12);
    thudGain.gain.setValueAtTime(0.28, t);
    thudGain.gain.exponentialRampToValueAtTime(0.0001, t + 0.12);
    thud.connect(thudGain);
    thudGain.connect(this.ctx.destination);
    thud.start(t);
    thud.stop(t + 0.13);

    // C. Harsh discordant steel vibration (Tsubazeriai)
    const clashFreqs = [920, 980, 1540, 2240, 3180];
    clashFreqs.forEach((freq, idx) => {
      const osc = this.ctx.createOscillator();
      const gain = this.ctx.createGain();

      osc.type = 'sawtooth';
      osc.frequency.setValueAtTime(freq, t);
      osc.frequency.linearRampToValueAtTime(freq * 0.94, t + 0.32);

      gain.gain.setValueAtTime(0.12 / (idx + 1), t);
      gain.gain.exponentialRampToValueAtTime(0.0001, t + 0.32);

      osc.connect(gain);
      gain.connect(this.ctx.destination);

      osc.start(t);
      osc.stop(t + 0.33);
    });
  }
}

// Global instance compatible with all callers
window.cyberSound = new SamuraiKatanaSound();
window.katanaSound = window.cyberSound;
