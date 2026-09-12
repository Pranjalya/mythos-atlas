/**
 * Three.js 3D Spatio-Temporal Globe Presentation Layer.
 * Renders an interactive celestial sphere with atmospheric shaders,
 * InstancedMesh myth nodes, animated syncretic Bezier arcs, and smooth camera controls.
 */

import * as THREE from 'three';
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { store, ActiveMyth } from '../state/store.ts';

const GLOBE_RADIUS = 100;
const NODE_ELEVATION = 101.2;
const MAX_INSTANCES = 200;

// Civilizational color palette
export const CULTURE_COLORS: Record<string, string> = {
  Mesopotamian: '#E6B86A', // Ancient Gold
  Levantine: '#F4A261',    // Bronze Amber
  Egyptian: '#E76F51',     // Terracotta Sun
  Vedic: '#48CAE4',        // Celestial Cyan
  'Greco-Roman': '#00B4D8', // Aegean Blue
  Norse: '#90E0EF',        // Glacial Frost
  Mesoamerican: '#2A9D8F', // Jade Quetzal
  'East Asian': '#E63946', // Imperial Vermilion
  Celtic: '#52B788',       // Forest Emerald
  'West African': '#F77F00',// Saharan Gold
  Oceanic: '#06D6A0',      // Pacific Aqua
  Andean: '#FFB703',       // Incan Sun
  Default: '#E6B86A',
};

export class MythosGlobe {
  private container: HTMLElement;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;

  private globeMesh: THREE.Mesh | null = null;
  private atmosphereMesh: THREE.Mesh | null = null;
  private instancedNodes: THREE.InstancedMesh | null = null;
  private arcsGroup: THREE.Group = new THREE.Group();
  private beaconGroup: THREE.Group = new THREE.Group();

  private raycaster = new THREE.Raycaster();
  private mouse = new THREE.Vector2();
  private hoveredIndex: number = -1;
  private currentActiveList: ActiveMyth[] = [];

  private tooltipEl: HTMLElement | null = null;
  private tooltipName: HTMLElement | null = null;
  private tooltipCulture: HTMLElement | null = null;
  private tooltipEpoch: HTMLElement | null = null;
  private tooltipArchetype: HTMLElement | null = null;

  private dummy = new THREE.Object3D();
  private animationFrameId: number = 0;
  private arcTime: number = 0;

  constructor(containerId: string) {
    const el = document.getElementById(containerId);
    if (!el) throw new Error(`Container #${containerId} not found`);
    this.container = el;

    // Scene & Camera
    this.scene = new THREE.Scene();
    this.camera = new THREE.PerspectiveCamera(
      45,
      window.innerWidth / window.innerHeight,
      1,
      2000
    );
    this.camera.position.set(0, 50, 260);

    // WebGL Renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // OrbitControls
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 125;
    this.controls.maxDistance = 450;
    this.controls.rotateSpeed = 0.6;
    this.controls.zoomSpeed = 0.8;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.25;

    this.initLighting();
    this.initStarfield();
    this.initGlobe();
    this.initAtmosphere();
    this.initInstancedNodes();
    this.scene.add(this.arcsGroup);
    this.scene.add(this.beaconGroup);

    this.initTooltips();
    this.initEventListeners();
    this.animate();
  }

