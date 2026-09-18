/**
 * BioRAG KNTT - Enhanced 3D Virtual Science Laboratory Engine
 * Powered by Three.js (r128) & OrbitControls
 * 
 * Provides photorealistic 3D apparatus, interactive controls, Web Audio synthesizer,
 * raycasting interaction, and high-fidelity physics/chemistry simulations for all 20 KHTN experiments.
 */

(function(window) {
  'use strict';

  var Lab3DEngine = {
    container: null,
    scene: null,
    camera: null,
    renderer: null,
    controls: null,
    simGroup: null,
    currentExp: null,
    currentSimType: '',
    animFrameId: null,
    updateFns: [],
    dynamicLights: [],
    interactiveObjects: [],
    raycaster: null,
    mouse: null,
    tooltipEl: null,
    isInitialized: false,
    targetCamPos: null,
    targetLookAt: null,
    audioCtx: null,
    soundEnabled: false,

    // -------------------------------------------------------------------------
    // INITIALIZATION & LIFECYCLE
    // -------------------------------------------------------------------------
    init: function(container, exp, state) {
      if (!container || typeof THREE === 'undefined') {
        console.warn('[Lab3DEngine] THREE is not loaded or container missing.');
        return false;
      }

      this.destroy();

      this.container = container;
      this.currentExp = exp;
      this.currentSimType = (exp && exp.simulation ? exp.simulation.sim_type : '') || (exp && exp.simulation_type ? exp.simulation_type : '') || '';
      this.currentSimState = state || window.labSimState || {};
      window.labSimState = this.currentSimState;

      var width = container.clientWidth || 640;
      var height = container.clientHeight || 390;

      // 1. Scene setup
      this.scene = new THREE.Scene();
      this.scene.background = new THREE.Color(0x0a101d);
      this.scene.fog = new THREE.FogExp2(0x0a101d, 0.028);

      // 2. Perspective Camera
      this.camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 100);

      // 3. WebGL Renderer
      this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
      this.renderer.setSize(width, height);
      this.renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
      this.renderer.shadowMap.enabled = true;
      this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      this.renderer.toneMapping = THREE.ACESFilmicToneMapping;
      this.renderer.toneMappingExposure = 1.15;

      container.innerHTML = '';
      container.appendChild(this.renderer.domElement);

      // 4. OrbitControls
      if (typeof THREE.OrbitControls !== 'undefined') {
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.08;
        this.controls.maxPolarAngle = Math.PI / 2 - 0.02;
        this.controls.minDistance = 0.4;
        this.controls.maxDistance = 25;
      }

      // 5. Studio Environment & Lighting
      this.initEnvironment();

      // 6. Interactive Raycasting & Tooltip
      this.initRaycaster();

      // 7. Build 3D apparatus
      this.simGroup = new THREE.Group();
      this.scene.add(this.simGroup);
      this.updateFns = [];
      this.dynamicLights = [];

      this.buildSimulationApparatus(this.currentSimType, state || {});

      // 8. Set initial camera & controls target after everything is ready
      this.setDefaultCameraPosition();

      this.isInitialized = true;

      this._onResize = this.resize.bind(this);
      window.addEventListener('resize', this._onResize);

      this.startLoop();
      return true;
    },

    setDefaultCameraPosition: function() {
      if (!this.camera) return;
      var st = this.currentSimType;
      if (st === 'filtration_evaporation') {
        var stage = (window.labSimState && window.labSimState.stage) || 1;
        if (stage === 1) {
          this.camera.position.set(-1.4, 1.8, 2.8);
          if (this.controls) this.controls.target.set(-1.4, 1.2, 0);
        } else {
          this.camera.position.set(1.4, 1.9, 2.8);
          if (this.controls) this.controls.target.set(1.4, 1.3, 0);
        }
      } else if (st === 'atomic_structure' || st === 'molecule_bonding') {
        this.camera.position.set(0, 1.6, 3.4);
        if (this.controls) this.controls.target.set(0, 1.2, 0);
      } else if (st === 'circuit_ohm') {
        this.camera.position.set(0, 2.4, 3.2);
        if (this.controls) this.controls.target.set(0, 0.5, 0);
      } else if (st === 'spring_stretch') {
        this.camera.position.set(0.05, 2.05, 2.45);
        if (this.controls) this.controls.target.set(-0.08, 2.0, 0);
      } else if (st === 'mass_conservation') {
        this.camera.position.set(0, 1.5, 2.5);
        if (this.controls) this.controls.target.set(0, 0.85, 0);
      } else if (st === 'acid_base_neutralization') {
        this.camera.position.set(0, 1.8, 2.8);
        if (this.controls) this.controls.target.set(0, 1.3, 0);
      } else if (st === 'metal_acid') {
        this.camera.position.set(0, 1.4, 2.6);
        if (this.controls) this.controls.target.set(0, 0.8, 0);
      } else if (st === 'ph_indicator') {
        this.camera.position.set(0, 1.4, 2.6);
        if (this.controls) this.controls.target.set(0, 0.8, 0);
      } else if (st === 'lever_balance') {
        this.camera.position.set(0, 1.8, 3.5);
        if (this.controls) this.controls.target.set(0, 1.35, 0);
      } else if (st === 'liquid_pressure') {
        this.camera.position.set(0.1, 1.6, 2.8);
        if (this.controls) this.controls.target.set(0, 1.15, 0);
      } else if (st === 'metal_displacement') {
        this.camera.position.set(0, 1.25, 2.1);
        if (this.controls) this.controls.target.set(0, 0.7, 0);
      } else if (st === 'light_refraction' || st === 'light_reflection') {
        this.camera.position.set(0, 2.4, 3.0);
        if (this.controls) this.controls.target.set(0, 0.5, 0);
      } else if (st === 'air_oxygen_fraction') {
        this.camera.position.set(0, 1.35, 2.3);
        if (this.controls) this.controls.target.set(0, 0.7, 0);
      } else if (st === 'hydrocarbon_bromine') {
        this.camera.position.set(0, 1.35, 2.5);
        if (this.controls) this.controls.target.set(0, 0.8, 0);
      } else if (st === 'friction_force') {
        this.camera.position.set(0, 1.5, 2.9);
        if (this.controls) this.controls.target.set(0, 0.5, 0);
      } else {
        this.camera.position.set(0, 1.8, 3.2);
        if (this.controls) this.controls.target.set(0, 1.1, 0);
      }
      if (this.controls) this.controls.update();
    },

    captureScreenshot: function() {
      if (!this.renderer || !this.scene || !this.camera) return null;
      this.renderer.render(this.scene, this.camera);
      return this.renderer.domElement.toDataURL('image/png');
    },

    // -------------------------------------------------------------------------
    // AUDIO SYNTHESIZER
    // -------------------------------------------------------------------------
    playDripSound: function() {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var ctx = this.audioCtx;
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(900 + Math.random() * 200, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(320, ctx.currentTime + 0.08);
        gain.gain.setValueAtTime(0.18, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.08);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.09);
      } catch(e) {}
    },

    playBoilSound: function() {
      if (!this.soundEnabled || Math.random() > 0.12) return;
      try {
        if (!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var ctx = this.audioCtx;
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(260 + Math.random() * 120, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(460, ctx.currentTime + 0.06);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.06);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.07);
      } catch(e) {}
    },

    playSwitchSound: function() {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var ctx = this.audioCtx;
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(1400, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(90, ctx.currentTime + 0.04);
        gain.gain.setValueAtTime(0.25, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.04);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.05);
      } catch(e) {}
    },

    playPopSound: function() {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var ctx = this.audioCtx;
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(360, ctx.currentTime);
        osc.frequency.exponentialRampToValueAtTime(60, ctx.currentTime + 0.12);
        gain.gain.setValueAtTime(0.3, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.12);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.13);
      } catch(e) {}
    },

    playBellSound: function() {
      if (!this.soundEnabled) return;
      try {
        if (!this.audioCtx) this.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        var ctx = this.audioCtx;
        var osc1 = ctx.createOscillator();
        var osc2 = ctx.createOscillator();
        var gain = ctx.createGain();
        osc1.type = 'sine';
        osc2.type = 'sine';
        osc1.frequency.setValueAtTime(880, ctx.currentTime);
        osc2.frequency.setValueAtTime(1760, ctx.currentTime);
        gain.gain.setValueAtTime(0.2, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
        osc1.connect(gain);
        osc2.connect(gain);
        gain.connect(ctx.destination);
        osc1.start();
        osc2.start();
        osc1.stop(ctx.currentTime + 0.45);
        osc2.stop(ctx.currentTime + 0.45);
      } catch(e) {}
    },

    resetCamera: function() {
      if (this.currentSimType === 'filtration_evaporation') {
        this.camera.position.set(0, 2.4, 5.0);
        if (this.controls) {
          this.controls.target.set(0, 1.2, 0);
          this.controls.update();
        }
      } else {
        this.setDefaultCameraPosition();
      }
    },

    focusOnStage: function(stageNum) {
      if (!this.camera || !this.controls) return;
      if (stageNum === 1) {
        this.targetCamPos = new THREE.Vector3(-1.4, 2.0, 3.4);
        this.targetLookAt = new THREE.Vector3(-1.4, 1.2, 0);
      } else {
        this.targetCamPos = new THREE.Vector3(1.4, 2.1, 3.4);
        this.targetLookAt = new THREE.Vector3(1.4, 1.3, 0);
      }
    },

    // -------------------------------------------------------------------------
    // RAYCASTER & DIRECT 3D INTERACTION
    // -------------------------------------------------------------------------
    initRaycaster: function() {
      var self = this;
      this.raycaster = new THREE.Raycaster();
      this.mouse = new THREE.Vector2();
      this.interactiveObjects = [];

      // Create floating tooltip badge
      if (this.container) {
        this.tooltipEl = document.createElement('div');
        this.tooltipEl.style.position = 'absolute';
        this.tooltipEl.style.pointerEvents = 'none';
        this.tooltipEl.style.background = 'rgba(15, 23, 42, 0.88)';
        this.tooltipEl.style.color = '#38bdf8';
        this.tooltipEl.style.padding = '4px 10px';
        this.tooltipEl.style.borderRadius = '6px';
        this.tooltipEl.style.fontSize = '12px';
        this.tooltipEl.style.fontWeight = '600';
        this.tooltipEl.style.border = '1px solid rgba(56, 189, 248, 0.4)';
        this.tooltipEl.style.boxShadow = '0 4px 12px rgba(0,0,0,0.4)';
        this.tooltipEl.style.display = 'none';
        this.tooltipEl.style.zIndex = '100';
        this.container.appendChild(this.tooltipEl);
      }

      this._onPointerMove = function(e) {
        if (!self.renderer || !self.camera || self.interactiveObjects.length === 0) return;
        var rect = self.renderer.domElement.getBoundingClientRect();
        self.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        self.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        self.raycaster.setFromCamera(self.mouse, self.camera);
        var intersects = self.raycaster.intersectObjects(self.interactiveObjects, true);

        if (intersects.length > 0) {
          self.renderer.domElement.style.cursor = 'pointer';
          var topObj = intersects[0].object;
          while (topObj && !topObj.userData.hint && topObj.parent && topObj.parent !== self.simGroup) {
            topObj = topObj.parent;
          }
          if (topObj && topObj.userData && topObj.userData.hint && self.tooltipEl) {
            self.tooltipEl.textContent = topObj.userData.hint;
            self.tooltipEl.style.display = 'block';
            self.tooltipEl.style.left = Math.min(rect.width - 160, e.clientX - rect.left + 14) + 'px';
            self.tooltipEl.style.top = Math.max(10, e.clientY - rect.top - 28) + 'px';
          }
        } else {
          self.renderer.domElement.style.cursor = 'default';
          if (self.tooltipEl) self.tooltipEl.style.display = 'none';
        }
      };

      this._onPointerDown = function(e) {
        if (!self.renderer || !self.camera || self.interactiveObjects.length === 0) return;
        var rect = self.renderer.domElement.getBoundingClientRect();
        self.mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
        self.mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;
        self.raycaster.setFromCamera(self.mouse, self.camera);
        var intersects = self.raycaster.intersectObjects(self.interactiveObjects, true);

        if (intersects.length > 0) {
          var hitObj = intersects[0].object;
          while (hitObj && !hitObj.userData.onClick && hitObj.parent && hitObj.parent !== self.simGroup) {
            hitObj = hitObj.parent;
          }
          if (hitObj && hitObj.userData && typeof hitObj.userData.onClick === 'function') {
            hitObj.userData.onClick(window.labSimState || {}, self);
          }
        }
      };

      this.renderer.domElement.addEventListener('mousemove', this._onPointerMove);
      this.renderer.domElement.addEventListener('click', this._onPointerDown);
    },

    registerInteractive: function(object, hint, onClick) {
      if (!object) return;
      object.userData = object.userData || {};
      object.userData.hint = hint;
      object.userData.onClick = onClick;
      this.interactiveObjects.push(object);
    },

    // -------------------------------------------------------------------------
    // STUDIO ENVIRONMENT & LIGHTING
    // -------------------------------------------------------------------------
    initEnvironment: function() {
      var ambLight = new THREE.AmbientLight(0xdbeafe, 0.75);
      this.scene.add(ambLight);

      var keyLight = new THREE.DirectionalLight(0xffffff, 0.95);
      keyLight.position.set(5, 10, 6);
      keyLight.castShadow = true;
      keyLight.shadow.mapSize.width = 1024;
      keyLight.shadow.mapSize.height = 1024;
      keyLight.shadow.camera.near = 0.5;
      keyLight.shadow.camera.far = 25;
      keyLight.shadow.camera.left = -6;
      keyLight.shadow.camera.right = 6;
      keyLight.shadow.camera.top = 6;
      keyLight.shadow.camera.bottom = -6;
      keyLight.shadow.bias = -0.001;
      this.scene.add(keyLight);

      var rimLight = new THREE.DirectionalLight(0x38bdf8, 0.45);
      rimLight.position.set(-6, 6, -5);
      this.scene.add(rimLight);

      var fillLight = new THREE.DirectionalLight(0xfef08a, 0.3);
      fillLight.position.set(4, 5, -3);
      this.scene.add(fillLight);

      var tableGeo = new THREE.BoxGeometry(16, 0.3, 11);
      var tableMat = new THREE.MeshStandardMaterial({
        color: 0x111827,
        roughness: 0.4,
        metalness: 0.1
      });
      var table = new THREE.Mesh(tableGeo, tableMat);
      table.position.set(0, -0.15, 0);
      table.receiveShadow = true;
      this.scene.add(table);

      var grid = new THREE.GridHelper(14, 28, 0x1e293b, 0x0f172a);
      grid.position.set(0, 0.005, 0);
      this.scene.add(grid);
    },

    // -------------------------------------------------------------------------
    // MATERIAL FACTORIES
    // -------------------------------------------------------------------------
    getGlassMaterial: function(tintColor, opacity) {
      tintColor = tintColor || 0xdbeafe;
      opacity = opacity !== undefined ? opacity : 0.32;
      return new THREE.MeshPhysicalMaterial ? new THREE.MeshPhysicalMaterial({
        color: tintColor,
        transparent: true,
        opacity: opacity,
        roughness: 0.05,
        metalness: 0.05,
        transmission: 0.85,
        ior: 1.52,
        clearcoat: 1.0,
        clearcoatRoughness: 0.05,
        depthWrite: false,
        side: THREE.DoubleSide
      }) : new THREE.MeshStandardMaterial({
        color: tintColor,
        transparent: true,
        opacity: opacity,
        roughness: 0.1,
        metalness: 0.1,
        side: THREE.DoubleSide
      });
    },

    getLiquidMaterial: function(colorHex, opacity) {
      return new THREE.MeshStandardMaterial({
        color: colorHex !== undefined ? colorHex : 0x0284c7,
        transparent: true,
        opacity: opacity !== undefined ? opacity : 0.82,
        roughness: 0.1,
        metalness: 0.05,
        side: THREE.DoubleSide
      });
    },

    getMetalMaterial: function(roughness, colorHex) {
      return new THREE.MeshStandardMaterial({
        color: colorHex !== undefined ? colorHex : 0x94a3b8,
        roughness: roughness !== undefined ? roughness : 0.35,
        metalness: 0.85
      });
    },

    // -------------------------------------------------------------------------
    // 3D APPARATUS BUILDERS ROUTER
    // -------------------------------------------------------------------------
    buildSimulationApparatus: function(simType, state) {
      var group = this.simGroup;

      if (simType === 'filtration_evaporation') {
        this.buildFiltrationEvaporation(group, state);
      } else if (simType === 'atomic_structure') {
        this.buildAtomicStructure(group, state);
      } else if (simType === 'molecule_bonding') {
        this.buildMoleculeBonding(group, state);
      } else if (simType === 'magnetic_field') {
        this.buildMagneticField(group, state);
      } else if (simType === 'circuit_ohm') {
        this.buildCircuitOhm(group, state);
      } else if (simType === 'spring_stretch') {
        this.buildSpringStretch(group, state);
      } else if (simType === 'archimedes') {
        this.buildArchimedes(group, state);
      } else if (simType === 'lens_convex') {
        this.buildLensConvex(group, state);
      } else if (simType === 'light_reflection') {
        this.buildLightReflection(group, state);
      } else if (simType === 'mass_conservation') {
        this.buildMassConservation(group, state);
      } else if (simType === 'acid_base_neutralization') {
        this.buildAcidBaseNeutralization(group, state);
      } else if (simType === 'metal_acid') {
        this.buildMetalAcid(group, state);
      } else if (simType === 'ph_indicator') {
        this.buildPhIndicator(group, state);
      } else if (simType === 'lever_balance') {
        this.buildLeverBalance(group, state);
      } else if (simType === 'liquid_pressure') {
        this.buildLiquidPressure(group, state);
      } else if (simType === 'metal_displacement') {
        this.buildMetalDisplacement(group, state);
      } else if (simType === 'light_refraction') {
        this.buildLightRefraction(group, state);
      } else if (simType === 'air_oxygen_fraction') {
        this.buildAirOxygenFraction(group, state);
      } else if (simType === 'hydrocarbon_bromine') {
        this.buildHydrocarbonBromine(group, state);
      } else if (simType === 'friction_force') {
        this.buildFrictionForce(group, state);
      } else {
        this.buildUniversalLabStand(group, simType, state);
      }
    },

    // =========================================================================
    // 1. FILTRATION & EVAPORATION (Tách muối ăn khỏi cát và nước)
    // =========================================================================
    buildFiltrationEvaporation: function(group, state) {
      var self = this;
      var ironMat = this.getMetalMaterial(0.4, 0x334155);
      var glassMat = this.getGlassMaterial(0xdbeafe, 0.28);

      // STAGE 1: Filtration Stand (left side at x = -1.4)
      var s1Group = new THREE.Group();
      s1Group.position.set(-1.4, 0, 0);

      var base1 = new THREE.Mesh(new THREE.BoxGeometry(1.4, 0.12, 1.2), ironMat);
      base1.position.set(0, 0.06, 0);
      base1.castShadow = true;
      s1Group.add(base1);

      var rod1 = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 3.2, 16), ironMat);
      rod1.position.set(-0.45, 1.66, -0.35);
      rod1.castShadow = true;
      s1Group.add(rod1);

      var clamp1 = new THREE.Mesh(new THREE.BoxGeometry(0.55, 0.07, 0.07), ironMat);
      clamp1.position.set(-0.2, 1.95, -0.35);
      s1Group.add(clamp1);

      var ring1 = new THREE.Mesh(new THREE.TorusGeometry(0.38, 0.03, 16, 32), ironMat);
      ring1.rotation.x = Math.PI / 2;
      ring1.position.set(0, 1.95, 0);
      s1Group.add(ring1);

      // Glass Funnel
      var funnelGroup = new THREE.Group();
      funnelGroup.position.set(0, 1.95, 0);

      var coneMesh = new THREE.Mesh(new THREE.ConeGeometry(0.38, 0.55, 32, 1, true), glassMat);
      coneMesh.rotation.x = Math.PI;
      coneMesh.position.set(0, -0.05, 0);
      funnelGroup.add(coneMesh);

      var stemMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.75, 16, 1, true), glassMat);
      stemMesh.position.set(0, -0.68, 0);
      funnelGroup.add(stemMesh);

      // Filter Paper Cone (4-layer folded filter paper)
      var paperMat = new THREE.MeshStandardMaterial({
        color: 0xf1f5f9,
        roughness: 0.88,
        side: THREE.DoubleSide
      });
      var paperMesh = new THREE.Mesh(new THREE.ConeGeometry(0.35, 0.48, 28), paperMat);
      paperMesh.rotation.x = Math.PI;
      paperMesh.position.set(0, -0.04, 0);
      funnelGroup.add(paperMesh);

      // Sand Particles inside filter paper (golden-brown SiO2)
      var sandMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.95 });
      var sandGroup = new THREE.Group();
      sandGroup.position.set(0, -0.15, 0);
      for (var sp = 0; sp < 45; sp++) {
        var sRad = Math.random() * 0.22;
        var sAng = Math.random() * Math.PI * 2;
        var sMesh = new THREE.Mesh(new THREE.DodecahedronGeometry(0.02 + Math.random() * 0.025), sandMat);
        sMesh.position.set(Math.cos(sAng) * sRad, (Math.random() - 0.5) * 0.05, Math.sin(sAng) * sRad);
        sandGroup.add(sMesh);
      }
      funnelGroup.add(sandGroup);
      s1Group.add(funnelGroup);

      // Receiving Beaker below (catching clear salt water)
      var beakerMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 0.95, 32, 1, true), glassMat);
      beakerMesh.position.set(0, 0.60, 0);
      beakerMesh.castShadow = true;
      s1Group.add(beakerMesh);

      // Filtered liquid level in beaker
      var beakerLiqMat = this.getLiquidMaterial(0x38bdf8, 0.55);
      var beakerLiq = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.52, 32), beakerLiqMat);
      beakerLiq.position.set(0, 0.38, 0);
      s1Group.add(beakerLiq);

      // Dripping Droplet from funnel stem
      var dropGeo = new THREE.SphereGeometry(0.032, 12, 12);
      dropGeo.scale(1, 1.5, 1);
      var dropMesh = new THREE.Mesh(dropGeo, beakerLiqMat);
      dropMesh.position.set(0, 1.25, 0);
      s1Group.add(dropMesh);

      // Surface Ripple
      var rippleGeo = new THREE.RingGeometry(0.04, 0.28, 24);
      var rippleMat = new THREE.MeshBasicMaterial({ color: 0xbae6fd, transparent: true, opacity: 0, side: THREE.DoubleSide });
      var rippleMesh = new THREE.Mesh(rippleGeo, rippleMat);
      rippleMesh.rotation.x = -Math.PI / 2;
      rippleMesh.position.set(0, 0.642, 0);
      s1Group.add(rippleMesh);

      // Animated Dripping Loop
      var dripY = 1.25;
      this.updateFns.push(function(st, t) {
        var activeStage = (st && st.stage !== undefined) ? st.stage : 1;
        if (activeStage === 1) {
          dropMesh.visible = true;
          dripY -= 0.028;
          if (dripY < 0.65) {
            dripY = 1.25;
            rippleMat.opacity = 0.85;
            self.playDripSound();
          }
          dropMesh.position.y = dripY;
          if (rippleMat.opacity > 0) {
            rippleMat.opacity -= 0.035;
          }
        } else {
          dropMesh.visible = false;
          rippleMat.opacity = 0;
        }
      });

      group.add(s1Group);

      // STAGE 2: Evaporation Stand (right side at x = 1.4)
      var s2Group = new THREE.Group();
      s2Group.position.set(1.4, 0, 0);

      var tripodRing = new THREE.Mesh(new THREE.TorusGeometry(0.55, 0.04, 16, 32), ironMat);
      tripodRing.rotation.x = Math.PI / 2;
      tripodRing.position.set(0, 1.25, 0);
      tripodRing.castShadow = true;
      s2Group.add(tripodRing);

      for (var legIdx = 0; legIdx < 3; legIdx++) {
        var angle = (legIdx * 2 * Math.PI) / 3;
        var leg = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 1.35, 16), ironMat);
        var legR = 0.52;
        leg.position.set(Math.cos(angle) * legR, 0.62, Math.sin(angle) * legR);
        leg.rotation.z = -Math.cos(angle) * 0.18;
        leg.rotation.x = Math.sin(angle) * 0.18;
        leg.castShadow = true;
        s2Group.add(leg);
      }

      var gauze = new THREE.Mesh(new THREE.PlaneGeometry(1.0, 1.0, 16, 16), new THREE.MeshStandardMaterial({ color: 0x94a3b8, wireframe: true, roughness: 0.7 }));
      gauze.rotation.x = -Math.PI / 2;
      gauze.position.set(0, 1.29, 0);
      s2Group.add(gauze);

      var circleAmiang = new THREE.Mesh(new THREE.CircleGeometry(0.36, 32), new THREE.MeshStandardMaterial({ color: 0xd1d5db, roughness: 0.9 }));
      circleAmiang.rotation.x = -Math.PI / 2;
      circleAmiang.position.set(0, 1.292, 0);
      s2Group.add(circleAmiang);

      // Porcelain Evaporating Dish (Bát sứ tráng men chịu nhiệt)
      var porcelainMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.15, metalness: 0.05, side: THREE.DoubleSide });
      var dishPoints = [
        new THREE.Vector2(0.001, 0.00), new THREE.Vector2(0.25, 0.01), new THREE.Vector2(0.38, 0.05),
        new THREE.Vector2(0.52, 0.15), new THREE.Vector2(0.66, 0.32), new THREE.Vector2(0.72, 0.44),
        new THREE.Vector2(0.75, 0.47), new THREE.Vector2(0.73, 0.47), new THREE.Vector2(0.64, 0.31),
        new THREE.Vector2(0.50, 0.15), new THREE.Vector2(0.36, 0.05), new THREE.Vector2(0.22, 0.02),
        new THREE.Vector2(0.001, 0.015)
      ];
      var porcelainDish = new THREE.Mesh(new THREE.LatheGeometry(dishPoints, 40), porcelainMat);
      porcelainDish.position.set(0, 1.295, 0);
      porcelainDish.castShadow = true;
      s2Group.add(porcelainDish);

      // Liquid in Dish
      var dishLiqMat = this.getLiquidMaterial(0x38bdf8, 0.75);
      var dishLiq = new THREE.Mesh(new THREE.CircleGeometry(0.58, 36), dishLiqMat);
      dishLiq.rotation.x = -Math.PI / 2;
      dishLiq.position.set(0, 1.48, 0);
      s2Group.add(dishLiq);

      // White Salt Crystals (Tinh thể muối ăn NaCl)
      var saltGroup = new THREE.Group();
      saltGroup.position.set(0, 1.32, 0);
      var saltMat = new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.2, metalness: 0.15 });
      for (var s = 0; s < 60; s++) {
        var sAng = Math.random() * Math.PI * 2;
        var sRad = Math.random() * 0.46;
        var cSize = 0.025 + Math.random() * 0.04;
        var crystal = new THREE.Mesh(new THREE.BoxGeometry(cSize, cSize, cSize), saltMat);
        crystal.position.set(Math.cos(sAng) * sRad, 0.01 + Math.random() * 0.025, Math.sin(sAng) * sRad);
        crystal.rotation.set(Math.random() * Math.PI, Math.random() * Math.PI, 0);
        saltGroup.add(crystal);
      }
      saltGroup.scale.set(0.01, 0.01, 0.01);
      s2Group.add(saltGroup);

      // Alcohol Lamp (Đèn cồn)
      var lampGroup = new THREE.Group();
      lampGroup.position.set(0, 0, 0);

      var lampBody = new THREE.Mesh(new THREE.SphereGeometry(0.38, 24, 20), this.getGlassMaterial(0xc7d2fe, 0.4));
      lampBody.position.set(0, 0.36, 0);
      lampBody.scale.set(1.15, 0.85, 1.15);
      lampGroup.add(lampBody);

      var alcoholLiq = new THREE.Mesh(new THREE.SphereGeometry(0.35, 20, 16), this.getLiquidMaterial(0x818cf8, 0.45));
      alcoholLiq.position.set(0, 0.32, 0);
      alcoholLiq.scale.set(1.12, 0.72, 1.12);
      lampGroup.add(alcoholLiq);

      var collar = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.14, 0.16, 20), this.getMetalMaterial(0.25, 0xd97706));
      collar.position.set(0, 0.70, 0);
      lampGroup.add(collar);

      var wick = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.18, 12), new THREE.MeshStandardMaterial({ color: 0x475569 }));
      wick.position.set(0, 0.82, 0);
      lampGroup.add(wick);

      // Flame with Dual Colors (Lõi xanh & Vỏ vàng cam)
      var flameGroup = new THREE.Group();
      flameGroup.position.set(0, 0.92, 0);

      var flameInner = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.22, 16), new THREE.MeshBasicMaterial({ color: 0x60a5fa, transparent: true, opacity: 0.9 }));
      flameGroup.add(flameInner);

      var flameOuter = new THREE.Mesh(new THREE.ConeGeometry(0.11, 0.42, 16), new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.82 }));
      flameGroup.add(flameOuter);

      var flameLight = new THREE.PointLight(0xf59e0b, 1.8, 4.0);
      flameLight.position.set(0, 0.2, 0);
      flameGroup.add(flameLight);
      lampGroup.add(flameGroup);

      self.registerInteractive(lampBody, 'Đèn cồn: Nhấp chuột để Bật/Tắt lửa', function(st) {
        st.burner = (st.burner === 0 || !st.burner) ? 2 : 0;
        self.playSwitchSound();
      });
      s2Group.add(lampGroup);

      // Boiling Bubbles & Steam
      var bubbleGroup = new THREE.Group();
      bubbleGroup.position.set(0, 1.48, 0);
      var bubbles = [];
      var bMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 });
      for (var b = 0; b < 20; b++) {
        var bMesh = new THREE.Mesh(new THREE.SphereGeometry(0.02 + Math.random() * 0.03, 8, 8), bMat);
        bMesh.position.set((Math.random() - 0.5) * 0.52, 0, (Math.random() - 0.5) * 0.52);
        bubbleGroup.add(bMesh);
        bubbles.push({ mesh: bMesh, speed: 0.012 + Math.random() * 0.025 });
      }
      s2Group.add(bubbleGroup);

      // Evaporation loop hook
      var evapProgress = 0;
      this.updateFns.push(function(st, t) {
        var activeStage = (st && st.stage !== undefined) ? st.stage : 1;
        var burnerLvl = (st && st.burner !== undefined) ? st.burner : (activeStage === 2 ? 2 : 0);

        if (activeStage === 1) {
          evapProgress = 0;
        } else if (activeStage === 2 && burnerLvl > 0) {
          evapProgress = Math.min(1.0, evapProgress + 0.0025 * burnerLvl);
        }

        if (burnerLvl > 0 && activeStage === 2) {
          flameGroup.visible = true;
          var flicker = 1.0 + Math.sin(t * 18) * 0.12 + Math.cos(t * 31) * 0.08;
          flameGroup.scale.set(flicker, flicker * 1.1, flicker);
          flameLight.intensity = (burnerLvl === 1 ? 1.0 : 2.2) * flicker;

          bubbleGroup.visible = (evapProgress < 0.95);
          bubbles.forEach(function(bObj) {
            bObj.mesh.position.y += bObj.speed;
            if (bObj.mesh.position.y > 0.10) bObj.mesh.position.y = 0;
          });
          self.playBoilSound();
        } else {
          flameGroup.visible = false;
          flameLight.intensity = 0;
          bubbleGroup.visible = false;
        }

        var liqScale = Math.max(0.001, 1.0 - evapProgress);
        dishLiq.scale.set(liqScale, liqScale, liqScale);
        dishLiq.position.y = 1.34 + 0.14 * liqScale;
        dishLiq.visible = (evapProgress < 0.98);

        var saltScale = Math.min(1.0, evapProgress * 1.35);
        saltGroup.scale.set(saltScale, saltScale, saltScale);
      });

      group.add(s2Group);
    },

    buildAtomicStructure: function(group, state) {
      var self = this;
      var aGroup = new THREE.Group();
      aGroup.position.set(0, 1.3, 0);

      var nucMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.3, metalness: 0.2 });
      var neuMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4, metalness: 0.1 });
      var elecMat = new THREE.MeshStandardMaterial({ color: 0x38bdf8, roughness: 0.1, emissive: 0x0284c7, emissiveIntensity: 0.6 });

      // Nucleus
      var nucleusGroup = new THREE.Group();
      var pCoords = [
        [0, 0, 0], [0.12, 0.1, 0.08], [-0.1, -0.08, 0.12], [0.08, -0.12, -0.1],
        [-0.12, 0.1, -0.08], [0.1, 0.08, -0.12], [-0.08, -0.1, -0.12]
      ];
      pCoords.forEach(function(c, i) {
        var sphere = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), (i % 2 === 0) ? nucMat : neuMat);
        sphere.position.set(c[0], c[1], c[2]);
        nucleusGroup.add(sphere);
      });
      aGroup.add(nucleusGroup);

      // Electron Shells (K, L, M)
      var shellsData = [
        { radius: 1.1, count: 2, speed: 1.8 },
        { radius: 1.8, count: 8, speed: 1.2 },
        { radius: 2.5, count: 1, speed: 0.8 }
      ];

      var shellMeshes = [];
      shellsData.forEach(function(sh, sIdx) {
        var ringMat = new THREE.MeshBasicMaterial({ color: 0x475569, transparent: true, opacity: 0.45 });
        var ring = new THREE.Mesh(new THREE.RingGeometry(sh.radius - 0.015, sh.radius + 0.015, 64), ringMat);
        ring.rotation.x = Math.PI / 2;
        aGroup.add(ring);

        var electrons = [];
        for (var e = 0; e < sh.count; e++) {
          var eMesh = new THREE.Mesh(new THREE.SphereGeometry(0.07, 16, 16), elecMat);
          aGroup.add(eMesh);
          electrons.push({ mesh: eMesh, phase: (e * 2 * Math.PI) / sh.count });
        }
        shellMeshes.push({ radius: sh.radius, speed: sh.speed, electrons: electrons });
      });

      this.updateFns.push(function(st, t) {
        nucleusGroup.rotation.y = t * 0.5;
        shellMeshes.forEach(function(shItem) {
          shItem.electrons.forEach(function(eItem) {
            var ang = eItem.phase + t * shItem.speed;
            eItem.mesh.position.set(Math.cos(ang) * shItem.radius, 0, Math.sin(ang) * shItem.radius);
          });
        });
      });

      group.add(aGroup);
    },

    // =========================================================================
    // 3. MOLECULE BONDING (Mô hình phân tử CPK)
    // =========================================================================
    buildMoleculeBonding: function(group, state) {
      var self = this;
      var molGroup = new THREE.Group();
      molGroup.position.set(0, 1.3, 0);

      var cMat = new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3 });
      var hMat = new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.2 });
      var bondMat = new THREE.MeshStandardMaterial({ color: 0x94a3b8, roughness: 0.4, metalness: 0.5 });

      function createBond(p1, p2, radius) {
        radius = radius || 0.06;
        var dir = new THREE.Vector3().subVectors(p2, p1);
        var len = dir.length();
        var bond = new THREE.Mesh(new THREE.CylinderGeometry(radius, radius, len, 16), bondMat);
        bond.position.copy(p1).addScaledVector(dir, 0.5);
        bond.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), dir.clone().normalize());
        return bond;
      }

      // Methane CH4 Tetrahedron
      var cPos = new THREE.Vector3(0, 0, 0);
      var cSphere = new THREE.Mesh(new THREE.SphereGeometry(0.46, 32, 32), cMat);
      molGroup.add(cSphere);

      var d = 0.95;
      var hCoords = [
        new THREE.Vector3(d, d, d).normalize().multiplyScalar(1.2),
        new THREE.Vector3(-d, -d, d).normalize().multiplyScalar(1.2),
        new THREE.Vector3(-d, d, -d).normalize().multiplyScalar(1.2),
        new THREE.Vector3(d, -d, -d).normalize().multiplyScalar(1.2)
      ];

      hCoords.forEach(function(hPos) {
        var hSphere = new THREE.Mesh(new THREE.SphereGeometry(0.26, 24, 24), hMat);
        hSphere.position.copy(hPos);
        molGroup.add(hSphere);
        molGroup.add(createBond(cPos, hPos, 0.07));
      });

      this.updateFns.push(function(st, t) {
        molGroup.rotation.y = t * 0.6;
        molGroup.rotation.x = Math.sin(t * 0.4) * 0.2;
      });

      group.add(molGroup);
    },

    // =========================================================================
    // 4. MAGNETIC FIELD (Từ trường nam châm)
    // =========================================================================
    buildMagneticField: function(group, state) {
      var self = this;
      var magGroup = new THREE.Group();
      magGroup.position.set(0, 0.8, 0);

      // Bar Magnet
      var nMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.3 });
      var sMat = new THREE.MeshStandardMaterial({ color: 0x3b82f6, roughness: 0.3 });

      var nPole = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.35, 0.6), nMat);
      nPole.position.set(0.6, 0, 0);
      magGroup.add(nPole);

      var sPole = new THREE.Mesh(new THREE.BoxGeometry(1.2, 0.35, 0.6), sMat);
      sPole.position.set(-0.6, 0, 0);
      magGroup.add(sPole);

      // Compasses grid
      var compassPositions = [
        [-1.6, 0, 1.2], [-0.8, 0, 1.4], [0, 0, 1.5], [0.8, 0, 1.4], [1.6, 0, 1.2],
        [-1.6, 0, -1.2], [-0.8, 0, -1.4], [0, 0, -1.5], [0.8, 0, -1.4], [1.6, 0, -1.2],
        [1.8, 0, 0], [-1.8, 0, 0]
      ];

      var compassNeedles = [];
      compassPositions.forEach(function(pos) {
        var baseC = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.04, 24), new THREE.MeshStandardMaterial({ color: 0x1e293b }));
        baseC.position.set(pos[0], 0, pos[2]);
        magGroup.add(baseC);

        var nGroup = new THREE.Group();
        nGroup.position.set(pos[0], 0.04, pos[2]);

        var needleN = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.22, 8), nMat);
        needleN.rotation.x = Math.PI / 2;
        needleN.position.z = 0.11;
        nGroup.add(needleN);

        var needleS = new THREE.Mesh(new THREE.ConeGeometry(0.06, 0.22, 8), sMat);
        needleS.rotation.x = -Math.PI / 2;
        needleS.position.z = -0.11;
        nGroup.add(needleS);

        magGroup.add(nGroup);
        compassNeedles.push({ group: nGroup, pos: pos });
      });

      this.updateFns.push(function(st, t) {
        var str = (st && st.fieldStrength !== undefined) ? (st.fieldStrength / (st.fieldStrength > 5 ? 100 : 1)) : 1.0;
        var showC = (st && st.showCompass !== undefined) ? st.showCompass : ((st && st.showCompasses !== undefined) ? st.showCompasses : true);
        compassNeedles.forEach(function(cmp, idx) {
          cmp.group.visible = !!showC;
          var p = cmp.pos;
          var angle = Math.atan2(p[2], p[0] - 0.6) - Math.atan2(p[2], p[0] + 0.6);
          var wobble = Math.sin(t * 3.5 + idx) * 0.08 * (1.2 - Math.min(1.0, str * 0.5));
          cmp.group.rotation.y = (angle * 0.5 + Math.PI / 2) * str + wobble;
        });
      });

      group.add(magGroup);
    },

    // =========================================================================
    // 5. CIRCUIT OHM (Đoạn mạch định luật Ohm)
    // =========================================================================
    buildCircuitOhm: function(group, state) {
      var self = this;
      var cGroup = new THREE.Group();
      cGroup.position.set(0, 0.3, 0);

      // Wooden circuit breadboard
      var board = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.14, 2.8), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.6 }));
      board.position.set(0, 0.07, 0);
      cGroup.add(board);

      // Power Supply (Nguồn điện)
      var psu = new THREE.Mesh(new THREE.BoxGeometry(1.0, 0.65, 0.8), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.3 }));
      psu.position.set(-1.4, 0.45, -0.7);
      cGroup.add(psu);

      // Resistor (Điện trở R)
      var rMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.12, 0.12, 0.8, 20), new THREE.MeshStandardMaterial({ color: 0xd97706 }));
      rMesh.rotation.z = Math.PI / 2;
      rMesh.position.set(0, 0.3, -0.7);
      cGroup.add(rMesh);

      // Ammeter A with needle
      var aMeter = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.3, 32), new THREE.MeshStandardMaterial({ color: 0xdbeafe }));
      aMeter.position.set(1.3, 0.3, -0.7);
      cGroup.add(aMeter);

      var aNeedle = new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.28, 8), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      aNeedle.position.set(1.3, 0.46, -0.7);
      aNeedle.rotation.x = Math.PI / 2;
      cGroup.add(aNeedle);

      // Voltmeter V with needle
      var vMeter = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.3, 32), new THREE.MeshStandardMaterial({ color: 0xdbeafe }));
      vMeter.position.set(0, 0.3, 0.6);
      cGroup.add(vMeter);

      var vNeedle = new THREE.Mesh(new THREE.ConeGeometry(0.02, 0.28, 8), new THREE.MeshBasicMaterial({ color: 0xef4444 }));
      vNeedle.position.set(0, 0.46, 0.6);
      vNeedle.rotation.x = Math.PI / 2;
      cGroup.add(vNeedle);

      // Interactive Knife Switch (Công tắc K)
      var switchBase = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.08, 0.4), new THREE.MeshStandardMaterial({ color: 0x475569 }));
      switchBase.position.set(-1.4, 0.18, 0.6);
      cGroup.add(switchBase);

      var switchArm = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.45, 12), self.getMetalMaterial(0.2, 0xd97706));
      switchArm.position.set(-1.4, 0.32, 0.6);
      switchArm.rotation.z = 0.45;
      cGroup.add(switchArm);

      self.registerInteractive(switchBase, 'Công tắc K: Nhấp chuột để Đóng/Ngắt mạch', function(st) {
        var closed = (st.switchOn !== undefined) ? !st.switchOn : !st.switch_closed;
        st.switchOn = closed;
        st.switch_closed = closed;
        self.playSwitchSound();
        if (typeof window.syncControlsFromState === 'function') {
          window.syncControlsFromState('circuit_ohm');
        }
      });

      this.updateFns.push(function(st, t) {
        var isClosed = (st.switchOn !== undefined) ? !!st.switchOn : (st.switch_closed !== undefined ? !!st.switch_closed : true);
        switchArm.rotation.z = isClosed ? 0.0 : 0.55;
        var u = (st.voltage_v !== undefined) ? st.voltage_v : ((st.voltage !== undefined) ? st.voltage : ((st.U !== undefined) ? st.U : 12.0));
        var r = (st.resistance_ohm !== undefined) ? st.resistance_ohm : ((st.resistance !== undefined) ? st.resistance : ((st.R !== undefined) ? st.R : 20.0));
        var currentI = isClosed ? (u / (r || 1)) : 0.0;
        var currentU = isClosed ? u : 0.0;
        var maxI = 2.4;
        var maxU = 24.0;
        var targetRotA = -0.7 + (currentI / maxI) * 1.4;
        var targetRotV = -0.7 + (currentU / maxU) * 1.4;
        aNeedle.rotation.z += (targetRotA - aNeedle.rotation.z) * 0.15;
        vNeedle.rotation.z += (targetRotV - vNeedle.rotation.z) * 0.15;
      });

      group.add(cGroup);
    },

    // =========================================================================
    // 6. SPRING STRETCH (Lực đàn hồi lò xo)
    // =========================================================================
    buildSpringStretch: function(group, state) {
      var self = this;
      var sGroup = new THREE.Group();
      sGroup.position.set(0, 0, 0);

      var ironMat = this.getMetalMaterial(0.4, 0x1e293b);
      var chromeMat = this.getMetalMaterial(0.12, 0xf1f5f9);
      var brassMat = this.getMetalMaterial(0.2, 0xd97706);

      // 1. Cast-Iron Heavy Base with Beveled Rim & Rubber Feet
      var base = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.16, 1.3), ironMat);
      base.position.set(-0.2, 0.08, 0);
      base.castShadow = true;
      base.receiveShadow = true;
      sGroup.add(base);

      for (var fx = -0.95; fx <= 0.55; fx += 1.5) {
        for (var fz = -0.55; fz <= 0.55; fz += 1.1) {
          var foot = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 0.04, 16), new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.9 }));
          foot.position.set(fx, 0.02, fz);
          sGroup.add(foot);
        }
      }

      // 2. Stainless Steel Upright Rod (Trụ đứng mạ crom sáng bóng)
      var pole = new THREE.Mesh(new THREE.CylinderGeometry(0.05, 0.05, 3.6, 24), chromeMat);
      pole.position.set(-0.65, 1.88, 0);
      pole.castShadow = true;
      sGroup.add(pole);

      // 3. Double Clamp Bosshead (Khớp nối chữ thập bằng gang)
      var clamp = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.18, 0.18), ironMat);
      clamp.position.set(-0.65, 3.35, 0);
      sGroup.add(clamp);

      var wingScrew = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.32, 12), brassMat);
      wingScrew.rotation.z = Math.PI / 2;
      wingScrew.position.set(-0.8, 3.35, 0);
      sGroup.add(wingScrew);

      // 4. Horizontal Suspension Arm (Tay treo kim loại)
      var arm = new THREE.Mesh(new THREE.CylinderGeometry(0.035, 0.035, 0.9, 16), chromeMat);
      arm.rotation.z = Math.PI / 2;
      arm.position.set(-0.25, 3.35, 0);
      arm.castShadow = true;
      sGroup.add(arm);

      // Top suspension ring
      var topRing = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.015, 12, 24), brassMat);
      topRing.position.set(0.12, 3.31, 0);
      sGroup.add(topRing);

      // 5. Precision Millimeter Ruler (Thước thẳng chia vạch mm 0 - 30cm)
      var rulerCanvas = document.createElement('canvas');
      rulerCanvas.width = 256;
      rulerCanvas.height = 1024;
      var rctx = rulerCanvas.getContext('2d');

      // Ivory acrylic ruler background
      rctx.fillStyle = '#fefce8';
      rctx.fillRect(0, 0, 256, 1024);

      // Outer border
      rctx.strokeStyle = '#334155';
      rctx.lineWidth = 6;
      rctx.strokeRect(4, 4, 248, 1016);

      // Scale Header
      rctx.fillStyle = '#0f172a';
      rctx.font = 'bold 30px sans-serif';
      rctx.textAlign = 'center';
      rctx.fillText('cm (mm)', 128, 45);

      // Graduations (0 to 30 cm)
      var startY = 70;
      var endY = 990;
      var totalCm = 30;
      var stepY = (endY - startY) / totalCm;

      for (var c = 0; c <= totalCm; c++) {
        var cy = startY + c * stepY;

        // Centimeter line
        rctx.strokeStyle = '#0f172a';
        rctx.lineWidth = 3;
        rctx.beginPath();
        rctx.moveTo(20, cy);
        rctx.lineTo(110, cy);
        rctx.stroke();

        // Number label
        rctx.fillStyle = '#0f172a';
        rctx.font = 'bold 24px monospace';
        rctx.textAlign = 'left';
        rctx.fillText(c.toString(), 125, cy + 8);

        // Millimeter subdivisions
        if (c < totalCm) {
          for (var m = 1; m < 10; m++) {
            var my = cy + m * (stepY / 10);
            rctx.strokeStyle = (m === 5) ? '#1e293b' : '#64748b';
            rctx.lineWidth = (m === 5) ? 2.2 : 1.2;
            rctx.beginPath();
            rctx.moveTo(20, my);
            rctx.lineTo((m === 5) ? 80 : 50, my);
            rctx.stroke();
          }
        }
      }

      var rulerTex = new THREE.CanvasTexture(rulerCanvas);
      rulerTex.anisotropy = 8;
      var rulerMat = new THREE.MeshStandardMaterial({ map: rulerTex, roughness: 0.3, metalness: 0.05 });

      var rulerGeo = new THREE.BoxGeometry(0.38, 2.7, 0.03);
      var rulerMesh = new THREE.Mesh(rulerGeo, rulerMat);
      rulerMesh.position.set(-0.24, 1.88, 0);
      rulerMesh.castShadow = true;
      sGroup.add(rulerMesh);

      // Ruler mounting brackets
      var b1 = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.06, 0.08), ironMat);
      b1.position.set(-0.44, 3.0, 0);
      sGroup.add(b1);
      var b2 = new THREE.Mesh(new THREE.BoxGeometry(0.18, 0.06, 0.08), ironMat);
      b2.position.set(-0.44, 0.8, 0);
      sGroup.add(b2);

      // 6. High-Quality Helical Spring with dynamic geometry
      var springMesh = null;
      var springTopY = 3.25;

      function updateSpringMesh(len) {
        if (springMesh) sGroup.remove(springMesh);
        var points = [];
        var coils = 16;
        var r = 0.18;
        var totalPts = coils * 18;

        for (var i = 0; i <= totalPts; i++) {
          var frac = i / totalPts;
          var angle = frac * coils * Math.PI * 2;
          var py = springTopY - frac * len;
          points.push(new THREE.Vector3(0.12 + Math.cos(angle) * r, py, Math.sin(angle) * r));
        }
        var curve = new THREE.CatmullRomCurve3(points);
        var tubeGeo = new THREE.TubeGeometry(curve, totalPts, 0.032, 12, false);
        springMesh = new THREE.Mesh(tubeGeo, chromeMat);
        springMesh.castShadow = true;
        sGroup.add(springMesh);
      }

      // 7. Weight Hanger & Red Indicator Needle
      var hangerGroup = new THREE.Group();
      hangerGroup.position.set(0.12, 2.0, 0);

      // Bottom connecting hook
      var hookRing = new THREE.Mesh(new THREE.TorusGeometry(0.05, 0.015, 12, 20), brassMat);
      hookRing.position.set(0, 0, 0);
      hangerGroup.add(hookRing);

      // Bright Red Indicator Needle pointing across to ruler
      var needleMat = new THREE.MeshStandardMaterial({ color: 0xef4444, roughness: 0.2, emissive: 0xb91c1c, emissiveIntensity: 0.4 });
      var needle = new THREE.Mesh(new THREE.ConeGeometry(0.035, 0.42, 12), needleMat);
      needle.rotation.z = Math.PI / 2;
      needle.position.set(-0.21, 0, 0.02);
      hangerGroup.add(needle);

      // Hanger Vertical Stem & Base Flange
      var hangerStem = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.75, 12), brassMat);
      hangerStem.position.set(0, -0.38, 0);
      hangerGroup.add(hangerStem);

      var hangerBase = new THREE.Mesh(new THREE.CylinderGeometry(0.24, 0.24, 0.06, 24), brassMat);
      hangerBase.position.set(0, -0.74, 0);
      hangerGroup.add(hangerBase);

      // 4 Individual Slotted Weights (50g each)
      var slottedWeights = [];
      for (var wIdx = 0; wIdx < 4; wIdx++) {
        var wDisc = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.11, 24), brassMat);
        wDisc.position.set(0, -0.66 + wIdx * 0.12, 0);
        wDisc.castShadow = true;
        hangerGroup.add(wDisc);
        slottedWeights.push(wDisc);
      }

      sGroup.add(hangerGroup);

      // Focused Spotlight on spring & ruler
      var spotLight = new THREE.SpotLight(0xfffbeb, 1.8, 8, Math.PI / 3.5, 0.35);
      spotLight.position.set(1.4, 3.6, 2.5);
      spotLight.target = sGroup;
      sGroup.add(spotLight);

      // Interactive Click on weights to add mass
      self.registerInteractive(hangerBase, 'Quả cân: Nhấp chuột để Móc thêm 50g', function(st) {
        var curM = (st.mass !== undefined) ? st.mass : ((st.mass_g !== undefined) ? st.mass_g : 0);
        var nextM = (curM >= 200) ? 0 : curM + 50;
        st.mass = st.mass_g = nextM;
        self.playSwitchSound();
        if (typeof window.syncControlsFromState === 'function') {
          window.syncControlsFromState('spring_stretch');
        }
      });

      // Simulation physics loop with smooth damping and millimeter precision
      var currentLen = 1.1737;
      var oscVelocity = 0;
      var lastMass = -1;

      this.updateFns.push(function(st, t) {
        var mass = (st.mass !== undefined) ? st.mass : ((st.mass_g !== undefined) ? st.mass_g : 100);
        var k = st.k || 25;
        var l0 = st.l0 || 12.0;
        var forceP = (mass / 1000) * 9.8;
        var deltaL = (k > 0) ? (forceP / k) * 100 : 0; // cm
        var curL = l0 + deltaL; // cm

        // Number of weights visible (50g per disc, max 4 = 200g)
        var numWeights = Math.min(4, Math.floor(mass / 50));
        slottedWeights.forEach(function(sw, idx) {
          sw.visible = (idx < numWeights);
        });

        // Exact calibration: Needle tip points directly to curL mark on the millimeter ruler!
        // 0g -> 12.0 cm (1.1737m), 50g -> 14.0 cm (1.3352m), 100g -> 16.0 cm (1.4968m), 200g -> 20.0 cm (1.8198m)
        var targetLen = 0.2046 + curL * 0.08076;

        if (mass !== lastMass) {
          oscVelocity = (targetLen - currentLen) * 0.6;
          lastMass = mass;
        }

        // Damping oscillation
        var displacement = currentLen - targetLen;
        var springForce = -displacement * 0.18;
        oscVelocity += springForce;
        oscVelocity *= 0.88;
        currentLen += oscVelocity;

        updateSpringMesh(currentLen);
        hangerGroup.position.set(0.12, springTopY - currentLen, 0);

        // Update 3D Measurement HUD overlay
        if (self.container) {
          var hud = document.getElementById('lab3DSpringHUD');
          if (!hud) {
            hud = document.createElement('div');
            hud.id = 'lab3DSpringHUD';
            hud.style.cssText = 'position:absolute;top:10px;left:10px;background:rgba(15,23,42,0.85);backdrop-filter:blur(8px);border:1px solid #38bdf8;border-radius:8px;padding:8px 12px;color:#f8fafc;font-size:12px;box-shadow:0 8px 20px rgba(0,0,0,0.5);pointer-events:none;z-index:15;display:flex;flex-direction:column;gap:3px;';
            self.container.style.position = 'relative';
            self.container.appendChild(hud);
          }
          hud.innerHTML = '<div style="font-weight:700;color:#38bdf8;display:flex;align-items:center;gap:6px;">' +
            '<span>📍</span> Kim chỉ thước: <span style="font-size:14px;color:#ffffff;font-weight:800">' + curL.toFixed(1) + ' cm</span> ' +
            '<span style="color:#2dd4bf;font-weight:700">(Δl = +' + deltaL.toFixed(1) + ' cm)</span>' +
            '</div>' +
            '<div style="color:#cbd5e1;font-size:11px;">' +
            'Tải treo: <b>' + mass + ' g</b> (' + numWeights + ' quả cân 50g) &bull; Trọng lượng P = <b>' + forceP.toFixed(2) + ' N</b>' +
            '</div>';
        }
      });

      group.add(sGroup);
    },

    // =========================================================================
    // 7. ARCHIMEDES (Lực đẩy Archimedes)
    // =========================================================================
    buildArchimedes: function(group, state) {
      var self = this;
      var aGroup = new THREE.Group();
      aGroup.position.set(0, 0, 0);

      var ironMat = this.getMetalMaterial(0.45, 0x1e293b);
      var glassMat = this.getGlassMaterial(0xdbeafe, 0.32);

      // Overflow Beaker with spout
      var beaker = new THREE.Mesh(new THREE.CylinderGeometry(0.65, 0.65, 1.4, 32, 1, true), glassMat);
      beaker.position.set(-0.5, 0.75, 0);
      aGroup.add(beaker);

      var liq = new THREE.Mesh(new THREE.CylinderGeometry(0.63, 0.63, 1.0, 32), self.getLiquidMaterial(0x38bdf8, 0.7));
      liq.position.set(-0.5, 0.55, 0);
      aGroup.add(liq);

      // Catch Beaker
      var catchB = new THREE.Mesh(new THREE.CylinderGeometry(0.35, 0.35, 0.7, 24, 1, true), glassMat);
      catchB.position.set(0.7, 0.4, 0);
      aGroup.add(catchB);

      // Submerged Cylinder
      var brassBlock = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.5, 24), self.getMetalMaterial(0.2, 0xd97706));
      brassBlock.position.set(-0.5, 0.7, 0);
      aGroup.add(brassBlock);

      this.updateFns.push(function(st, t) {
        var depth = 0.5;
        if (st && st.submerged !== undefined) {
          depth = st.submerged;
        } else if (st && st.submerged_depth !== undefined) {
          depth = st.submerged_depth;
        } else if (st && st.matDensity && st.liqDensity) {
          var ratio = st.matDensity / st.liqDensity;
          depth = ratio < 1.0 ? ratio : 1.0;
        }
        var bob = Math.sin(t * 2.5) * 0.02;
        brassBlock.position.y = 1.2 - depth * 0.7 + bob;
        liq.scale.y = 1.0 + depth * 0.08;
      });

      group.add(aGroup);
    },

    // =========================================================================
    // 8. LENS CONVEX (Thấu kính hội tụ)
    // =========================================================================
    buildLensConvex: function(group, state) {
      var self = this;
      var lGroup = new THREE.Group();
      lGroup.position.set(0, 0.4, 0);

      // Optical Bench Rail (X axis, length 4.6)
      var rail = new THREE.Mesh(
        new THREE.BoxGeometry(4.6, 0.1, 0.35),
        self.getMetalMaterial(0.3, 0x334155)
      );
      rail.position.set(0, 0.05, 0);
      lGroup.add(rail);

      // Convex Lens at X = 0
      var lensHolder = new THREE.Mesh(
        new THREE.CylinderGeometry(0.58, 0.58, 0.06, 32),
        self.getMetalMaterial(0.2, 0x1e293b)
      );
      lensHolder.rotation.z = Math.PI / 2;
      lensHolder.position.set(0, 0.8, 0);
      lGroup.add(lensHolder);

      var lensMat = self.getGlassMaterial(0xdbeafe, 0.55);
      var lensMesh = new THREE.Mesh(new THREE.SphereGeometry(0.55, 32, 32), lensMat);
      lensMesh.scale.set(0.18, 1.0, 1.0);
      lensMesh.position.set(0, 0.8, 0);
      lGroup.add(lensMesh);

      // Candle Object (Vật sáng AB)
      var candleGroup = new THREE.Group();
      var candleBody = new THREE.Mesh(
        new THREE.CylinderGeometry(0.07, 0.07, 0.5, 16),
        new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.3 })
      );
      candleBody.position.set(0, 0.35, 0);
      candleGroup.add(candleBody);

      var flameGeo = new THREE.ConeGeometry(0.045, 0.15, 12);
      var flameMat = new THREE.MeshBasicMaterial({ color: 0xf59e0b });
      var flameMesh = new THREE.Mesh(flameGeo, flameMat);
      flameMesh.position.set(0, 0.68, 0);
      candleGroup.add(flameMesh);

      var flameLight = new THREE.PointLight(0xf59e0b, 1.5, 2.0);
      flameLight.position.set(0, 0.7, 0.05);
      candleGroup.add(flameLight);
      lGroup.add(candleGroup);

      // Projection Screen (Màn hứng ảnh A'B')
      var screenGroup = new THREE.Group();
      var screenPlate = new THREE.Mesh(
        new THREE.BoxGeometry(0.04, 0.95, 0.95),
        new THREE.MeshStandardMaterial({ color: 0xf1f5f9, roughness: 0.9 })
      );
      screenPlate.position.set(0, 0.75, 0);
      screenGroup.add(screenPlate);

      // Inverted image of candle on screen
      var imgFlameMesh = new THREE.Mesh(flameGeo, new THREE.MeshBasicMaterial({ color: 0xf59e0b, transparent: true, opacity: 0.85 }));
      imgFlameMesh.rotation.z = Math.PI;
      imgFlameMesh.position.set(-0.025, 0.75, 0);
      screenGroup.add(imgFlameMesh);
      lGroup.add(screenGroup);

      var curD = 25;
      this.updateFns.push(function(st, t) {
        var targetD = (st.d !== undefined) ? st.d : 25;
        var f = (st.f !== undefined) ? st.f : 10;

        curD += (targetD - curD) * 0.15;
        var candleX = - (curD / 10) * 0.8;
        candleGroup.position.set(candleX, 0, 0);

        flameMesh.scale.y = 1.0 + Math.sin(t * 18) * 0.15;

        if (curD > f + 0.5) {
          var dPrime = (curD * f) / (curD - f);
          var screenX = (dPrime / 10) * 0.8;
          screenX = Math.min(2.1, Math.max(0.4, screenX));
          screenGroup.position.set(screenX, 0, 0);
          screenGroup.visible = true;

          var mag = Math.abs(dPrime / curD);
          imgFlameMesh.visible = true;
          imgFlameMesh.scale.set(mag, mag * (1.0 + Math.sin(t * 18) * 0.15), mag);
          imgFlameMesh.position.y = 0.75 - (0.12 * mag);
        } else {
          screenGroup.visible = false;
        }
      });

      group.add(lGroup);
    },

    // =========================================================================
    // 9. LIGHT REFLECTION (Phản xạ ánh sáng)
    // =========================================================================
    buildLightReflection: function(group, state) {
      var self = this;
      var rGroup = new THREE.Group();
      rGroup.position.set(0, 0, 0);

      // Laboratory Stand Base
      var baseGeo = new THREE.BoxGeometry(2.4, 0.12, 1.4);
      var baseMat = self.getMetalMaterial(0.4, 0x1e293b);
      var standBase = new THREE.Mesh(baseGeo, baseMat);
      standBase.position.set(0, 0.06, 0);
      standBase.castShadow = true;
      standBase.receiveShadow = true;
      rGroup.add(standBase);

      // Support Pillar
      var pillarGeo = new THREE.CylinderGeometry(0.04, 0.04, 0.55, 16);
      var pillarMat = self.getMetalMaterial(0.2, 0x94a3b8);
      var pillar = new THREE.Mesh(pillarGeo, pillarMat);
      pillar.position.set(0, 0.35, -0.06);
      rGroup.add(pillar);

      // Circular Optical Protractor Disk (Radius 1.48, Facing Front)
      var discCanvas = document.createElement('canvas');
      discCanvas.width = 1024;
      discCanvas.height = 1024;
      var dCtx = discCanvas.getContext('2d');
      var cX = 512, cY = 512, dR = 460;

      // Dark metallic disc surface
      dCtx.fillStyle = '#0f172a';
      dCtx.beginPath();
      dCtx.arc(cX, cY, dR, 0, Math.PI * 2);
      dCtx.fill();

      // Outer rim and inner graduations
      dCtx.strokeStyle = '#38bdf8';
      dCtx.lineWidth = 6;
      dCtx.beginPath();
      dCtx.arc(cX, cY, dR - 8, 0, Math.PI * 2);
      dCtx.stroke();

      dCtx.strokeStyle = '#334155';
      dCtx.lineWidth = 2;
      dCtx.beginPath();
      dCtx.arc(cX, cY, dR - 70, 0, Math.PI * 2);
      dCtx.stroke();

      // Baseline (Mirror line)
      dCtx.strokeStyle = '#0284c7';
      dCtx.lineWidth = 5;
      dCtx.beginPath();
      dCtx.moveTo(cX - dR + 15, cY);
      dCtx.lineTo(cX + dR - 15, cY);
      dCtx.stroke();

      // Normal Line (ON) - Dashed
      dCtx.strokeStyle = '#f8fafc';
      dCtx.lineWidth = 4;
      dCtx.setLineDash([12, 10]);
      dCtx.beginPath();
      dCtx.moveTo(cX, cY);
      dCtx.lineTo(cX, cY - dR + 25);
      dCtx.stroke();
      dCtx.setLineDash([]);

      // Degree markings (every 5 and 10 deg)
      dCtx.fillStyle = '#94a3b8';
      dCtx.font = 'bold 22px system-ui, sans-serif';
      dCtx.textAlign = 'center';
      dCtx.textBaseline = 'middle';

      dCtx.fillText('N (Pháp tuyến)', cX, cY - dR + 52);
      dCtx.fillText('O (Điểm tới)', cX, cY + 36);

      for (var deg = 0; deg <= 90; deg += 5) {
        var aRad = (deg * Math.PI) / 180;
        var is10 = (deg % 10 === 0);
        var tickLen = is10 ? 32 : 16;
        
        // Left (-X, +Y)
        var lx1 = cX - Math.sin(aRad) * (dR - 12);
        var ly1 = cY - Math.cos(aRad) * (dR - 12);
        var lx2 = cX - Math.sin(aRad) * (dR - 12 - tickLen);
        var ly2 = cY - Math.cos(aRad) * (dR - 12 - tickLen);
        dCtx.strokeStyle = is10 ? '#38bdf8' : '#64748b';
        dCtx.lineWidth = is10 ? 3 : 1.5;
        dCtx.beginPath(); dCtx.moveTo(lx1, ly1); dCtx.lineTo(lx2, ly2); dCtx.stroke();

        // Right (+X, +Y)
        var rx1 = cX + Math.sin(aRad) * (dR - 12);
        var ry1 = cY - Math.cos(aRad) * (dR - 12);
        var rx2 = cX + Math.sin(aRad) * (dR - 12 - tickLen);
        var ry2 = cY - Math.cos(aRad) * (dR - 12 - tickLen);
        dCtx.beginPath(); dCtx.moveTo(rx1, ry1); dCtx.lineTo(rx2, ry2); dCtx.stroke();

        if (is10 && deg > 0 && deg < 90) {
          var tlx = cX - Math.sin(aRad) * (dR - 75);
          var tly = cY - Math.cos(aRad) * (dR - 75);
          dCtx.fillStyle = '#e2e8f0';
          dCtx.fillText(deg + '°', tlx, tly);

          var trx = cX + Math.sin(aRad) * (dR - 75);
          var try_ = cY - Math.cos(aRad) * (dR - 75);
          dCtx.fillText(deg + '°', trx, try_);
        }
      }

      var discTex = new THREE.CanvasTexture(discCanvas);
      discTex.anisotropy = 4;
      var discGeo = new THREE.CylinderGeometry(1.48, 1.48, 0.03, 64);
      var discMaterials = [
        new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 }),
        new THREE.MeshStandardMaterial({ map: discTex, roughness: 0.4, metalness: 0.1 }),
        new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.6 })
      ];
      var discMesh = new THREE.Mesh(discGeo, discMaterials);
      discMesh.rotation.x = Math.PI / 2;
      discMesh.position.set(0, 1.0, -0.02);
      rGroup.add(discMesh);

      // Plane Mirror mounted at center baseline O = (0, 1.0, 0)
      var mirrorGroup = new THREE.Group();
      mirrorGroup.position.set(0, 1.0, 0);

      var mirrorHolder = new THREE.Mesh(
        new THREE.BoxGeometry(1.6, 0.08, 0.3),
        self.getMetalMaterial(0.3, 0x1e293b)
      );
      mirrorHolder.position.set(0, -0.04, 0.06);
      mirrorGroup.add(mirrorHolder);

      var mirrorGlass = new THREE.Mesh(
        new THREE.BoxGeometry(1.5, 0.03, 0.24),
        new THREE.MeshStandardMaterial({
          color: 0xffffff,
          metalness: 0.95,
          roughness: 0.05,
          envMapIntensity: 2.0
        })
      );
      mirrorGlass.position.set(0, 0.015, 0.06);
      mirrorGroup.add(mirrorGlass);
      rGroup.add(mirrorGroup);

      // Laser Pointer Assembly
      var laserRadius = 1.25;
      var laserAssembly = new THREE.Group();
      laserAssembly.position.set(0, 1.0, 0.04);

      var laserBody = new THREE.Mesh(
        new THREE.CylinderGeometry(0.045, 0.055, 0.38, 20),
        self.getMetalMaterial(0.25, 0xd97706)
      );
      laserBody.position.set(0, laserRadius - 0.19, 0);
      laserAssembly.add(laserBody);

      var laserTip = new THREE.Mesh(
        new THREE.ConeGeometry(0.042, 0.08, 20),
        self.getMetalMaterial(0.15, 0x475569)
      );
      laserTip.rotation.x = Math.PI;
      laserTip.position.set(0, laserRadius - 0.42, 0);
      laserAssembly.add(laserTip);

      // Laser Mount Arm
      var armGeo = new THREE.BoxGeometry(0.03, laserRadius - 0.35, 0.02);
      var armMesh = new THREE.Mesh(armGeo, self.getMetalMaterial(0.4, 0x64748b));
      armMesh.position.set(0, (laserRadius - 0.35) / 2 + 0.1, -0.02);
      laserAssembly.add(armMesh);

      // Center pivot cap
      var pivotCap = new THREE.Mesh(
        new THREE.CylinderGeometry(0.07, 0.07, 0.05, 24),
        self.getMetalMaterial(0.2, 0x38bdf8)
      );
      pivotCap.rotation.x = Math.PI / 2;
      pivotCap.position.set(0, 0, 0.02);
      laserAssembly.add(pivotCap);

      rGroup.add(laserAssembly);

      // Dynamic Laser Beam Meshes
      var beamMatRed = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.95 });
      var beamRadius = 0.016;

      // Incident ray (laser tip -> center O)
      var inBeamGeo = new THREE.CylinderGeometry(beamRadius, beamRadius, laserRadius - 0.44, 12);
      var inBeamMesh = new THREE.Mesh(inBeamGeo, beamMatRed);
      inBeamMesh.position.set(0, (laserRadius - 0.44) / 2, 0.04);
      laserAssembly.add(inBeamMesh);

      // Reflected ray (center O -> outgoing at i' = i)
      var outRayLength = laserRadius - 0.1;
      var outBeamGeo = new THREE.CylinderGeometry(beamRadius, beamRadius, outRayLength, 12);
      var outBeamMesh = new THREE.Mesh(outBeamGeo, beamMatRed);
      rGroup.add(outBeamMesh);

      // Glowing laser spot at point of incidence O
      var spotGeo = new THREE.SphereGeometry(0.045, 16, 16);
      var spotMat = new THREE.MeshBasicMaterial({ color: 0xff3333 });
      var spotMesh = new THREE.Mesh(spotGeo, spotMat);
      spotMesh.position.set(0, 1.0, 0.06);
      rGroup.add(spotMesh);

      var spotLight = new THREE.PointLight(0xef4444, 2.0, 1.2);
      spotLight.position.set(0, 1.0, 0.12);
      rGroup.add(spotLight);

      // Dynamic update loop with damping & responsive control
      var curAngleDeg = 45;
      this.updateFns.push(function(st, t) {
        var targetDeg = (st.angle !== undefined) ? st.angle : ((st.angle_deg !== undefined) ? st.angle_deg : 45);
        curAngleDeg += (targetDeg - curAngleDeg) * 0.18;
        var rad = (curAngleDeg * Math.PI) / 180;

        var isOn = (st.laserOn !== false);
        var isGreen = (st.color === 'green');

        inBeamMesh.visible = isOn;
        outBeamMesh.visible = isOn;
        spotMesh.visible = isOn;
        spotLight.visible = isOn;

        var beamColorHex = isGreen ? 0x22c55e : 0xef4444;
        inBeamMesh.material.color.setHex(beamColorHex);
        outBeamMesh.material.color.setHex(beamColorHex);
        spotMat.color.setHex(isGreen ? 0x86efac : 0xfca5a5);
        spotLight.color.setHex(beamColorHex);

        laserAssembly.rotation.z = rad;

        var midX = Math.sin(rad) * (outRayLength / 2);
        var midY = 1.0 + Math.cos(rad) * (outRayLength / 2);
        outBeamMesh.position.set(midX, midY, 0.04);
        outBeamMesh.rotation.z = -rad;

        if (isOn) {
          var pulse = 1.0 + Math.sin(t * 20) * 0.08;
          spotLight.intensity = 1.8 * pulse;
          spotMesh.scale.set(pulse, pulse, pulse);
        }
      });

      group.add(rGroup);
    },

    // =========================================================================
    // 10. MASS CONSERVATION (Bảo toàn khối lượng: BaCl2 + Na2SO4 -> BaSO4 v)
    // =========================================================================
    buildMassConservation: function(group, state) {
      var self = this;
      var mGroup = new THREE.Group();
      mGroup.position.set(0, 0, 0);

      // Digital Analytical Balance Housing (Cân phân tích điện tử)
      var scaleBase = new THREE.Mesh(new THREE.BoxGeometry(2.6, 0.35, 2.2), new THREE.MeshStandardMaterial({ color: 0x1e293b, roughness: 0.35 }));
      scaleBase.position.set(0, 0.175, 0);
      scaleBase.castShadow = true;
      mGroup.add(scaleBase);

      // Stainless Steel Weighing Pan (Đĩa cân inox sáng bóng)
      var panMat = self.getMetalMaterial(0.12, 0xf1f5f9);
      var pan = new THREE.Mesh(new THREE.CylinderGeometry(0.95, 0.95, 0.06, 40), panMat);
      pan.position.set(0, 0.38, 0);
      pan.castShadow = true;
      mGroup.add(pan);

      // Glowing Green LED Readout Panel
      var ledPanel = new THREE.Mesh(new THREE.BoxGeometry(1.3, 0.24, 0.02), new THREE.MeshBasicMaterial({ color: 0x052e16 }));
      ledPanel.position.set(0, 0.19, 1.11);
      mGroup.add(ledPanel);

      var canvas = document.createElement('canvas');
      canvas.width = 256;
      canvas.height = 64;
      var ctx = canvas.getContext('2d');
      ctx.fillStyle = '#052e16';
      ctx.fillRect(0, 0, 256, 64);
      ctx.fillStyle = '#22c55e';
      ctx.font = 'bold 36px monospace';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('158.45 g', 128, 32);

      var ledTex = new THREE.CanvasTexture(canvas);
      var ledMesh = new THREE.Mesh(new THREE.PlaneGeometry(1.2, 0.20), new THREE.MeshBasicMaterial({ map: ledTex, transparent: true }));
      ledMesh.position.set(0, 0.19, 1.122);
      mGroup.add(ledMesh);

      // Glass Draft Shield Cover
      var shield = new THREE.Mesh(new THREE.CylinderGeometry(1.02, 1.02, 1.7, 32, 1, true), self.getGlassMaterial(0xdbeafe, 0.15));
      shield.position.set(0, 1.25, 0);
      mGroup.add(shield);

      var glassMat = self.getGlassMaterial(0xdbeafe, 0.32);

      // Beaker A (BaCl2 Solution - Left) - Capable of full tilting & pouring kinematics
      var beakerA = new THREE.Group();
      beakerA.position.set(-0.45, 0.41, 0);

      var bAGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.9, 28, 1, true), glassMat);
      bAGlass.position.set(0, 0.45, 0);
      beakerA.add(bAGlass);

      var bALiqMat = self.getLiquidMaterial(0x93c5fd, 0.55);
      var bALiq = new THREE.Mesh(new THREE.CylinderGeometry(0.30, 0.30, 0.45, 28), bALiqMat);
      bALiq.position.set(0, 0.23, 0);
      beakerA.add(bALiq);
      mGroup.add(beakerA);

      // Pouring Stream Mesh (Dòng chất lỏng rót từ cốc A sang cốc B)
      var pourStreamMat = self.getLiquidMaterial(0x93c5fd, 0.75);
      var pourStream = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.045, 0.85, 12), pourStreamMat);
      pourStream.position.set(0.12, 1.05, 0);
      pourStream.rotation.z = -0.45;
      pourStream.visible = false;
      mGroup.add(pourStream);

      // Beaker B (Na2SO4 Solution -> White BaSO4 Precipitate - Right)
      var beakerB = new THREE.Group();
      beakerB.position.set(0.45, 0.41, 0);

      var bBGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.34, 0.34, 0.95, 28, 1, true), glassMat);
      bBGlass.position.set(0, 0.48, 0);
      beakerB.add(bBGlass);

      var bBLiqMat = self.getLiquidMaterial(0x93c5fd, 0.55);
      var bBLiq = new THREE.Mesh(new THREE.CylinderGeometry(0.32, 0.32, 0.48, 28), bBLiqMat);
      bBLiq.position.set(0, 0.24, 0);
      beakerB.add(bBLiq);

      // Dense White Milky Precipitate (BaSO4 kết tủa trắng đục)
      var pptMat = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        roughness: 0.95,
        transparent: true,
        opacity: 0
      });
      var pptMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.318, 0.318, 0.65, 28), pptMat);
      pptMesh.position.set(0, 0.33, 0);
      beakerB.add(pptMesh);

      // Precipitate Flakes
      var flakesGroup = new THREE.Group();
      flakesGroup.position.set(0, 0.35, 0);
      var flakeMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0 });
      var flakes = [];
      for (var f = 0; f < 30; f++) {
        var fl = new THREE.Mesh(new THREE.DodecahedronGeometry(0.015 + Math.random() * 0.02), flakeMat);
        fl.position.set((Math.random() - 0.5) * 0.45, (Math.random() - 0.5) * 0.4, (Math.random() - 0.5) * 0.45);
        flakesGroup.add(fl);
        flakes.push(fl);
      }
      beakerB.add(flakesGroup);
      mGroup.add(beakerB);

      self.registerInteractive(scaleBase, 'Cân điện tử: Nhấp chuột để Trộn 2 dung dịch BaCl2 & Na2SO4', function(st) {
        st.reacted = !st.reacted;
        st.step = st.reacted ? 2 : 1;
        self.playBellSound();
      });

      // Kinematic Pouring & Reacting Animation
      var animTime = 0;
      this.updateFns.push(function(st, t) {
        var isReacted = !!st.reacted || (st.step !== undefined && st.step >= 2) || (st.mixProgress !== undefined && st.mixProgress > 0);
        if (isReacted) {
          animTime = Math.min(1.0, animTime + 0.025);

          // Phase 1 (0 -> 0.4): Lift Beaker A and move over Beaker B
          // Phase 2 (0.4 -> 0.8): Tilt Beaker A and pour stream
          // Phase 3 (0.8 -> 1.0): Rotate back and return to pan
          if (animTime < 0.35) {
            var p1 = animTime / 0.35;
            beakerA.position.set(
              THREE.MathUtils.lerp(-0.45, 0.15, p1),
              THREE.MathUtils.lerp(0.41, 1.45, p1),
              0
            );
            beakerA.rotation.z = 0;
            pourStream.visible = false;
          } else if (animTime < 0.75) {
            var p2 = (animTime - 0.35) / 0.40;
            beakerA.position.set(0.15, 1.45, 0);
            beakerA.rotation.z = THREE.MathUtils.lerp(0, 1.15, p2);
            pourStream.visible = (p2 > 0.2 && p2 < 0.9);
            bALiq.scale.y = Math.max(0.001, 1.0 - p2 * 1.2);
            bALiq.visible = (bALiq.scale.y > 0.05);

            // Beaker B reacts
            bBLiq.scale.y = 1.0 + p2 * 0.45;
            bBLiq.position.y = 0.24 + p2 * 0.11;
            pptMat.opacity = Math.min(0.95, p2 * 1.2);
            flakeMat.opacity = Math.min(0.9, p2 * 1.2);
          } else {
            var p3 = (animTime - 0.75) / 0.25;
            beakerA.rotation.z = THREE.MathUtils.lerp(1.15, 0, p3);
            beakerA.position.set(
              THREE.MathUtils.lerp(0.15, -0.45, p3),
              THREE.MathUtils.lerp(1.45, 0.41, p3),
              0
            );
            pourStream.visible = false;
            bALiq.visible = false;
            pptMat.opacity = 0.95;
            flakeMat.opacity = 0.9;
          }

          // Swirling precipitate flakes in Beaker B
          flakes.forEach(function(fl, idx) {
            fl.position.y -= 0.004;
            if (fl.position.y < -0.25) fl.position.y = 0.25;
            fl.rotation.x += 0.03 * (idx % 2 === 0 ? 1 : -1);
          });
        } else {
          animTime = 0;
          beakerA.position.set(-0.45, 0.41, 0);
          beakerA.rotation.z = 0;
          bALiq.scale.y = 1.0;
          bALiq.visible = true;
          pourStream.visible = false;
          bBLiq.scale.y = 1.0;
          bBLiq.position.y = 0.24;
          pptMat.opacity = 0;
          flakeMat.opacity = 0;
        }
      });

      group.add(mGroup);
    },

    buildAcidBaseNeutralization: function(group, state) {
      var self = this;
      var nGroup = new THREE.Group();
      nGroup.position.set(0, 0, 0);

      var ironMat = this.getMetalMaterial(0.45, 0x1e293b);
      var chromeMat = this.getMetalMaterial(0.2, 0xe2e8f0);
      var glassMat = this.getGlassMaterial(0xdbeafe, 0.28);

      // Retort Stand with White Porcelain Base
      var base = new THREE.Mesh(new THREE.BoxGeometry(1.8, 0.12, 1.4), new THREE.MeshStandardMaterial({ color: 0xf8fafc, roughness: 0.2 }));
      base.position.set(0, 0.06, 0);
      base.castShadow = true;
      nGroup.add(base);

      var rod = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 3.8, 16), chromeMat);
      rod.position.set(-0.6, 1.96, -0.4);
      rod.castShadow = true;
      nGroup.add(rod);

      var clamp = new THREE.Mesh(new THREE.BoxGeometry(0.6, 0.08, 0.08), ironMat);
      clamp.position.set(-0.3, 2.4, -0.4);
      nGroup.add(clamp);

      // Glass Burette 50ml
      var buretGroup = new THREE.Group();
      buretGroup.position.set(0, 2.2, 0);

      var buretTube = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 2.4, 20, 1, true), glassMat);
      buretTube.position.set(0, 0, 0);
      buretGroup.add(buretTube);

      var buretTip = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.02, 0.4, 16, 1, true), glassMat);
      buretTip.position.set(0, -1.4, 0);
      buretGroup.add(buretTip);

      var valve = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.22, 12), new THREE.MeshStandardMaterial({ color: 0x0284c7, roughness: 0.3 }));
      valve.rotation.z = Math.PI / 2;
      valve.position.set(0, -1.2, 0);
      buretGroup.add(valve);

      var buretLiqMat = self.getLiquidMaterial(0x93c5fd, 0.65);
      var buretLiq = new THREE.Mesh(new THREE.CylinderGeometry(0.075, 0.075, 2.2, 16), buretLiqMat);
      buretLiq.position.set(0, 0.05, 0);
      buretGroup.add(buretLiq);

      nGroup.add(buretGroup);

      // Erlenmeyer Flask sitting below
      var flaskGroup = new THREE.Group();
      flaskGroup.position.set(0, 0.12, 0);

      var flaskPoints = [
        new THREE.Vector2(0.001, 0.0), new THREE.Vector2(0.62, 0.02), new THREE.Vector2(0.65, 0.15),
        new THREE.Vector2(0.28, 0.95), new THREE.Vector2(0.18, 1.25), new THREE.Vector2(0.20, 1.28),
        new THREE.Vector2(0.16, 1.28), new THREE.Vector2(0.16, 0.95), new THREE.Vector2(0.60, 0.15),
        new THREE.Vector2(0.001, 0.02)
      ];
      var flaskGeo = new THREE.LatheGeometry(flaskPoints, 32);
      var flask = new THREE.Mesh(flaskGeo, glassMat);
      flask.position.set(0, 0, 0);
      flask.castShadow = true;
      flaskGroup.add(flask);

      // Flask Solution
      var flaskSolMat = new THREE.MeshStandardMaterial({
        color: 0xdbeafe,
        transparent: true,
        opacity: 0.35,
        roughness: 0.15
      });
      var flaskLiqPoints = [
        new THREE.Vector2(0.001, 0.01), new THREE.Vector2(0.58, 0.02), new THREE.Vector2(0.59, 0.15),
        new THREE.Vector2(0.38, 0.65), new THREE.Vector2(0.001, 0.65)
      ];
      var flaskLiqGeo = new THREE.LatheGeometry(flaskLiqPoints, 32);
      var flaskLiq = new THREE.Mesh(flaskLiqGeo, flaskSolMat);
      flaskLiq.position.set(0, 0, 0);
      flaskGroup.add(flaskLiq);

      var stirBar = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 0.22, 12), new THREE.MeshStandardMaterial({ color: 0xffffff, roughness: 0.2 }));
      stirBar.rotation.z = Math.PI / 2;
      stirBar.position.set(0, 0.04, 0);
      flaskGroup.add(stirBar);

      var dropMat = self.getLiquidMaterial(0x93c5fd, 0.85);
      var drop = new THREE.Mesh(new THREE.SphereGeometry(0.025, 10, 10), dropMat);
      drop.scale.set(1, 1.4, 1);
      drop.position.set(0, 0.78, 0);
      drop.visible = false;
      nGroup.add(drop);

      var ripGeo = new THREE.RingGeometry(0.02, 0.22, 20);
      var ripMat = new THREE.MeshBasicMaterial({ color: 0xf472b6, transparent: true, opacity: 0, side: THREE.DoubleSide });
      var ripMesh = new THREE.Mesh(ripGeo, ripMat);
      ripMesh.rotation.x = -Math.PI / 2;
      ripMesh.position.set(0, 0.652, 0);
      flaskGroup.add(ripMesh);

      nGroup.add(flaskGroup);

      self.registerInteractive(valve, 'Khóa buret: Nhấp chuột để Mở/Khóa nhỏ giọt NaOH', function(st) {
        st.buretteFlow = (st.buretteFlow === 0 || !st.buretteFlow) ? 1 : 0;
        self.playSwitchSound();
      });

      var dropY = 0.78;
      this.updateFns.push(function(st, t) {
        var flow = (st && st.buretteFlow !== undefined) ? st.buretteFlow : 0;
        var addedMl = (st && st.addedMl !== undefined) ? st.addedMl : 0;

        if (flow > 0) {
          drop.visible = true;
          dropY -= 0.032 * flow;
          if (dropY < 0.65) {
            dropY = 0.78;
            ripMat.opacity = 0.85;
            self.playDripSound();
          }
          drop.position.y = dropY;
          if (ripMat.opacity > 0) ripMat.opacity -= 0.04;
          valve.rotation.x = Math.PI / 2;
        } else {
          drop.visible = false;
          ripMat.opacity = 0;
          valve.rotation.x = 0;
        }

        stirBar.rotation.y += 0.25;

        var buretScale = Math.max(0.05, 1.0 - (addedMl / 25.0));
        buretLiq.scale.y = buretScale;
        buretLiq.position.y = -1.1 + 1.15 * buretScale;

        if (addedMl < 9.8) {
          flaskSolMat.color.lerp(new THREE.Color(0xdbeafe), 0.08);
          flaskSolMat.opacity = THREE.MathUtils.lerp(flaskSolMat.opacity, 0.28, 0.08);
        } else if (addedMl <= 10.2) {
          flaskSolMat.color.lerp(new THREE.Color(0xf472b6), 0.12);
          flaskSolMat.opacity = THREE.MathUtils.lerp(flaskSolMat.opacity, 0.78, 0.12);
        } else {
          flaskSolMat.color.lerp(new THREE.Color(0xdb2777), 0.08);
          flaskSolMat.opacity = THREE.MathUtils.lerp(flaskSolMat.opacity, 0.92, 0.08);
        }
      });

      group.add(nGroup);
    },

    buildMetalAcid: function(group, state) {
      var self = this;
      var maGroup = new THREE.Group();
      maGroup.position.set(0, 0, 0);

      var woodMat = new THREE.MeshStandardMaterial({ color: 0x92400e, roughness: 0.75 });
      var glassMat = this.getGlassMaterial(0xdbeafe, 0.28);

      var rackBase = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.12, 1.2), woodMat);
      rackBase.position.set(0, 0.06, 0);
      maGroup.add(rackBase);

      var rackTop = new THREE.Mesh(new THREE.BoxGeometry(3.6, 0.08, 1.2), woodMat);
      rackTop.position.set(0, 1.1, 0);
      maGroup.add(rackTop);

      for (var p = -1.6; p <= 1.6; p += 3.2) {
        var post = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.1, 12), woodMat);
        post.position.set(p, 0.58, 0);
        maGroup.add(post);
      }

      var metalConfigs = [
        { name: "Mg (Magie)", x: -1.2, color: 0xe2e8f0, bubbleCount: 24, bubbleSpeed: 0.035, tint: 0x93c5fd },
        { name: "Zn (Kẽm)",   x: -0.4, color: 0x94a3b8, bubbleCount: 16, bubbleSpeed: 0.020, tint: 0x93c5fd },
        { name: "Fe (Sắt)",   x:  0.4, color: 0x475569, bubbleCount: 8,  bubbleSpeed: 0.008, tint: 0x86efac },
        { name: "Cu (Đồng)",  x:  1.2, color: 0xea580c, bubbleCount: 0,  bubbleSpeed: 0,     tint: 0x93c5fd }
      ];

      var tubesData = [];
      metalConfigs.forEach(function(cfg) {
        var tGroup = new THREE.Group();
        tGroup.position.set(cfg.x, 0.8, 0);

        var tube = new THREE.Mesh(new THREE.CylinderGeometry(0.16, 0.16, 1.4, 24, 1, true), glassMat);
        tGroup.add(tube);

        var liqMat = self.getLiquidMaterial(cfg.tint, 0.5);
        var liq = new THREE.Mesh(new THREE.CylinderGeometry(0.15, 0.15, 0.75, 24), liqMat);
        liq.position.set(0, -0.3, 0);
        tGroup.add(liq);

        var metalMesh;
        if (cfg.name.indexOf("Cu") !== -1) {
          metalMesh = new THREE.Mesh(new THREE.BoxGeometry(0.06, 0.35, 0.02), new THREE.MeshStandardMaterial({ color: cfg.color, metalness: 0.85, roughness: 0.2 }));
        } else if (cfg.name.indexOf("Fe") !== -1) {
          metalMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.025, 0.025, 0.4, 12), new THREE.MeshStandardMaterial({ color: cfg.color, metalness: 0.7, roughness: 0.3 }));
        } else {
          metalMesh = new THREE.Mesh(new THREE.DodecahedronGeometry(0.06), new THREE.MeshStandardMaterial({ color: cfg.color, metalness: 0.8, roughness: 0.25 }));
        }
        metalMesh.position.set(0, -0.6, 0);
        tGroup.add(metalMesh);

        var bubbleList = [];
        var bMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.8 });
        for (var b = 0; b < cfg.bubbleCount; b++) {
          var bMesh = new THREE.Mesh(new THREE.SphereGeometry(0.015 + Math.random() * 0.02, 8, 8), bMat);
          bMesh.position.set((Math.random() - 0.5) * 0.18, -0.6 + Math.random() * 0.6, (Math.random() - 0.5) * 0.18);
          tGroup.add(bMesh);
          bubbleList.push({ mesh: bMesh, speed: cfg.bubbleSpeed * (0.8 + Math.random() * 0.4) });
        }

        maGroup.add(tGroup);
        tubesData.push({ config: cfg, bubbles: bubbleList, liqMat: liqMat });
      });

      var splintGroup = new THREE.Group();
      splintGroup.position.set(-0.4, 2.1, 0);

      var splintStick = new THREE.Mesh(new THREE.CylinderGeometry(0.015, 0.015, 0.8, 8), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.8 }));
      splintStick.rotation.z = 0.5;
      splintGroup.add(splintStick);

      var splintFlame = new THREE.Mesh(new THREE.ConeGeometry(0.04, 0.16, 12), new THREE.MeshBasicMaterial({ color: 0x38bdf8, transparent: true, opacity: 0.9 }));
      splintFlame.position.set(0.18, -0.38, 0);
      splintGroup.add(splintFlame);
      splintGroup.visible = false;
      maGroup.add(splintGroup);

      self.registerInteractive(rackBase, 'Giá ống nghiệm: Nhấp chuột để Thử que đóm kiểm tra khí H2', function(st) {
        st.splintTest = !st.splintTest;
        if (st.splintTest) self.playPopSound();
      });

      this.updateFns.push(function(st, t) {
        var isReacting = (st && st.acidConc !== "none");
        var activeMetal = (st && st.metal) ? st.metal : "Zn";
        var isSplint = !!(st && st.splintTest);

        tubesData.forEach(function(td) {
          var isThisActive = (td.config.name.indexOf(activeMetal) !== -1);
          td.bubbles.forEach(function(bObj) {
            if (isReacting && (isThisActive || activeMetal === "all")) {
              bObj.mesh.visible = true;
              bObj.mesh.position.y += bObj.speed;
              if (bObj.mesh.position.y > 0.05) {
                bObj.mesh.position.y = -0.6;
              }
            } else {
              bObj.mesh.visible = false;
            }
          });
        });

        if (isSplint) {
          splintGroup.visible = true;
          var flicker = 1.0 + Math.sin(t * 25) * 0.25;
          splintFlame.scale.set(flicker, flicker * 1.3, flicker);
        } else {
          splintGroup.visible = false;
        }
      });

      group.add(maGroup);
    },

    buildPhIndicator: function(group, state) {
      var self = this;
      var phGroup = new THREE.Group();
      phGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.28);
      var woodMat = new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.75 });

      // Wooden Rack Base & Upper tier
      var rackBase = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.12, 1.2), woodMat);
      rackBase.position.set(0, 0.06, 0);
      phGroup.add(rackBase);

      var rackTop = new THREE.Mesh(new THREE.BoxGeometry(3.8, 0.08, 1.2), woodMat);
      rackTop.position.set(0, 1.1, 0);
      phGroup.add(rackTop);

      for (var p = -1.7; p <= 1.7; p += 3.4) {
        var post = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 1.1, 12), woodMat);
        post.position.set(p, 0.58, 0);
        phGroup.add(post);
      }

      // 5 Real-world Samples with Positions
      var sampleData = [
        { name: "Chanh",     ph: 2.2, color: 0xef4444, liqColor: 0xfef08a, x: -1.4 },
        { name: "Giấm",      ph: 3.0, color: 0xf97316, liqColor: 0xffedd5, x: -0.7 },
        { name: "Nước cất",  ph: 7.0, color: 0x22c55e, liqColor: 0xbae6fd, x:  0.0 },
        { name: "Xà phòng", ph: 9.5, color: 0x0ea5e9, liqColor: 0xe0f2fe, x:  0.7 },
        { name: "NaOH",      ph: 13.0, color: 0x7c3aed, liqColor: 0xdbeafe, x:  1.4 }
      ];

      var strips = [];
      sampleData.forEach(function(smp) {
        var tGroup = new THREE.Group();
        tGroup.position.set(smp.x, 0.8, 0);

        var tube = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 1.4, 20, 1, true), glassMat);
        tGroup.add(tube);

        var liq = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.8, 20), self.getLiquidMaterial(smp.liqColor, 0.65));
        liq.position.set(0, -0.28, 0);
        tGroup.add(liq);

        // Watch glass with pH paper strip in front
        var watchGlass = new THREE.Mesh(new THREE.CylinderGeometry(0.22, 0.22, 0.04, 20), glassMat);
        watchGlass.position.set(smp.x, 0.14, 0.85);
        phGroup.add(watchGlass);

        var stripMat = new THREE.MeshStandardMaterial({ color: 0xfef08a, roughness: 0.8 });
        var strip = new THREE.Mesh(new THREE.BoxGeometry(0.10, 0.01, 0.32), stripMat);
        strip.position.set(smp.x, 0.165, 0.85);
        phGroup.add(strip);

        strips.push({ sample: smp, stripMat: stripMat });
        phGroup.add(tGroup);
      });

      // Animated Glass Stirring Rod (Đũa thủy tinh chấm thử pH thực tế)
      var rodGroup = new THREE.Group();
      rodGroup.position.set(0, 1.6, 0.4);

      var rod = new THREE.Mesh(new THREE.CylinderGeometry(0.02, 0.02, 1.2, 12), glassMat);
      rod.rotation.z = 0.25;
      rodGroup.add(rod);

      // Droplet at rod tip
      var tipDropMat = self.getLiquidMaterial(0xfef08a, 0.85);
      var tipDrop = new THREE.Mesh(new THREE.SphereGeometry(0.028, 10, 10), tipDropMat);
      tipDrop.position.set(0.15, -0.58, 0);
      tipDrop.visible = false;
      rodGroup.add(tipDrop);

      phGroup.add(rodGroup);

      self.registerInteractive(rackBase, 'Bảng so màu pH: Nhấp chuột để Chấm đũa thủy tinh thử pH các mẫu', function(st) {
        st.samplePh = (st.samplePh === 7.0 || !st.samplePh) ? 2.2 : (st.samplePh === 2.2 ? 13.0 : 7.0);
        self.playBellSound();
      });

      // Action loop: Dip rod -> Lift -> Dab on strip -> Color spread
      var rodAnimProgress = 0;
      var lastTargetPh = 7.0;

      this.updateFns.push(function(st, t) {
        var curPh = (st && st.samplePh !== undefined) ? st.samplePh : 7.0;

        // Find matching sample
        var activeSample = sampleData[2]; // Default neutral
        for (var i = 0; i < sampleData.length; i++) {
          if (Math.abs(sampleData[i].ph - curPh) < 1.5) {
            activeSample = sampleData[i];
            break;
          }
        }

        if (curPh !== lastTargetPh) {
          lastTargetPh = curPh;
          rodAnimProgress = 0; // Trigger dab animation
        }

        rodAnimProgress = Math.min(1.0, rodAnimProgress + 0.02);

        // Rod Motion Kinematics:
        // 0.0 -> 0.3: Move over tube and dip down into solution
        // 0.3 -> 0.6: Lift out with liquid drop on tip
        // 0.6 -> 0.85: Move forward over watch glass and dab down on paper
        // 0.85 -> 1.0: Lift back up
        var targetX = activeSample.x;
        if (rodAnimProgress < 0.3) {
          var p1 = rodAnimProgress / 0.3;
          rodGroup.position.set(
            targetX,
            THREE.MathUtils.lerp(1.6, 0.85, p1),
            THREE.MathUtils.lerp(0.4, 0, p1)
          );
          tipDrop.visible = false;
        } else if (rodAnimProgress < 0.6) {
          var p2 = (rodAnimProgress - 0.3) / 0.3;
          rodGroup.position.set(
            targetX,
            THREE.MathUtils.lerp(0.85, 1.55, p2),
            THREE.MathUtils.lerp(0, 0.4, p2)
          );
          tipDrop.visible = true;
          tipDropMat.color.set(activeSample.liqColor);
        } else if (rodAnimProgress < 0.85) {
          var p3 = (rodAnimProgress - 0.6) / 0.25;
          rodGroup.position.set(
            targetX,
            THREE.MathUtils.lerp(1.55, 0.75, p3),
            THREE.MathUtils.lerp(0.4, 0.85, p3)
          );
          if (p3 > 0.85) {
            tipDrop.visible = false;
            self.playDripSound();
          }
        } else {
          var p4 = (rodAnimProgress - 0.85) / 0.15;
          rodGroup.position.set(
            targetX,
            THREE.MathUtils.lerp(0.75, 1.5, p4),
            THREE.MathUtils.lerp(0.85, 0.4, p4)
          );
        }

        // Color strips
        strips.forEach(function(sObj) {
          if (Math.abs(sObj.sample.ph - curPh) < 1.5 || curPh === "all") {
            if (rodAnimProgress > 0.75) {
              sObj.stripMat.color.lerp(new THREE.Color(sObj.sample.color), 0.08);
            }
          } else {
            sObj.stripMat.color.lerp(new THREE.Color(0xfef08a), 0.06);
          }
        });
      });

      group.add(phGroup);
    },

    buildLeverBalance: function(group, state) {
      var self = this;
      var lGroup = new THREE.Group();
      lGroup.position.set(0, 0, 0);

      var ironMat = this.getMetalMaterial(0.45, 0x1e293b);
      var chromeMat = this.getMetalMaterial(0.2, 0xe2e8f0);

      // Fulcrum Pyramid Base
      var base = new THREE.Mesh(new THREE.BoxGeometry(2.0, 0.12, 1.4), ironMat);
      base.position.set(0, 0.06, 0);
      lGroup.add(base);

      var fulcrum = new THREE.Mesh(new THREE.ConeGeometry(0.35, 1.4, 4), ironMat);
      fulcrum.position.set(0, 0.76, 0);
      fulcrum.rotation.y = Math.PI / 4;
      lGroup.add(fulcrum);

      // Meter Lever Beam
      var beamGroup = new THREE.Group();
      beamGroup.position.set(0, 1.46, 0);

      var beam = new THREE.Mesh(new THREE.BoxGeometry(4.2, 0.08, 0.18), chromeMat);
      beamGroup.add(beam);

      // Hanging Weights
      var wLeft = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.35, 16), self.getMetalMaterial(0.2, 0xd97706));
      wLeft.position.set(-1.2, -0.3, 0);
      beamGroup.add(wLeft);

      var wRight = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 0.35, 16), self.getMetalMaterial(0.2, 0xd97706));
      wRight.position.set(1.2, -0.3, 0);
      beamGroup.add(wRight);

      self.registerInteractive(beam, 'Thanh đòn bẩy: Nhấp chuột để đổi vị trí quả nặng', function(st) {
        st.leverBalanced = !st.leverBalanced;
        self.playSwitchSound();
      });

      this.updateFns.push(function(st, t) {
        var tilt = 0;
        if (st.m1 !== undefined && st.d1 !== undefined && st.m2 !== undefined && st.d2 !== undefined) {
          var torqueDiff = (st.m1 * st.d1) - (st.m2 * st.d2);
          tilt = Math.max(-0.25, Math.min(0.25, -torqueDiff * 0.00012));
          if (torqueDiff === 0) tilt += Math.sin(t * 2.0) * 0.01;
        } else {
          tilt = st.leverBalanced ? 0 : Math.sin(t * 1.5) * 0.12;
        }
        beamGroup.rotation.z += (tilt - beamGroup.rotation.z) * 0.1;
      });

      lGroup.add(beamGroup);
      group.add(lGroup);
    },

    // =========================================================================
    // 15. LIQUID PRESSURE (Áp suất chất lỏng & Áp kế chữ U)
    // =========================================================================
    buildLiquidPressure: function(group, state) {
      var self = this;
      var lpGroup = new THREE.Group();
      lpGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.3);

      // Tall Cylinder containing water
      var cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.7, 0.7, 2.6, 32, 1, true), glassMat);
      cyl.position.set(-0.8, 1.35, 0);
      lpGroup.add(cyl);

      var water = new THREE.Mesh(new THREE.CylinderGeometry(0.68, 0.68, 2.2, 32), self.getLiquidMaterial(0x38bdf8, 0.65));
      water.position.set(-0.8, 1.15, 0);
      lpGroup.add(water);

      // Pressure Probe
      var probe = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, 0.12, 20), self.getMetalMaterial(0.25, 0xd97706));
      probe.position.set(-0.8, 1.2, 0);
      lpGroup.add(probe);

      // U-Tube Manometer (right side)
      var uTube = new THREE.Mesh(new THREE.TorusGeometry(0.4, 0.05, 16, 32, Math.PI), glassMat);
      uTube.position.set(1.1, 0.8, 0);
      uTube.rotation.z = Math.PI;
      lpGroup.add(uTube);

      // Red Manometer Fluid Columns
      var leftCol = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.6, 16), self.getLiquidMaterial(0xef4444, 0.9));
      leftCol.position.set(0.7, 1.1, 0);
      lpGroup.add(leftCol);

      var rightCol = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.9, 16), self.getLiquidMaterial(0xef4444, 0.9));
      rightCol.position.set(1.5, 1.25, 0);
      lpGroup.add(rightCol);

      self.registerInteractive(cyl, 'Ống chất lỏng: Nhấp chuột để Di chuyển đầu dò áp suất', function(st) {
        st.probeDepth = ((st.probeDepth || 1) % 3) + 1;
        self.playBellSound();
      });

      this.updateFns.push(function(st, t) {
        var depthVal = (st.depth !== undefined) ? (st.depth / 6.0) : (st.probeDepth || 1);
        var clampedD = Math.max(0.2, Math.min(3.0, depthVal));
        probe.position.y = 1.9 - clampedD * 0.45;
        leftCol.scale.y = Math.max(0.1, 1.0 - clampedD * 0.15);
        rightCol.scale.y = 1.0 + clampedD * 0.25;
      });

      group.add(lpGroup);
    },

    // =========================================================================
    // 16. METAL DISPLACEMENT (Fe + CuSO4 -> FeSO4 + Cu v)
    // =========================================================================
    buildMetalDisplacement: function(group, state) {
      var self = this;
      var mdGroup = new THREE.Group();
      mdGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.3);
      var woodMat = new THREE.MeshStandardMaterial({ color: 0x78350f, roughness: 0.8 });

      var stand = new THREE.Mesh(new THREE.BoxGeometry(2.4, 0.12, 1.0), woodMat);
      stand.position.set(0, 0.06, 0);
      mdGroup.add(stand);

      // TUBE 1: Fe nail in CuSO4 solution
      var t1Group = new THREE.Group();
      t1Group.position.set(-0.65, 0, 0);

      var beaker1 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.3, 28, 1, true), glassMat);
      beaker1.position.set(0, 0.72, 0);
      t1Group.add(beaker1);

      var solMat1 = self.getLiquidMaterial(0x0284c7, 0.85);
      var sol1 = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.85, 28), solMat1);
      sol1.position.set(0, 0.52, 0);
      t1Group.add(sol1);

      var nailGroup = new THREE.Group();
      nailGroup.position.set(0, 0.75, 0);

      var feNail = new THREE.Mesh(new THREE.CylinderGeometry(0.04, 0.04, 0.9, 16), self.getMetalMaterial(0.2, 0x64748b));
      nailGroup.add(feNail);

      var cuCoatingMat = new THREE.MeshStandardMaterial({ color: 0xc2410c, metalness: 0.85, roughness: 0.25, transparent: true, opacity: 0 });
      var cuCoating = new THREE.Mesh(new THREE.CylinderGeometry(0.045, 0.045, 0.65, 16), cuCoatingMat);
      cuCoating.position.set(0, -0.12, 0);
      nailGroup.add(cuCoating);
      t1Group.add(nailGroup);
      mdGroup.add(t1Group);

      // TUBE 2: Cu wire spiral in AgNO3 solution
      var t2Group = new THREE.Group();
      t2Group.position.set(0.65, 0, 0);

      var beaker2 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.3, 28, 1, true), glassMat);
      beaker2.position.set(0, 0.72, 0);
      t2Group.add(beaker2);

      var solMat2 = self.getLiquidMaterial(0xdbeafe, 0.4);
      var sol2 = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.85, 28), solMat2);
      sol2.position.set(0, 0.52, 0);
      t2Group.add(sol2);

      var wireGroup = new THREE.Group();
      wireGroup.position.set(0, 0.75, 0);

      var cuWire = new THREE.Mesh(new THREE.TorusGeometry(0.18, 0.025, 12, 32), new THREE.MeshStandardMaterial({ color: 0xea580c, metalness: 0.85, roughness: 0.2 }));
      cuWire.rotation.x = Math.PI / 2;
      wireGroup.add(cuWire);

      var agMat = new THREE.MeshStandardMaterial({ color: 0xe2e8f0, metalness: 0.9, roughness: 0.1, transparent: true, opacity: 0 });
      var agCrystals = new THREE.Mesh(new THREE.TorusGeometry(0.185, 0.038, 12, 32), agMat);
      agCrystals.rotation.x = Math.PI / 2;
      wireGroup.add(agCrystals);

      t2Group.add(wireGroup);
      mdGroup.add(t2Group);

      self.registerInteractive(stand, 'Giá phản ứng: Nhấp chuột để Bắt đầu phản ứng kim loại đẩy muối', function(st) {
        st.displaced = !st.displaced;
        self.playBellSound();
      });

      this.updateFns.push(function(st, t) {
        var isDisplaced = !!st.displaced || (st.reactTime !== undefined && st.reactTime > 2) || (st.time !== undefined && st.time > 2);
        if (isDisplaced) {
          cuCoatingMat.opacity = Math.min(0.95, cuCoatingMat.opacity + 0.025);
          solMat1.color.lerp(new THREE.Color(0x86efac), 0.02);

          agMat.opacity = Math.min(0.95, agMat.opacity + 0.025);
          solMat2.color.lerp(new THREE.Color(0x38bdf8), 0.02);
        } else {
          cuCoatingMat.opacity = Math.max(0, cuCoatingMat.opacity - 0.025);
          solMat1.color.lerp(new THREE.Color(0x0284c7), 0.02);
          agMat.opacity = Math.max(0, agMat.opacity - 0.025);
          solMat2.color.lerp(new THREE.Color(0xdbeafe), 0.02);
        }
      });

      group.add(mdGroup);
    },

    buildLightRefraction: function(group, state) {
      var self = this;
      var lrGroup = new THREE.Group();
      lrGroup.position.set(0, 0, 0);

      // Base & Pillar
      var baseMesh = new THREE.Mesh(
        new THREE.BoxGeometry(2.4, 0.12, 1.4),
        self.getMetalMaterial(0.4, 0x1e293b)
      );
      baseMesh.position.set(0, 0.06, 0);
      baseMesh.castShadow = true;
      lrGroup.add(baseMesh);

      // Protractor Disc (Center at O = (0, 1.0, 0))
      var discCanvas = document.createElement('canvas');
      discCanvas.width = 1024;
      discCanvas.height = 1024;
      var dCtx = discCanvas.getContext('2d');
      var cX = 512, cY = 512, dR = 460;

      dCtx.fillStyle = '#0a0f1d';
      dCtx.beginPath();
      dCtx.arc(cX, cY, dR, 0, Math.PI * 2);
      dCtx.fill();

      // Outer rim
      dCtx.strokeStyle = '#38bdf8';
      dCtx.lineWidth = 6;
      dCtx.beginPath();
      dCtx.arc(cX, cY, dR - 8, 0, Math.PI * 2);
      dCtx.stroke();

      // Normal Line (N - N') Vertical Dashed through center
      dCtx.strokeStyle = '#f8fafc';
      dCtx.lineWidth = 4;
      dCtx.setLineDash([12, 10]);
      dCtx.beginPath();
      dCtx.moveTo(cX, cY - dR + 25);
      dCtx.lineTo(cX, cY + dR - 25);
      dCtx.stroke();
      dCtx.setLineDash([]);

      // Interface Line (Horizontal)
      dCtx.strokeStyle = '#0284c7';
      dCtx.lineWidth = 5;
      dCtx.beginPath();
      dCtx.moveTo(cX - dR + 20, cY);
      dCtx.lineTo(cX + dR - 20, cY);
      dCtx.stroke();

      // Degree labels
      dCtx.fillStyle = '#94a3b8';
      dCtx.font = 'bold 22px system-ui, sans-serif';
      dCtx.textAlign = 'center';
      dCtx.textBaseline = 'middle';
      dCtx.fillText('N', cX, cY - dR + 50);
      dCtx.fillText("N'", cX, cY + dR - 50);
      dCtx.fillText('Không khí (n = 1.0)', cX - 220, cY - 180);
      dCtx.fillText('Bán trụ Thủy tinh (n = 1.51)', cX - 220, cY + 180);

      for (var deg = 0; deg <= 90; deg += 10) {
        var aRad = (deg * Math.PI) / 180;
        if (deg > 0 && deg < 90) {
          dCtx.fillStyle = '#cbd5e1';
          dCtx.fillText(deg + '°', cX - Math.sin(aRad) * (dR - 70), cY - Math.cos(aRad) * (dR - 70));
          dCtx.fillText(deg + '°', cX + Math.sin(aRad) * (dR - 70), cY - Math.cos(aRad) * (dR - 70));
          dCtx.fillText(deg + '°', cX - Math.sin(aRad) * (dR - 70), cY + Math.cos(aRad) * (dR - 70));
          dCtx.fillText(deg + '°', cX + Math.sin(aRad) * (dR - 70), cY + Math.cos(aRad) * (dR - 70));
        }
      }

      var discTex = new THREE.CanvasTexture(discCanvas);
      discTex.anisotropy = 4;
      var discMesh = new THREE.Mesh(
        new THREE.CylinderGeometry(1.48, 1.48, 0.03, 64),
        [
          new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.5 }),
          new THREE.MeshStandardMaterial({ map: discTex, roughness: 0.4 }),
          new THREE.MeshStandardMaterial({ color: 0x0f172a, roughness: 0.6 })
        ]
      );
      discMesh.rotation.x = Math.PI / 2;
      discMesh.position.set(0, 1.0, -0.02);
      lrGroup.add(discMesh);

      // Semicircular Glass Block (Flat edge at Y = 1.0, curved body in lower half Y < 1.0)
      var glassR = 0.82;
      var glassThick = 0.28;
      var semiGeo = new THREE.CylinderGeometry(glassR, glassR, glassThick, 48, 1, false, 0, Math.PI);
      var semiMat = self.getGlassMaterial(0x93c5fd, 0.6);
      semiMat.transparent = true;
      semiMat.opacity = 0.55;
      semiMat.roughness = 0.05;
      semiMat.metalness = 0.1;
      var semiGlass = new THREE.Mesh(semiGeo, semiMat);
      semiGlass.rotation.z = Math.PI;
      semiGlass.rotation.x = Math.PI / 2;
      semiGlass.position.set(0, 1.0, 0.14);
      lrGroup.add(semiGlass);

      // Laser Pointer
      var laserR = 1.25;
      var laserAssy = new THREE.Group();
      laserAssy.position.set(0, 1.0, 0.08);

      var laserBody = new THREE.Mesh(
        new THREE.CylinderGeometry(0.045, 0.055, 0.36, 16),
        self.getMetalMaterial(0.25, 0xd97706)
      );
      laserBody.position.set(0, laserR - 0.18, 0);
      laserAssy.add(laserBody);

      var laserTip = new THREE.Mesh(
        new THREE.ConeGeometry(0.04, 0.07, 16),
        self.getMetalMaterial(0.15, 0x475569)
      );
      laserTip.rotation.x = Math.PI;
      laserTip.position.set(0, laserR - 0.39, 0);
      laserAssy.add(laserTip);

      var inBeamGeo = new THREE.CylinderGeometry(0.015, 0.015, laserR - 0.41, 10);
      var inBeamMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.95 });
      var inBeamMesh = new THREE.Mesh(inBeamGeo, inBeamMat);
      inBeamMesh.position.set(0, (laserR - 0.41) / 2, 0);
      laserAssy.add(inBeamMesh);
      lrGroup.add(laserAssy);

      // Refracted Ray
      var refrRayLen = 1.1;
      var refrBeamGeo = new THREE.CylinderGeometry(0.015, 0.015, refrRayLen, 10);
      var refrBeamMat = new THREE.MeshBasicMaterial({ color: 0x2dd4bf, transparent: true, opacity: 0.95 });
      var refrBeamMesh = new THREE.Mesh(refrBeamGeo, refrBeamMat);
      lrGroup.add(refrBeamMesh);

      // Reflected Ray (for partial reflection or TIR)
      var reflBeamGeo = new THREE.CylinderGeometry(0.014, 0.014, laserR - 0.1, 10);
      var reflBeamMat = new THREE.MeshBasicMaterial({ color: 0xef4444, transparent: true, opacity: 0.6 });
      var reflBeamMesh = new THREE.Mesh(reflBeamGeo, reflBeamMat);
      lrGroup.add(reflBeamMesh);

      // Spot at O
      var spotMesh = new THREE.Mesh(new THREE.SphereGeometry(0.04, 16, 16), new THREE.MeshBasicMaterial({ color: 0xff4444 }));
      spotMesh.position.set(0, 1.0, 0.08);
      lrGroup.add(spotMesh);

      var curAngleI = 30;
      this.updateFns.push(function(st, t) {
        var targetI = (st.angle_i !== undefined) ? st.angle_i : ((st.angle !== undefined) ? st.angle : 30);
        curAngleI += (targetI - curAngleI) * 0.18;
        var iRad = (curAngleI * Math.PI) / 180;

        var dir = st.direction || 'air_to_glass';
        var nGlass = 1.51;

        if (dir === 'air_to_glass') {
          laserAssy.rotation.z = iRad;
          var sinR = (1.0 / nGlass) * Math.sin(iRad);
          var rRad = Math.asin(Math.min(1.0, sinR));

          var midX = Math.sin(rRad) * (refrRayLen / 2);
          var midY = 1.0 - Math.cos(rRad) * (refrRayLen / 2);
          refrBeamMesh.position.set(midX, midY, 0.08);
          refrBeamMesh.rotation.z = Math.PI - rRad;
          refrBeamMesh.visible = true;
          refrBeamMat.opacity = 0.95;

          var reflMidX = Math.sin(iRad) * ((laserR - 0.1) / 2);
          var reflMidY = 1.0 + Math.cos(iRad) * ((laserR - 0.1) / 2);
          reflBeamMesh.position.set(reflMidX, reflMidY, 0.08);
          reflBeamMesh.rotation.z = -iRad;
          reflBeamMesh.visible = (curAngleI > 3);
          reflBeamMat.opacity = 0.45;
        } else {
          laserAssy.rotation.z = Math.PI - iRad;
          var sinR = nGlass * Math.sin(iRad);
          if (sinR >= 1.0) {
            // Total Internal Reflection
            refrBeamMesh.visible = false;
            var reflMidX = Math.sin(iRad) * ((laserR - 0.1) / 2);
            var reflMidY = 1.0 - Math.cos(iRad) * ((laserR - 0.1) / 2);
            reflBeamMesh.position.set(reflMidX, reflMidY, 0.08);
            reflBeamMesh.rotation.z = -(Math.PI - iRad);
            reflBeamMesh.visible = true;
            reflBeamMat.opacity = 1.0;
          } else {
            var rRad = Math.asin(sinR);
            var midX = Math.sin(rRad) * (refrRayLen / 2);
            var midY = 1.0 + Math.cos(rRad) * (refrRayLen / 2);
            refrBeamMesh.position.set(midX, midY, 0.08);
            refrBeamMesh.rotation.z = -rRad;
            refrBeamMesh.visible = true;
            refrBeamMat.opacity = 0.95;

            var reflMidX = Math.sin(iRad) * ((laserR - 0.1) / 2);
            var reflMidY = 1.0 - Math.cos(iRad) * ((laserR - 0.1) / 2);
            reflBeamMesh.position.set(reflMidX, reflMidY, 0.08);
            reflBeamMesh.rotation.z = -(Math.PI - iRad);
            reflBeamMesh.visible = (curAngleI > 3);
            reflBeamMat.opacity = 0.45;
          }
        }
      });

      group.add(lrGroup);
    },

    // =========================================================================
    // 18. AIR OXYGEN FRACTION (Xác định 1/5 thể tích O2 trong không khí)
    // =========================================================================
    buildAirOxygenFraction: function(group, state) {
      var self = this;
      var aoGroup = new THREE.Group();
      aoGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.3);

      // Glass Water Basin with Red Colored Water (Chậu nước pha màu đỏ)
      var basin = new THREE.Mesh(new THREE.CylinderGeometry(1.2, 1.2, 0.5, 32, 1, true), glassMat);
      basin.position.set(0, 0.25, 0);
      aoGroup.add(basin);

      var basinLiqMat = self.getLiquidMaterial(0xf43f5e, 0.65);
      var basinLiq = new THREE.Mesh(new THREE.CylinderGeometry(1.18, 1.18, 0.35, 32), basinLiqMat);
      basinLiq.position.set(0, 0.18, 0);
      aoGroup.add(basinLiq);

      // Floating Cork Disk with Candle (Đế nổi và cây nến trắng)
      var candleFloat = new THREE.Mesh(new THREE.CylinderGeometry(0.26, 0.26, 0.08, 20), new THREE.MeshStandardMaterial({ color: 0xd97706, roughness: 0.8 }));
      candleFloat.position.set(0, 0.36, 0);
      aoGroup.add(candleFloat);

      var candle = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.28, 16), new THREE.MeshStandardMaterial({ color: 0xf8fafc }));
      candle.position.set(0, 0.54, 0);
      aoGroup.add(candle);

      var flame = new THREE.Mesh(new THREE.ConeGeometry(0.05, 0.18, 12), new THREE.MeshBasicMaterial({ color: 0xf59e0b }));
      flame.position.set(0, 0.76, 0);
      aoGroup.add(flame);

      var flameLight = new THREE.PointLight(0xf59e0b, 1.5, 3.0);
      flameLight.position.set(0, 0.76, 0);
      aoGroup.add(flameLight);

      // Inverted Graduated Measuring Cylinder (Ống đong thủy tinh 5 vạch chia mức 1/5)
      var bellJarGroup = new THREE.Group();
      bellJarGroup.position.set(0, 2.3, 0); // Starts suspended above

      var bellJar = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.7, 28, 1, true), glassMat);
      bellJar.position.set(0, 0, 0);
      bellJarGroup.add(bellJar);

      for (var r = 1; r <= 5; r++) {
        var tickRing = new THREE.Mesh(new THREE.RingGeometry(0.422, 0.432, 24), new THREE.MeshBasicMaterial({ color: 0xffffff, side: THREE.DoubleSide }));
        tickRing.rotation.x = Math.PI / 2;
        tickRing.position.set(0, -0.8 + r * 0.28, 0);
        bellJarGroup.add(tickRing);
      }
      aoGroup.add(bellJarGroup);

      // Rising Red Water Column inside cylinder (rises to exactly 1/5)
      var riseLiqMat = self.getLiquidMaterial(0xf43f5e, 0.85);
      var riseLiq = new THREE.Mesh(new THREE.CylinderGeometry(0.40, 0.40, 0.35, 24), riseLiqMat);
      riseLiq.position.set(0, 0.35, 0);
      riseLiq.scale.set(1, 0.001, 1);
      aoGroup.add(riseLiq);

      self.registerInteractive(basin, 'Ống đong: Nhấp chuột để Úp ống đong và đốt cháy O2', function(st) {
        st.airBurned = !st.airBurned;
        self.playBellSound();
      });

      // Kinematic Lowering of Cylinder and Water Rise
      var lowerAnim = 0;
      this.updateFns.push(function(st, t) {
        var isBurned = !!st.airBurned || (st.phase === "running" || st.phase === 3 || st.phase === 4 || st.phase === 5) || (st.burnProgress !== undefined && st.burnProgress > 0);
        if (isBurned) {
          lowerAnim = Math.min(1.0, lowerAnim + 0.02);

          // Lower cylinder over the candle
          bellJarGroup.position.y = THREE.MathUtils.lerp(2.3, 1.15, lowerAnim);

          // Once cylinder is fully down (lowerAnim > 0.8), flame dims and water rises
          if (lowerAnim > 0.7) {
            var flameFade = Math.max(0.001, 1.0 - (lowerAnim - 0.7) / 0.3);
            flame.scale.set(flameFade, flameFade, flameFade);
            flameLight.intensity = 1.5 * flameFade;

            // Water rises to 1/5
            riseLiq.scale.y = Math.min(1.0, (lowerAnim - 0.7) / 0.3);
            riseLiq.position.y = 0.35 + riseLiq.scale.y * 0.175;
          }
        } else {
          lowerAnim = Math.max(0, lowerAnim - 0.02);
          bellJarGroup.position.y = THREE.MathUtils.lerp(1.15, 2.3, 1.0 - lowerAnim);

          var flicker = 1.0 + Math.sin(t * 20) * 0.15;
          flame.scale.set(flicker, flicker * 1.1, flicker);
          flameLight.intensity = 1.5 * flicker;

          riseLiq.scale.y = 0.001;
          riseLiq.position.y = 0.35;
        }
      });

      group.add(aoGroup);
    },

    buildHydrocarbonBromine: function(group, state) {
      var self = this;
      var hbGroup = new THREE.Group();
      hbGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.3);

      // Bottle 1: CH4
      var b1Group = new THREE.Group();
      b1Group.position.set(-0.9, 0, 0);

      var b1 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.4, 24, 1, true), glassMat);
      b1.position.set(0, 0.75, 0);
      b1Group.add(b1);

      var b1Liq = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.85, 24), self.getLiquidMaterial(0xea580c, 0.85));
      b1Liq.position.set(0, 0.55, 0);
      b1Group.add(b1Liq);

      var tube1 = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.6, 12), glassMat);
      tube1.position.set(0, 1.0, 0);
      b1Group.add(tube1);

      var bubbles1 = [];
      var bMat = new THREE.MeshBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.75 });
      for (var b = 0; b < 12; b++) {
        var bm1 = new THREE.Mesh(new THREE.SphereGeometry(0.02 + Math.random() * 0.02, 8, 8), bMat);
        bm1.position.set((Math.random() - 0.5) * 0.25, 0.2 + Math.random() * 0.6, (Math.random() - 0.5) * 0.25);
        b1Group.add(bm1);
        bubbles1.push({ mesh: bm1, speed: 0.015 + Math.random() * 0.02 });
      }
      hbGroup.add(b1Group);

      // Bottle 2: C2H4
      var b2Group = new THREE.Group();
      b2Group.position.set(0.9, 0, 0);

      var b2 = new THREE.Mesh(new THREE.CylinderGeometry(0.42, 0.42, 1.4, 24, 1, true), glassMat);
      b2.position.set(0, 0.75, 0);
      b2Group.add(b2);

      var b2Mat = self.getLiquidMaterial(0xea580c, 0.85);
      var b2Liq = new THREE.Mesh(new THREE.CylinderGeometry(0.4, 0.4, 0.85, 24), b2Mat);
      b2Liq.position.set(0, 0.55, 0);
      b2Group.add(b2Liq);

      var tube2 = new THREE.Mesh(new THREE.CylinderGeometry(0.03, 0.03, 1.6, 12), glassMat);
      tube2.position.set(0, 1.0, 0);
      b2Group.add(tube2);

      var bubbles2 = [];
      for (var b = 0; b < 16; b++) {
        var bm2 = new THREE.Mesh(new THREE.SphereGeometry(0.02 + Math.random() * 0.02, 8, 8), bMat);
        bm2.position.set((Math.random() - 0.5) * 0.25, 0.2 + Math.random() * 0.6, (Math.random() - 0.5) * 0.25);
        b2Group.add(bm2);
        bubbles2.push({ mesh: bm2, speed: 0.020 + Math.random() * 0.02 });
      }
      hbGroup.add(b2Group);

      self.registerInteractive(b2, 'Bình sục khí C2H4: Nhấp chuột để Sục khí làm mất màu nước Brom', function(st) {
        st.bromineDecolorized = !st.bromineDecolorized;
        self.playBoilSound();
      });

      this.updateFns.push(function(st, t) {
        var isFlowing = !!(st && st.isFlowing);
        var isDecolor = !!st.bromineDecolorized || (st.isFlowing && st.gas === "C2H4") || (st.colorFactor !== undefined && st.colorFactor < 0.5);

        if (isFlowing) {
          bubbles1.forEach(function(bObj) {
            bObj.mesh.visible = true;
            bObj.mesh.position.y += bObj.speed;
            if (bObj.mesh.position.y > 0.95) bObj.mesh.position.y = 0.2;
          });
          bubbles2.forEach(function(bObj) {
            bObj.mesh.visible = true;
            bObj.mesh.position.y += bObj.speed;
            if (bObj.mesh.position.y > 0.95) bObj.mesh.position.y = 0.2;
          });
        } else {
          bubbles1.forEach(function(bObj) { bObj.mesh.visible = false; });
          bubbles2.forEach(function(bObj) { bObj.mesh.visible = false; });
        }

        if (isDecolor) {
          b2Mat.color.lerp(new THREE.Color(0xdbeafe), 0.035);
          b2Mat.opacity = Math.max(0.28, b2Mat.opacity - 0.025);
        } else {
          b2Mat.color.lerp(new THREE.Color(0xea580c), 0.035);
          b2Mat.opacity = Math.min(0.85, b2Mat.opacity + 0.025);
        }
      });

      group.add(hbGroup);
    },

    buildFrictionForce: function(group, state) {
      var self = this;
      var fGroup = new THREE.Group();
      fGroup.position.set(0, 0.3, 0);

      // Test Track
      var track = new THREE.Mesh(new THREE.BoxGeometry(4.4, 0.12, 1.2), new THREE.MeshStandardMaterial({ color: 0x334155, roughness: 0.7 }));
      track.position.set(0, 0.06, 0);
      fGroup.add(track);

      // Wooden Block
      var block = new THREE.Mesh(new THREE.BoxGeometry(0.9, 0.45, 0.6), new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.6 }));
      block.position.set(-0.6, 0.34, 0);
      fGroup.add(block);

      // Dynamometer (Lực kế lò xo kéo)
      var dyna = new THREE.Mesh(new THREE.CylinderGeometry(0.08, 0.08, 1.4, 16), self.getGlassMaterial(0xdbeafe, 0.5));
      dyna.rotation.z = Math.PI / 2;
      dyna.position.set(0.7, 0.34, 0);
      fGroup.add(dyna);

      self.registerInteractive(block, 'Khối gỗ: Nhấp chuột để Kéo trượt kiểm tra lực ma sát', function(st) {
        st.sliding = !st.sliding;
        self.playSwitchSound();
      });

      this.updateFns.push(function(st, t) {
        var isMoving = !!st.sliding || !!st.isPulling;
        if (isMoving) {
          var xOff = Math.sin(t * 3) * 0.4;
          block.position.x = -0.6 + xOff;
          dyna.position.x = 0.7 + xOff;
        } else {
          block.position.x += (-0.6 - block.position.x) * 0.1;
          dyna.position.x += (0.7 - dyna.position.x) * 0.1;
        }
      });

      group.add(fGroup);
    },

    // =========================================================================
    // UNIVERSAL LAB STAND (Fallback)
    // =========================================================================
    buildUniversalLabStand: function(group, simType, state) {
      var self = this;
      var uGroup = new THREE.Group();
      uGroup.position.set(0, 0, 0);

      var glassMat = this.getGlassMaterial(0xdbeafe, 0.35);

      var rackBase = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.12, 1.0), new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.7 }));
      rackBase.position.set(0, 0.06, 0);
      uGroup.add(rackBase);

      var rackTop = new THREE.Mesh(new THREE.BoxGeometry(2.8, 0.08, 1.0), new THREE.MeshStandardMaterial({ color: 0xb45309, roughness: 0.7 }));
      rackTop.position.set(0, 1.2, 0);
      uGroup.add(rackTop);

      var tubeColors = [0xef4444, 0x3b82f6, 0x10b981, 0xf59e0b];
      for (var i = 0; i < 4; i++) {
        var posX = -0.9 + i * 0.6;
        var tubeMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.14, 0.14, 1.4, 24, 1, true), glassMat);
        tubeMesh.position.set(posX, 0.85, 0);
        uGroup.add(tubeMesh);

        var liqMesh = new THREE.Mesh(new THREE.CylinderGeometry(0.13, 0.13, 0.8, 24), self.getLiquidMaterial(tubeColors[i], 0.75));
        liqMesh.position.set(posX, 0.55, 0);
        uGroup.add(liqMesh);
      }

      this.updateFns.push(function(st, t) {
        uGroup.rotation.y = Math.sin(t * 0.4) * 0.08;
      });

      group.add(uGroup);
    },

    // -------------------------------------------------------------------------
    // RENDER LOOP & LIFECYCLE
    // -------------------------------------------------------------------------
    startLoop: function() {
      var self = this;
      var clock = new THREE.Clock();

      function animate() {
        self.animFrameId = requestAnimationFrame(animate);

        var delta = clock.getDelta();
        var t = clock.getElapsedTime();

        if (self.targetCamPos && self.camera && self.controls) {
          self.camera.position.lerp(self.targetCamPos, 0.08);
          self.controls.target.lerp(self.targetLookAt, 0.08);
          if (self.camera.position.distanceTo(self.targetCamPos) < 0.02) {
            self.targetCamPos = null;
            self.targetLookAt = null;
          }
        }

        if (self.controls) {
          self.controls.update();
        }

        var activeState = self.currentSimState || window.labSimState || {};
        for (var i = 0; i < self.updateFns.length; i++) {
          try {
            self.updateFns[i](activeState, t);
          } catch (e) {}
        }

        if (self.renderer && self.scene && self.camera) {
          self.renderer.render(self.scene, self.camera);
        }
      }

      animate();
    },

    update: function(state, t) {
      if (state) {
        this.currentSimState = state;
        window.labSimState = state;
      }
      var activeState = this.currentSimState || window.labSimState || {};
      for (var i = 0; i < this.updateFns.length; i++) {
        try {
          this.updateFns[i](activeState, t !== undefined ? t : (performance.now() * 0.001));
        } catch (e) {}
      }
    },

    resize: function() {
      if (!this.container || !this.renderer || !this.camera) return;
      var width = this.container.clientWidth || 640;
      var height = this.container.clientHeight || 390;
      this.camera.aspect = width / height;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(width, height);
    },

    showRunStatusHUD: function(text, isComplete, isPaused) {
      if (!this.container) return;
      var hud = document.getElementById('lab3DRunStatusHUD');
      if (!text) {
        if (hud && hud.parentNode) hud.parentNode.removeChild(hud);
        return;
      }
      if (!hud) {
        hud = document.createElement('div');
        hud.id = 'lab3DRunStatusHUD';
        hud.style.cssText = 'position:absolute;top:14px;left:50%;transform:translateX(-50%);background:rgba(15,23,42,0.92);backdrop-filter:blur(10px);border:1px solid #10b981;border-radius:24px;padding:7px 18px;color:#f8fafc;font-size:12px;font-weight:700;box-shadow:0 10px 25px rgba(0,0,0,0.6);pointer-events:none;z-index:25;display:flex;align-items:center;gap:8px;white-space:nowrap;transition:all 0.25s ease;';
        this.container.style.position = 'relative';
        this.container.appendChild(hud);
      }
      if (isComplete) {
        hud.style.borderColor = '#10b981';
        hud.style.background = 'rgba(6,78,59,0.92)';
        hud.innerHTML = '<span style="font-size:14px">🎉</span> <span>' + text + '</span>';
      } else if (isPaused) {
        hud.style.borderColor = '#f59e0b';
        hud.style.background = 'rgba(120,53,15,0.92)';
        hud.innerHTML = '<span style="color:#f59e0b;font-size:13px">⏸</span> <span>' + text + '</span>';
      } else {
        hud.style.borderColor = '#38bdf8';
        hud.style.background = 'rgba(15,23,42,0.92)';
        hud.innerHTML = '<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;"></span> <span>' + text + '</span>';
      }
    },

    destroy: function() {
      if (this.animFrameId) {
        cancelAnimationFrame(this.animFrameId);
        this.animFrameId = null;
      }
      if (this._onResize) {
        window.removeEventListener('resize', this._onResize);
        this._onResize = null;
      }
      if (this.renderer && this.renderer.domElement) {
        if (this._onPointerMove) {
          this.renderer.domElement.removeEventListener('mousemove', this._onPointerMove);
        }
        if (this._onPointerDown) {
          this.renderer.domElement.removeEventListener('click', this._onPointerDown);
        }
      }
      if (this.tooltipEl && this.tooltipEl.parentNode) {
        this.tooltipEl.parentNode.removeChild(this.tooltipEl);
        this.tooltipEl = null;
      }
      var rHud = document.getElementById('lab3DRunStatusHUD'); if (rHud && rHud.parentNode) rHud.parentNode.removeChild(rHud);
      var sHud = document.getElementById('lab3DSpringHUD');
      if (sHud && sHud.parentNode) {
        sHud.parentNode.removeChild(sHud);
      }
      if (this.controls) {
        this.controls.dispose();
        this.controls = null;
      }
      if (this.renderer) {
        this.renderer.dispose();
        if (this.renderer.domElement && this.renderer.domElement.parentNode) {
          this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }
        this.renderer = null;
      }
      this.scene = null;
      this.camera = null;
      this.simGroup = null;
      this.updateFns = [];
      this.dynamicLights = [];
      this.interactiveObjects = [];
      this.isInitialized = false;
    }
  };

  window.Lab3DEngine = Lab3DEngine;
})(window);
