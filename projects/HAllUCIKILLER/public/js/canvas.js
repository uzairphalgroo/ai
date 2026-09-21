/* ==========================================================================
   2027 3D CYBER-ANIME MECHA SENTINEL & NEURAL RUNES CANVAS
   Interactive 3D geometry, tracking anime mecha head, floating funnels,
   holographic Kanji halos, and reactive cursor particle physics.
   ========================================================================== */

class AnimeMecha3DCanvas {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    if (!this.canvas) return;
    this.ctx = this.canvas.getContext('2d');

    this.mouseX = 0;
    this.mouseY = 0;
    this.targetMouseX = 0;
    this.targetMouseY = 0;
    this.scrollY = 0;
    this.scrollVelocity = 0;
    this.lastScrollY = 0;
    this.time = 0;
    this.pulseWave = 0;

    this.particles = [];
    this.funnels = [];

    this.init();
  }

  init() {
    this.resize();
    window.addEventListener('resize', () => this.resize());
    window.addEventListener('mousemove', (e) => {
      this.targetMouseX = (e.clientX - this.width / 2);
      this.targetMouseY = (e.clientY - this.height / 2);
    });

    window.addEventListener('scroll', () => {
      this.scrollY = window.scrollY || window.pageYOffset;
      this.scrollVelocity = (this.scrollY - this.lastScrollY) * 0.12;
      this.lastScrollY = this.scrollY;
    });

    window.addEventListener('click', () => {
      this.pulseWave = 1.0;
    });

    // 3D Particles
    for (let i = 0; i < 90; i++) {
      this.particles.push({
        x: (Math.random() - 0.5) * 1400,
        y: (Math.random() - 0.5) * 1000,
        z: Math.random() * 800 + 100,
        vx: (Math.random() - 0.5) * 0.8,
        vy: (Math.random() - 0.5) * 0.8,
        vz: (Math.random() - 0.5) * 1.2,
        size: Math.random() * 2.5 + 1.0,
        color: Math.random() > 0.4 ? '#ff0044' : (Math.random() > 0.5 ? '#00f0ff' : '#9d00ff')
      });
    }

    // Floating Tactical Drone Funnels (Bit Drones)
    for (let f = 0; f < 3; f++) {
      this.funnels.push({
        angle: (f * Math.PI * 2) / 3,
        distance: 260 + f * 40,
        speed: 0.015 + f * 0.005,
        yOffset: (f - 1) * 80,
        trail: []
      });
    }

    this.animate();
  }

  resize() {
    this.width = this.canvas.width = window.innerWidth;
    this.height = this.canvas.height = window.innerHeight;
  }

  // 3D Point Projection Helper
  project(x, y, z, rotX = 0, rotY = 0, rotZ = 0) {
    // Rotate Y
    let cosY = Math.cos(rotY), sinY = Math.sin(rotY);
    let x1 = x * cosY - z * sinY;
    let z1 = z * cosY + x * sinY;

    // Rotate X
    let cosX = Math.cos(rotX), sinX = Math.sin(rotX);
    let y2 = y * cosX - z1 * sinX;
    let z2 = z1 * cosX + y * sinX;

    // Camera Perspective FOV
    const fov = 650;
    const scale = fov / (fov + z2 + 400);

    return {
      x: this.width / 2 + x1 * scale,
      y: this.height / 2 + y2 * scale,
      scale: scale,
      z: z2
    };
  }

  animate() {
    this.time += 0.025;
    this.scrollVelocity *= 0.93;
    if (this.pulseWave > 0.01) this.pulseWave *= 0.92;

    // Smooth Mouse Interpolation
    this.mouseX += (this.targetMouseX - this.mouseX) * 0.08;
    this.mouseY += (this.targetMouseY - this.mouseY) * 0.08;

    this.ctx.clearRect(0, 0, this.width, this.height);

    // Dynamic 3D Character Rotation Angles based on Mouse Tracking
    const charRotY = (this.mouseX / (this.width / 2)) * 0.55;
    const charRotX = (-this.mouseY / (this.height / 2)) * 0.45;

    // 1. Draw 3D Background Particles
    this.draw3DParticles();

    // 2. Draw Holographic Tactical Halo & Kanji Defense Rings
    this.drawHoloHalo(charRotX, charRotY);

    // 3. Draw 3D Interactive Anime Cyber Mecha Sentinel
    this.drawMechaCharacter(charRotX, charRotY);

    // 4. Draw Orbiting Tactical Drone Funnels
    this.drawFunnels(charRotX, charRotY);

    // 5. Tactical Crosshair / Cursor Lock-on HUD
    this.drawCursorHUD();

    requestAnimationFrame(() => this.animate());
  }

  draw3DParticles() {
    for (let p of this.particles) {
      p.x += p.vx;
      p.y += p.vy - this.scrollVelocity * 0.4;
      p.z += p.vz;

      if (p.x < -800) p.x = 800;
      if (p.x > 800) p.x = -800;
      if (p.y < -600) p.y = 600;
      if (p.y > 600) p.y = -600;
      if (p.z < 0) p.z = 800;
      if (p.z > 800) p.z = 0;

      const pt = this.project(p.x, p.y, p.z);
      if (pt.scale > 0) {
        this.ctx.beginPath();
        this.ctx.arc(pt.x, pt.y, Math.max(0.5, p.size * pt.scale), 0, Math.PI * 2);
        this.ctx.fillStyle = p.color;
        this.ctx.shadowBlur = 8;
        this.ctx.shadowColor = p.color;
        this.ctx.fill();
      }
    }
  }

  drawHoloHalo(rotX, rotY) {
    const center = this.project(0, -60, 200, rotX * 0.3, rotY * 0.3);
    const radius = 220 * center.scale;

    // Outer Hologram Ring
    this.ctx.save();
    this.ctx.translate(center.x, center.y);
    this.ctx.rotate(this.time * 0.4);

    this.ctx.beginPath();
    this.ctx.arc(0, 0, radius, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(255, 0, 68, 0.45)';
    this.ctx.lineWidth = 2.5;
    this.ctx.setLineDash([18, 12, 6, 12]);
    this.ctx.stroke();

    // Inner Counter-Rotating Cyan Ring
    this.ctx.beginPath();
    this.ctx.arc(0, 0, radius * 0.82, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.5)';
    this.ctx.lineWidth = 1.5;
    this.ctx.setLineDash([35, 15]);
    this.ctx.stroke();

    // Kanji & Tactical Glyphs along ring
    this.ctx.setLineDash([]);
    this.ctx.font = `bold ${Math.max(10, Math.floor(14 * center.scale))}px "JetBrains Mono", monospace`;
    this.ctx.fillStyle = '#ff0044';
    this.ctx.textAlign = 'center';

    const glyphs = ['警告 // CRITICAL', '防衛 // ACTIVE', '異常 // ANOMALY', '01 // SYNC', 'THREAT // P0', 'MATRIX // SHIELD'];
    for (let i = 0; i < glyphs.length; i++) {
      const angle = (i * Math.PI * 2) / glyphs.length;
      const gx = Math.cos(angle) * (radius * 0.92);
      const gy = Math.sin(angle) * (radius * 0.92);
      this.ctx.save();
      this.ctx.translate(gx, gy);
      this.ctx.rotate(angle + Math.PI / 2);
      this.ctx.fillText(glyphs[i], 0, 0);
      this.ctx.restore();
    }

    this.ctx.restore();

    // Pulse Wave Blast Effect on Click
    if (this.pulseWave > 0.05) {
      this.ctx.beginPath();
      this.ctx.arc(center.x, center.y, radius * (2.2 - this.pulseWave), 0, Math.PI * 2);
      this.ctx.strokeStyle = `rgba(255, 0, 68, ${this.pulseWave * 0.8})`;
      this.ctx.lineWidth = 4 * this.pulseWave;
      this.ctx.stroke();
    }
  }

  drawMechaCharacter(rotX, rotY) {
    // Base 3D Anchor for Mecha Sentinel
    const baseY = 30 + Math.sin(this.time * 1.5) * 12; // Gentle floating breath
    const baseZ = 20;

    // Mecha Head / Mask 3D Vertex Coordinates
    const vertices = {
      // V-Fin Crest
      vFinL: [-120, -160, -40],
      vFinR: [120, -160, -40],
      vFinCenter: [0, -100, -20],
      vFinTipL: [-190, -240, -80],
      vFinTipR: [190, -240, -80],

      // Forehead & Crown
      crownTop: [0, -110, -60],
      crownL: [-60, -80, -50],
      crownR: [60, -80, -50],

      // Visor Eye Slit (Glowing Cyber Visor)
      visorL: [-70, -35, -75],
      visorR: [70, -35, -75],
      visorCenter: [0, -30, -90],
      visorBotL: [-50, -20, -70],
      visorBotR: [50, -20, -70],

      // Face Mask & Chin
      faceL: [-80, 10, -40],
      faceR: [80, 10, -40],
      chinL: [-35, 75, -60],
      chinR: [35, 75, -60],
      chinTip: [0, 105, -80],

      // Cyber Collar & Shoulders
      collarL: [-130, 90, 0],
      collarR: [130, 90, 0],
      shoulderL: [-240, 140, 60],
      shoulderR: [240, 140, 60],
      chestCore: [0, 130, -50],
      torsoBot: [0, 220, 20],

      // Floating Energy Blades / Wings
      wingL1: [-280, -120, 120],
      wingL2: [-340, 40, 140],
      wingR1: [280, -120, 120],
      wingR2: [340, 40, 140]
    };

    // Project 3D vertices into 2D screenspace with dynamic rotation
    const p = {};
    for (let [k, v] of Object.entries(vertices)) {
      p[k] = this.project(v[0], v[1] + baseY, v[2] + baseZ, rotX, rotY);
    }

    this.ctx.save();

    // 1. Draw Energy Wings
    this.drawPoly([p.collarL, p.wingL1, p.wingL2, p.shoulderL], 'rgba(255, 0, 68, 0.25)', '#ff0044', 2);
    this.drawPoly([p.collarR, p.wingR1, p.wingR2, p.shoulderR], 'rgba(255, 0, 68, 0.25)', '#ff0044', 2);

    // Wing Cyber Feathers / Energy trails
    this.drawLine(p.wingL1, p.wingL2, '#00f0ff', 2.5);
    this.drawLine(p.wingR1, p.wingR2, '#00f0ff', 2.5);

    // 2. Shoulders & Torso Armor
    this.drawPoly([p.collarL, p.shoulderL, p.chestCore, p.torsoBot], 'rgba(18, 5, 14, 0.85)', 'rgba(255, 0, 68, 0.6)', 1.5);
    this.drawPoly([p.collarR, p.shoulderR, p.chestCore, p.torsoBot], 'rgba(18, 5, 14, 0.85)', 'rgba(255, 0, 68, 0.6)', 1.5);

    // Core Orb Reactor (Glowing Chest Matrix)
    this.ctx.beginPath();
    this.ctx.arc(p.chestCore.x, p.chestCore.y, 16 * p.chestCore.scale, 0, Math.PI * 2);
    this.ctx.fillStyle = '#00f0ff';
    this.ctx.shadowBlur = 25;
    this.ctx.shadowColor = '#00f0ff';
    this.ctx.fill();

    // 3. Mecha Face / Armor Plates
    this.drawPoly([p.crownTop, p.crownL, p.faceL, p.chinL, p.chinTip, p.chinR, p.faceR, p.crownR], 'rgba(14, 3, 10, 0.92)', '#ff0044', 2);

    // Chin Armor Facets
    this.drawLine(p.chinL, p.chinTip, 'rgba(255, 255, 255, 0.6)', 1.5);
    this.drawLine(p.chinR, p.chinTip, 'rgba(255, 255, 255, 0.6)', 1.5);

    // 4. V-Fin Cyber Horns
    this.drawPoly([p.vFinCenter, p.vFinL, p.vFinTipL], 'rgba(255, 0, 68, 0.5)', '#ff0044', 2.5);
    this.drawPoly([p.vFinCenter, p.vFinR, p.vFinTipR], 'rgba(255, 0, 68, 0.5)', '#ff0044', 2.5);

    // 5. Glowing Visor Eyes (Laser Cyan)
    this.ctx.beginPath();
    this.ctx.moveTo(p.visorL.x, p.visorL.y);
    this.ctx.lineTo(p.visorCenter.x, p.visorCenter.y);
    this.ctx.lineTo(p.visorR.x, p.visorR.y);
    this.ctx.lineTo(p.visorBotR.x, p.visorBotR.y);
    this.ctx.lineTo(p.visorCenter.x, p.visorCenter.y + 4);
    this.ctx.lineTo(p.visorBotL.x, p.visorBotL.y);
    this.ctx.closePath();

    this.ctx.fillStyle = '#00f0ff';
    this.ctx.shadowBlur = 20;
    this.ctx.shadowColor = '#00f0ff';
    this.ctx.fill();
    this.ctx.strokeStyle = '#ffffff';
    this.ctx.lineWidth = 1.5;
    this.ctx.stroke();

    this.ctx.restore();
  }

  drawFunnels(rotX, rotY) {
    for (let f of this.funnels) {
      f.angle += f.speed;
      const fx = Math.cos(f.angle) * f.distance;
      const fz = Math.sin(f.angle) * f.distance + 40;
      const fy = f.yOffset + Math.sin(this.time * 2 + f.distance) * 25;

      const pt = this.project(fx, fy, fz, rotX, rotY);

      // Record trail
      f.trail.push({ x: pt.x, y: pt.y, alpha: 1.0 });
      if (f.trail.length > 12) f.trail.shift();

      // Draw Funnel Trail
      for (let t = 0; t < f.trail.length - 1; t++) {
        const t1 = f.trail[t];
        const t2 = f.trail[t + 1];
        this.ctx.beginPath();
        this.ctx.moveTo(t1.x, t1.y);
        this.ctx.lineTo(t2.x, t2.y);
        this.ctx.strokeStyle = `rgba(0, 240, 255, ${(t / f.trail.length) * 0.6})`;
        this.ctx.lineWidth = 2;
        this.ctx.stroke();
      }

      // Draw Funnel Diamond Body
      const size = 12 * pt.scale;
      this.ctx.beginPath();
      this.ctx.moveTo(pt.x, pt.y - size * 1.6);
      this.ctx.lineTo(pt.x + size, pt.y);
      this.ctx.lineTo(pt.x, pt.y + size * 1.6);
      this.ctx.lineTo(pt.x - size, pt.y);
      this.ctx.closePath();

      this.ctx.fillStyle = '#ff0044';
      this.ctx.shadowBlur = 15;
      this.ctx.shadowColor = '#ff0044';
      this.ctx.fill();
      this.ctx.strokeStyle = '#00f0ff';
      this.ctx.lineWidth = 1.5;
      this.ctx.stroke();
    }
  }

  drawCursorHUD() {
    const cx = this.width / 2 + this.mouseX;
    const cy = this.height / 2 + this.mouseY;

    this.ctx.save();
    this.ctx.translate(cx, cy);
    this.ctx.rotate(this.time * 0.6);

    // Crosshair Reticle
    this.ctx.beginPath();
    this.ctx.arc(0, 0, 28, 0, Math.PI * 2);
    this.ctx.strokeStyle = 'rgba(0, 240, 255, 0.45)';
    this.ctx.lineWidth = 1.2;
    this.ctx.setLineDash([8, 6]);
    this.ctx.stroke();

    this.ctx.beginPath();
    this.ctx.moveTo(-36, 0); this.ctx.lineTo(-14, 0);
    this.ctx.moveTo(14, 0); this.ctx.lineTo(36, 0);
    this.ctx.moveTo(0, -36); this.ctx.lineTo(0, -14);
    this.ctx.moveTo(0, 14); this.ctx.lineTo(0, 36);
    this.ctx.strokeStyle = 'rgba(255, 0, 68, 0.6)';
    this.ctx.setLineDash([]);
    this.ctx.stroke();

    this.ctx.restore();
  }

  drawPoly(points, fill, stroke, lineWidth = 1) {
    this.ctx.beginPath();
    this.ctx.moveTo(points[0].x, points[0].y);
    for (let i = 1; i < points.length; i++) {
      this.ctx.lineTo(points[i].x, points[i].y);
    }
    this.ctx.closePath();
    if (fill) {
      this.ctx.fillStyle = fill;
      this.ctx.fill();
    }
    if (stroke) {
      this.ctx.strokeStyle = stroke;
      this.ctx.lineWidth = lineWidth;
      this.ctx.stroke();
    }
  }

  drawLine(p1, p2, color, width = 1) {
    this.ctx.beginPath();
    this.ctx.moveTo(p1.x, p1.y);
    this.ctx.lineTo(p2.x, p2.y);
    this.ctx.strokeStyle = color;
    this.ctx.lineWidth = width;
    this.ctx.stroke();
  }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
  new AnimeMecha3DCanvas('cyberCanvas');
});