  private initLighting(): void {
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
    this.scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xfffaed, 1.4);
    dirLight1.position.set(200, 150, 200);
    this.scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0x48cae4, 0.5);
    dirLight2.position.set(-200, -100, -150);
    this.scene.add(dirLight2);
  }

  private initStarfield(): void {
    const starCount = 2000;
    const geometry = new THREE.BufferGeometry();
    const positions = new Float32Array(starCount * 3);
    const colors = new Float32Array(starCount * 3);

    for (let i = 0; i < starCount; i++) {
      const radius = 600 + Math.random() * 800;
      const theta = Math.random() * Math.PI * 2;
      const phi = Math.acos(Math.random() * 2 - 1);

      positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);
      positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta);
      positions[i * 3 + 2] = radius * Math.cos(phi);

      // Celestial gold and starlight white tinting
      const isGold = Math.random() > 0.8;
      colors[i * 3] = isGold ? 0.95 : 0.8;
      colors[i * 3 + 1] = isGold ? 0.85 : 0.85;
      colors[i * 3 + 2] = isGold ? 0.65 : 1.0;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geometry.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    const material = new THREE.PointsMaterial({
      size: 1.8,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
    });

    const starPoints = new THREE.Points(geometry, material);
    this.scene.add(starPoints);
  }

  private createEarthCanvas(): HTMLCanvasElement {
    const canvas = document.createElement('canvas');
    canvas.width = 2048;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d')!;

    // Deep cosmic ocean base
    const oceanGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    oceanGrad.addColorStop(0, '#060a17');
    oceanGrad.addColorStop(0.5, '#0b1329');
    oceanGrad.addColorStop(1, '#060a17');
    ctx.fillStyle = oceanGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Latitude & Longitude graticules
    ctx.strokeStyle = 'rgba(72, 202, 228, 0.08)';
    ctx.lineWidth = 1;

    // Latitudes
    for (let lat = -80; lat <= 80; lat += 20) {
      const y = ((90 - lat) / 180) * canvas.height;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }

    // Longitudes
    for (let lng = -180; lng <= 180; lng += 30) {
      const x = ((lng + 180) / 360) * canvas.width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }

    // Equator & Prime Meridian highlight
    ctx.strokeStyle = 'rgba(230, 184, 106, 0.2)';
    ctx.lineWidth = 1.5;
    const eqY = 0.5 * canvas.height;
    ctx.beginPath();
    ctx.moveTo(0, eqY);
    ctx.lineTo(canvas.width, eqY);
    ctx.stroke();

    const primeX = 0.5 * canvas.width;
    ctx.beginPath();
    ctx.moveTo(primeX, 0);
    ctx.lineTo(primeX, canvas.height);
    ctx.stroke();

    // Procedural glowing continental silhouettes
    ctx.fillStyle = 'rgba(230, 184, 106, 0.12)';
    ctx.strokeStyle = 'rgba(230, 184, 106, 0.28)';
    ctx.lineWidth = 2;

    const drawContinent = (coords: [number, number][]) => {
      ctx.beginPath();
      coords.forEach(([lng, lat], idx) => {
        const x = ((lng + 180) / 360) * canvas.width;
        const y = ((90 - lat) / 180) * canvas.height;
        if (idx === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
      });
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    };

    // Eurasia & Africa simplified land polygon
    drawContinent([
      [-10, 36], [0, 50], [20, 65], [60, 70], [100, 75], [140, 70], [170, 60],
      [140, 35], [120, 20], [105, 10], [80, 8], [60, 25], [45, 15], [50, -5],
      [40, -30], [20, -35], [10, -10], [-15, 12], [-10, 36]
    ]);

    // Americas simplified polygon
    drawContinent([
      [-160, 65], [-120, 68], [-80, 70], [-60, 50], [-75, 30], [-95, 20],
      [-80, 8], [-75, -15], [-70, -50], [-55, -20], [-35, -5], [-50, 10],
      [-75, 25], [-120, 35], [-130, 50], [-160, 65]
    ]);

    // Australia simplified polygon
    drawContinent([
      [115, -20], [135, -12], [150, -22], [145, -38], [115, -35], [115, -20]
    ]);

    return canvas;
  }

  private initGlobe(): void {
    const sphereGeo = new THREE.SphereGeometry(GLOBE_RADIUS, 64, 64);
    const canvas = this.createEarthCanvas();
    const texture = new THREE.CanvasTexture(canvas);

    const material = new THREE.MeshStandardMaterial({
      map: texture,
      roughness: 0.7,
      metalness: 0.2,
    });

    this.globeMesh = new THREE.Mesh(sphereGeo, material);
    this.scene.add(this.globeMesh);
  }

  private initAtmosphere(): void {
    // Atmospheric twilight Fresnel glow shader
    const vertexShader = `
      varying vec3 vNormal;
      void main() {
        vNormal = normalize(normalMatrix * normal);
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }
    `;

    const fragmentShader = `
      varying vec3 vNormal;
      void main() {
        float intensity = pow(0.65 - dot(vNormal, vec3(0.0, 0.0, 1.0)), 2.5);
        vec3 atmosphereColor = mix(vec3(0.9, 0.72, 0.41), vec3(0.28, 0.79, 0.89), vNormal.y * 0.5 + 0.5);
        gl_FragColor = vec4(atmosphereColor, 1.0) * intensity;
      }
    `;

    const atmosGeo = new THREE.SphereGeometry(GLOBE_RADIUS * 1.15, 64, 64);
    const atmosMat = new THREE.ShaderMaterial({
      vertexShader,
      fragmentShader,
      blending: THREE.AdditiveBlending,
      side: THREE.BackSide,
      transparent: true,
    });

    this.atmosphereMesh = new THREE.Mesh(atmosGeo, atmosMat);
    this.scene.add(this.atmosphereMesh);
  }

  private initInstancedNodes(): void {
    const markerGeo = new THREE.SphereGeometry(1.6, 16, 16);
    const markerMat = new THREE.MeshStandardMaterial({
      roughness: 0.3,
      metalness: 0.8,
      emissive: new THREE.Color(0x332211),
      emissiveIntensity: 0.6,
    });

    this.instancedNodes = new THREE.InstancedMesh(markerGeo, markerMat, MAX_INSTANCES);
    this.instancedNodes.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    this.instancedNodes.count = 0;
    this.scene.add(this.instancedNodes);
  }

  public updateActiveMyths(myths: ActiveMyth[]): void {
    this.currentActiveList = myths;
    if (!this.instancedNodes) return;

    const count = Math.min(myths.length, MAX_INSTANCES);
    this.instancedNodes.count = count;

    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const m = myths[i];
      // Convert lat/lng to 3D Cartesian coordinates
      const pos = this.geoToVector3(m.lat, m.lng, NODE_ELEVATION);

      // Visual scale based on temporal intensity
      const scale = 1.0 + (m.intensity * 1.4);
      this.dummy.position.copy(pos);
      this.dummy.scale.set(scale, scale, scale);
      this.dummy.updateMatrix();
      this.instancedNodes.setMatrixAt(i, this.dummy.matrix);

      // Color based on tradition
      const hex = CULTURE_COLORS[m.culture] || CULTURE_COLORS.Default;
      color.set(hex);
      this.instancedNodes.setColorAt(i, color);
    }

    this.instancedNodes.instanceMatrix.needsUpdate = true;
    if (this.instancedNodes.instanceColor) {
      this.instancedNodes.instanceColor.needsUpdate = true;
    }

    this.updateSyncreticArcs(myths);
  }

  private updateSyncreticArcs(myths: ActiveMyth[]): void {
    // Clear existing arcs
    while (this.arcsGroup.children.length > 0) {
      const obj = this.arcsGroup.children.pop();
      if (obj && 'geometry' in obj) {
        (obj as THREE.Mesh).geometry.dispose();
      }
    }

    if (!store.getState().showSyncretismArcs) return;

    const mythMap = new Map<string, ActiveMyth>();
    for (const m of myths) {
      mythMap.set(m.id, m);
    }

    const drawnPairs = new Set<string>();

    for (const m of myths) {
      const startPos = this.geoToVector3(m.lat, m.lng, NODE_ELEVATION);
      for (const synId of m.syncretic_ids || []) {
        const target = mythMap.get(synId);
        if (!target) continue;

        const pairKey = [m.id, target.id].sort().join(':');
        if (drawnPairs.has(pairKey)) continue;
        drawnPairs.add(pairKey);

        const endPos = this.geoToVector3(target.lat, target.lng, NODE_ELEVATION);
        this.createBezierArc(startPos, endPos, m.culture);
      }
    }
  }

  private createBezierArc(start: THREE.Vector3, end: THREE.Vector3, culture: string): void {
    // Midpoint elevated above surface
    const mid = new THREE.Vector3().addVectors(start, end).multiplyScalar(0.5);
    const distance = start.distanceTo(end);
    const altitude = GLOBE_RADIUS + Math.min(distance * 0.45, 45);
    mid.normalize().multiplyScalar(altitude);

    const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
    const points = curve.getPoints(40);
    const geometry = new THREE.BufferGeometry().setFromPoints(points);

    const hex = CULTURE_COLORS[culture] || '#E6B86A';
    const material = new THREE.LineDashedMaterial({
      color: new THREE.Color(hex),
      dashSize: 3,
      gapSize: 2,
      transparent: true,
      opacity: 0.65,
    });

    const line = new THREE.Line(geometry, material);
    line.computeLineDistances();
    this.arcsGroup.add(line);
  }

  public flyToCoordinate(lat: number, lng: number): void {
    const target = this.geoToVector3(lat, lng, 220);
    const startPos = this.camera.position.clone();
    const duration = 1200; // ms
    const startTime = performance.now();

    const animateCamera = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Smooth cubic ease out
      const ease = 1 - Math.pow(1 - progress, 3);

      this.camera.position.lerpVectors(startPos, target, ease);
      this.camera.lookAt(0, 0, 0);

      if (progress < 1) {
        requestAnimationFrame(animateCamera);
      }
    };

    requestAnimationFrame(animateCamera);
  }

  public resetView(): void {
    this.camera.position.set(0, 50, 260);
    this.camera.lookAt(0, 0, 0);
    this.controls.reset();
  }

  public geoToVector3(lat: number, lng: number, radius: number = GLOBE_RADIUS): THREE.Vector3 {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lng + 180) * (Math.PI / 180);

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const y = radius * Math.cos(phi);
    const z = radius * Math.sin(phi) * Math.sin(theta);

    return new THREE.Vector3(x, y, z);
  }

  private initTooltips(): void {
    this.tooltipEl = document.getElementById('hover-tooltip');
    this.tooltipName = document.getElementById('tooltip-name');
    this.tooltipCulture = document.getElementById('tooltip-culture');
    this.tooltipEpoch = document.getElementById('tooltip-epoch');
    this.tooltipArchetype = document.getElementById('tooltip-archetype');
  }

  private initEventListeners(): void {
    window.addEventListener('resize', this.onWindowResize.bind(this));

    this.container.addEventListener('mousemove', (event) => {
      const rect = this.container.getBoundingClientRect();
      this.mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      this.mouse.y = -(((event.clientY - rect.top) / rect.height) * 2 - 1);
      this.checkRaycastHover(event.clientX, event.clientY);
    });

    this.container.addEventListener('click', () => {
      if (this.hoveredIndex >= 0 && this.hoveredIndex < this.currentActiveList.length) {
        const clicked = this.currentActiveList[this.hoveredIndex];
        store.selectMyth(clicked.id);
        this.flyToCoordinate(clicked.lat, clicked.lng);
      }
    });
  }

  private checkRaycastHover(clientX: number, clientY: number): void {
    if (!this.instancedNodes || this.currentActiveList.length === 0) return;

    this.raycaster.setFromCamera(this.mouse, this.camera);
    const intersects = this.raycaster.intersectObject(this.instancedNodes);

    if (intersects.length > 0 && intersects[0].instanceId !== undefined) {
      const idx = intersects[0].instanceId;
      if (idx < this.currentActiveList.length) {
        this.hoveredIndex = idx;
        const myth = this.currentActiveList[idx];
        this.showTooltip(myth, clientX, clientY);
        document.body.style.cursor = 'pointer';
        return;
      }
    }

    this.hoveredIndex = -1;
    this.hideTooltip();
    document.body.style.cursor = 'default';
  }

  private showTooltip(myth: ActiveMyth, x: number, y: number): void {
    if (!this.tooltipEl) return;
    if (this.tooltipName) this.tooltipName.textContent = myth.name;
    if (this.tooltipCulture) this.tooltipCulture.textContent = myth.culture;
    if (this.tooltipEpoch) {
      const startStr = myth.epoch_start < 0 ? `${Math.abs(myth.epoch_start)} BCE` : `${myth.epoch_start} CE`;
      const endStr = myth.epoch_end < 0 ? `${Math.abs(myth.epoch_end)} BCE` : `${myth.epoch_end} CE`;
      this.tooltipEpoch.textContent = `${startStr} – ${endStr}`;
    }
    if (this.tooltipArchetype) this.tooltipArchetype.textContent = myth.archetype;

    this.tooltipEl.style.left = `${x}px`;
    this.tooltipEl.style.top = `${y}px`;
    this.tooltipEl.classList.remove('tooltip-hidden');
  }

  private hideTooltip(): void {
    if (this.tooltipEl) {
      this.tooltipEl.classList.add('tooltip-hidden');
    }
  }

  private onWindowResize(): void {
    this.camera.aspect = window.innerWidth / window.innerHeight;
    this.camera.updateProjectionMatrix();
    this.renderer.setSize(window.innerWidth, window.innerHeight);
  }

  private animate = (): void => {
    this.animationFrameId = requestAnimationFrame(this.animate);
    this.controls.update();

    // Animate dashed lines in syncretic arcs
    this.arcTime += 0.02;
    this.arcsGroup.children.forEach((child) => {
      if (child instanceof THREE.Line && child.material instanceof THREE.LineDashedMaterial) {
        // Subtle opacity pulsation
        child.material.opacity = 0.5 + 0.3 * Math.sin(this.arcTime);
      }
    });

    this.renderer.render(this.scene, this.camera);
  };

  public destroy(): void {
    cancelAnimationFrame(this.animationFrameId);
    window.removeEventListener('resize', this.onWindowResize);
    this.renderer.dispose();
  }
}
