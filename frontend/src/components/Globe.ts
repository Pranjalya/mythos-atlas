/**
 * Three.js 3D Modern Spatio-Temporal Globe Presentation Layer.
 * Renders an interactive celestial sphere with modern country vector boundaries,
 * realistic GeoJSON landmass textures, atmospheric Fresnel glow,
 * InstancedMesh myth nodes, animated syncretic Bezier arcs, and country hover intelligence.
 */

import * as THREE from 'three';
// @ts-ignore
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { store, ActiveMyth } from '../state/store.ts';

const GLOBE_RADIUS = 100;
const BORDER_ELEVATION = 100.18;
const NODE_ELEVATION = 101.4;
const MAX_INSTANCES = 1000;

export const CULTURE_COLORS: Record<string, string> = {
  // Near Eastern & Mediterranean
  Mesopotamian: '#E6B86A', // Ancient Cuneiform Gold
  Levantine: '#F4A261',    // Bronze Amber
  Egyptian: '#E76F51',     // Terracotta Sun / Red Ochre
  'Greco-Roman': '#00B4D8', // Aegean Blue

  // Indo-Iranian & South Asian
  'Vedic & Hindu': '#48CAE4', // Celestial Cyan / Soma Blue
  Vedic: '#48CAE4',
  'Persian & Iranian': '#C77DFF', // Imperial Sasanian Amethyst
  
  // European Traditions
  'Norse & Germanic': '#90E0EF', // Glacial Frost
  Norse: '#90E0EF',
  Celtic: '#52B788',       // Forest Druidic Emerald
  'Slavic & Baltic': '#38B000', // Sacred Oak Green
  'Finno-Ugric': '#70E000',     // Taiga Moss Lime

  // East, Central & Southeast Asian
  'East Asian': '#E63946', // Imperial Vermilion / Dragon Red
  'Central Asian & Steppe': '#FFD166', // Golden Steppe Sun
  'Southeast Asian': '#FF70A6', // Tropical Lotus Pink

  // Americas
  'North American Indigenous': '#FF9F1C', // Amber Ochre / Turquoise Feather
  Mesoamerican: '#2A9D8F', // Jade Quetzal Green
  'Andean & South American': '#FFB703', // Incan Sun Gold
  Andean: '#FFB703',

  // Africa
  'West African': '#F77F00', // Saharan Sun Gold
  'Central & Southern African': '#D62828', // Great Rift Ochre Crimson

  // Oceania & Australasia
  'Oceanic & Australasian': '#06D6A0', // Pacific Reef Aquamarine
  Oceanic: '#06D6A0',

  Default: '#E6B86A',
};

export interface CountryMeta {
  name: string;
  continent: string;
  lat: number;
  lng: number;
  bbox: [number, number, number, number]; // [minLng, minLat, maxLng, maxLat]
}

export class MythosGlobe {
  private container: HTMLElement;
  private scene: THREE.Scene;
  private camera: THREE.PerspectiveCamera;
  private renderer: THREE.WebGLRenderer;
  private controls: OrbitControls;

  private globeMesh: THREE.Mesh | null = null;
  private atmosphereMesh: THREE.Mesh | null = null;
  private countryBordersMesh: THREE.LineSegments | null = null;
  private instancedNodes: THREE.InstancedMesh | null = null;
  private arcsGroup: THREE.Group = new THREE.Group();

  private raycaster = new THREE.Raycaster();
  private mouse = new THREE.Vector2();
  private hoveredIndex: number = -1;
  private currentActiveList: ActiveMyth[] = [];
  private countriesList: CountryMeta[] = [];

  private tooltipEl: HTMLElement | null = null;
  private tooltipName: HTMLElement | null = null;
  private tooltipCulture: HTMLElement | null = null;
  private tooltipEpoch: HTMLElement | null = null;
  private tooltipCountry: HTMLElement | null = null;
  private tooltipArchetype: HTMLElement | null = null;

  private dummy = new THREE.Object3D();
  private animationFrameId: number = 0;
  private arcTime: number = 0;

  // Sacred Epicenter Constellation Bloom System
  private clusterMap = new Map<string, ActiveMyth[]>();
  private constellationGroup = new THREE.Group();
  private constellationSatellites: {
    mesh: THREE.Mesh;
    stem: THREE.Line;
    myth: ActiveMyth;
    index: number;
    basePos: THREE.Vector3;
  }[] = [];
  private activeBloomingClusterKey: string | null = null;
  private locusAnchorRing: THREE.Mesh | null = null;

  // Story Mode / Expedition Trail System
  private expeditionTrailGroup = new THREE.Group();

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
    this.renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance',
    });
    this.renderer.setSize(window.innerWidth, window.innerHeight);
    this.renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    this.container.appendChild(this.renderer.domElement);

    // OrbitControls with subtle smooth rotation
    this.controls = new OrbitControls(this.camera, this.renderer.domElement);
    this.controls.enableDamping = true;
    this.controls.dampingFactor = 0.05;
    this.controls.minDistance = 120;
    this.controls.maxDistance = 450;
    this.controls.rotateSpeed = 0.6;
    this.controls.zoomSpeed = 0.8;
    this.controls.autoRotate = true;
    this.controls.autoRotateSpeed = 0.25;

    this.initLighting();
    this.initStarfield();
    this.initAtmosphere();
    this.initInstancedNodes();
    this.scene.add(this.arcsGroup);
    this.scene.add(this.constellationGroup);
    this.scene.add(this.expeditionTrailGroup);

    this.initTooltips();
    this.initEventListeners();

    // Asynchronously load GeoJSON world data and build modern globe
    this.loadWorldDataAndBuildGlobe();

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
    const starCount = 2400;
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

      const isGold = Math.random() > 0.85;
      colors[i * 3] = isGold ? 0.95 : 0.82;
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

  private async loadWorldDataAndBuildGlobe(): Promise<void> {
    try {
      const res = await fetch('/data/world_countries.geojson');
      if (!res.ok) throw new Error(`Failed to fetch world_countries.geojson: ${res.statusText}`);
      const geojson = await res.json();

      // 1. Build modern 3D vector country boundary lines
      this.buildCountryBorders(geojson);

      // 2. Extract country metadata for hover intelligence
      this.extractCountryMetadata(geojson);

      // 3. Render modern high-definition earth texture with exact country geometries
      this.buildModernEarthTexture(geojson);
    } catch (e) {
      console.warn('Could not load world_countries.geojson, using procedural fallback:', e);
      this.buildFallbackGlobe();
    }
  }

  private buildCountryBorders(geojson: any): void {
    const linePositions: number[] = [];

    for (const f of geojson.features || []) {
      const geom = f.geometry;
      if (!geom) continue;

      const polyList =
        geom.type === 'Polygon'
          ? [geom.coordinates]
          : geom.type === 'MultiPolygon'
          ? geom.coordinates
          : [];

      for (const poly of polyList) {
        for (const ring of poly) {
          for (let i = 0; i < ring.length - 1; i++) {
            const [lng1, lat1] = ring[i];
            const [lng2, lat2] = ring[i + 1];

            // Avoid antimeridian wrap crossing
            if (Math.abs(lng2 - lng1) > 180) continue;

            const p1 = this.geoToCartesianArray(lat1, lng1, BORDER_ELEVATION);
            const p2 = this.geoToCartesianArray(lat2, lng2, BORDER_ELEVATION);
            linePositions.push(...p1, ...p2);
          }
        }
      }
    }

    const geometry = new THREE.BufferGeometry();
    geometry.setAttribute(
      'position',
      new THREE.Float32BufferAttribute(linePositions, 3)
    );

    // Glowing cyan/sky-blue border material
    const material = new THREE.LineBasicMaterial({
      color: new THREE.Color(0x38bdf8),
      transparent: true,
      opacity: 0.48,
      blending: THREE.AdditiveBlending,
    });

    this.countryBordersMesh = new THREE.LineSegments(geometry, material);
    this.countryBordersMesh.visible = store.getState().showCountryBorders;
    this.scene.add(this.countryBordersMesh);
  }

  private extractCountryMetadata(geojson: any): void {
    const list: CountryMeta[] = [];
    for (const f of geojson.features || []) {
      const p = f.properties;
      if (!p) continue;
      const name = p.NAME || p.ADMIN || 'Unknown Country';
      const continent = p.CONTINENT || p.REGION_UN || 'Global';
      const lng = typeof p.LABEL_X === 'number' ? p.LABEL_X : 0;
      const lat = typeof p.LABEL_Y === 'number' ? p.LABEL_Y : 0;
      const bbox = f.bbox || [-180, -90, 180, 90];

      list.push({ name, continent, lat, lng, bbox });
    }
    this.countriesList = list;
  }

  private buildModernEarthTexture(geojson: any): void {
    const canvas = document.createElement('canvas');
    canvas.width = 2048;
    canvas.height = 1024;
    const ctx = canvas.getContext('2d')!;

    // 1. Deep midnight oceanic gradient
    const oceanGrad = ctx.createLinearGradient(0, 0, 0, canvas.height);
    oceanGrad.addColorStop(0, '#040714');
    oceanGrad.addColorStop(0.3, '#070f26');
    oceanGrad.addColorStop(0.7, '#070f26');
    oceanGrad.addColorStop(1, '#040714');
    ctx.fillStyle = oceanGrad;
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // 2. Graticules (Latitude & Longitude gridlines)
    ctx.strokeStyle = 'rgba(56, 189, 248, 0.05)';
    ctx.lineWidth = 1;
    for (let lat = -80; lat <= 80; lat += 20) {
      const y = ((90 - lat) / 180) * canvas.height;
      ctx.beginPath();
      ctx.moveTo(0, y);
      ctx.lineTo(canvas.width, y);
      ctx.stroke();
    }
    for (let lng = -180; lng <= 180; lng += 30) {
      const x = ((lng + 180) / 360) * canvas.width;
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x, canvas.height);
      ctx.stroke();
    }

    // 3. Render all 177 modern countries onto canvas
    ctx.fillStyle = '#0c1527'; // Modern dark slate landmass
    ctx.strokeStyle = '#1e304d'; // Coastline boundary
    ctx.lineWidth = 1.2;

    for (const f of geojson.features || []) {
      const geom = f.geometry;
      if (!geom) continue;

      const polyList =
        geom.type === 'Polygon'
          ? [geom.coordinates]
          : geom.type === 'MultiPolygon'
          ? geom.coordinates
          : [];

      for (const poly of polyList) {
        for (const ring of poly) {
          ctx.beginPath();
          for (let i = 0; i < ring.length; i++) {
            const [lng, lat] = ring[i];
            const x = ((lng + 180) / 360) * canvas.width;
            const y = ((90 - lat) / 180) * canvas.height;
            if (i === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);
          }
          ctx.closePath();
          ctx.fill();
          ctx.stroke();
        }
      }
    }

    // 4. Subtle ancient & modern metropolitan night lights (starlight clusters)
    const keyCoords = [
      [31.32, 45.63], [32.53, 44.42], [30.13, 31.31], [25.72, 32.61],
      [28.61, 77.20], [25.43, 81.84], [37.98, 23.72], [41.90, 12.49],
      [19.43, -99.13], [20.68, -88.56], [34.34, 108.93], [35.67, 139.65],
      [59.32, 18.06], [51.50, -0.12], [11.55, -8.15], [6.68, -1.62],
      [-13.53, -71.96], [-33.86, 151.20], [40.71, -74.00], [-22.90, -43.17]
    ];

    for (const [lat, lng] of keyCoords) {
      const x = ((lng + 180) / 360) * canvas.width;
      const y = ((90 - lat) / 180) * canvas.height;

      const rad = ctx.createRadialGradient(x, y, 0, x, y, 12);
      rad.addColorStop(0, 'rgba(230, 184, 106, 0.7)');
      rad.addColorStop(0.4, 'rgba(230, 184, 106, 0.25)');
      rad.addColorStop(1, 'rgba(230, 184, 106, 0)');
      ctx.fillStyle = rad;
      ctx.beginPath();
      ctx.arc(x, y, 12, 0, Math.PI * 2);
      ctx.fill();
    }

    const texture = new THREE.CanvasTexture(canvas);
    texture.anisotropy = 4;

    const sphereGeo = new THREE.SphereGeometry(GLOBE_RADIUS, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      map: texture,
      roughness: 0.65,
      metalness: 0.25,
    });

    if (this.globeMesh) {
      this.scene.remove(this.globeMesh);
      this.globeMesh.geometry.dispose();
    }

    this.globeMesh = new THREE.Mesh(sphereGeo, material);
    this.scene.add(this.globeMesh);
  }

  private buildFallbackGlobe(): void {
    const sphereGeo = new THREE.SphereGeometry(GLOBE_RADIUS, 64, 64);
    const material = new THREE.MeshStandardMaterial({
      color: 0x09142b,
      roughness: 0.7,
      metalness: 0.2,
    });
    this.globeMesh = new THREE.Mesh(sphereGeo, material);
    this.scene.add(this.globeMesh);
  }

  private initAtmosphere(): void {
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
        vec3 atmosphereColor = mix(vec3(0.9, 0.72, 0.41), vec3(0.22, 0.74, 0.97), vNormal.y * 0.5 + 0.5);
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

  private beaconMesh: THREE.Mesh | null = null;

  private initInstancedNodes(): void {
    const markerGeo = new THREE.SphereGeometry(2.4, 20, 20);
    const markerMat = new THREE.MeshStandardMaterial({
      roughness: 0.25,
      metalness: 0.85,
      emissive: new THREE.Color(0x553311),
      emissiveIntensity: 0.8,
    });

    this.instancedNodes = new THREE.InstancedMesh(markerGeo, markerMat, MAX_INSTANCES);
    this.instancedNodes.instanceMatrix.setUsage(THREE.DynamicDrawUsage);
    this.instancedNodes.count = 0;
    this.scene.add(this.instancedNodes);

    // Glowing selection beacon ring
    const ringGeo = new THREE.RingGeometry(3.4, 4.8, 32);
    const ringMat = new THREE.MeshBasicMaterial({
      color: 0xfde047,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });
    this.beaconMesh = new THREE.Mesh(ringGeo, ringMat);
    this.beaconMesh.visible = false;
    this.scene.add(this.beaconMesh);
  }

  public updateActiveMyths(myths: ActiveMyth[]): void {
    this.currentActiveList = myths;

    // Group active myths by coordinate locus (within ~0.15 deg)
    this.clusterMap.clear();
    for (const m of myths) {
      const key = `${m.lat.toFixed(2)},${m.lng.toFixed(2)}`;
      let list = this.clusterMap.get(key);
      if (!list) {
        list = [];
        this.clusterMap.set(key, list);
      }
      list.push(m);
    }

    if (!this.instancedNodes) return;

    const count = Math.min(myths.length, MAX_INSTANCES);
    this.instancedNodes.count = count;

    const color = new THREE.Color();

    for (let i = 0; i < count; i++) {
      const m = myths[i];
      const pos = this.geoToVector3(m.lat, m.lng, NODE_ELEVATION);
      const key = `${m.lat.toFixed(2)},${m.lng.toFixed(2)}`;
      const cluster = this.clusterMap.get(key) || [];
      const isCluster = cluster.length > 1;

      // Multi-narrative epicenters receive a majestic scale boost
      const scale = (isCluster ? 1.45 : 1.0) + m.intensity * 1.4;

      this.dummy.position.copy(pos);
      this.dummy.scale.set(scale, scale, scale);
      this.dummy.updateMatrix();
      this.instancedNodes.setMatrixAt(i, this.dummy.matrix);

      const hex = CULTURE_COLORS[m.culture] || CULTURE_COLORS.Default;
      color.set(hex);
      this.instancedNodes.setColorAt(i, color);
    }

    this.instancedNodes.instanceMatrix.needsUpdate = true;
    if (this.instancedNodes.instanceColor) {
      this.instancedNodes.instanceColor.needsUpdate = true;
    }

    // If currently blooming a cluster, re-sync with active list
    if (this.activeBloomingClusterKey) {
      const activeCluster = this.clusterMap.get(this.activeBloomingClusterKey);
      if (!activeCluster || activeCluster.length <= 1) {
        this.retractConstellation();
      }
    }

    this.updateSyncreticArcs(myths);
  }

  private updateSyncreticArcs(myths: ActiveMyth[]): void {
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

  public toggleCountryBorders(visible: boolean): void {
    if (this.countryBordersMesh) {
      this.countryBordersMesh.visible = visible;
    }
  }

  public flyToCoordinate(lat: number, lng: number): void {
    const isDesktop = window.innerWidth > 900;
    // Desktop: offset camera slightly East (lng + 15°) so locus is framed in the open viewport to the left of the Inspector
    // Mobile: offset camera slightly South (lat - 12°) so locus sits cleanly in upper screen above bottom sheet
    const lngOffset = isDesktop ? 15 : 0;
    const latOffset = isDesktop ? 0 : -12;
    const targetLat = Math.max(-80, Math.min(80, lat + latOffset));
    const target = this.geoToVector3(targetLat, lng + lngOffset, 235);
    const startPos = this.camera.position.clone();
    const duration = 1100;
    const startTime = performance.now();

    const animateCamera = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);

      this.camera.position.lerpVectors(startPos, target, ease);
      this.camera.lookAt(0, 0, 0);
      this.controls.target.set(0, 0, 0);

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

  public cinematicFlyToCoordinate(
    lat: number,
    lng: number,
    duration: number = 1800,
    onComplete?: () => void
  ): void {
    const isDesktop = window.innerWidth > 900;
    const lngOffset = isDesktop ? 15 : 0;
    const latOffset = isDesktop ? 0 : -12;
    const targetLat = Math.max(-80, Math.min(80, lat + latOffset));
    const target = this.geoToVector3(targetLat, lng + lngOffset, 225);
    const startPos = this.camera.position.clone();
    const startTime = performance.now();

    // Parabolic orbital ascent: arc higher into space mid-flight for sweeping documentary feel
    const mid = new THREE.Vector3().addVectors(startPos, target).multiplyScalar(0.5);
    const chordDist = startPos.distanceTo(target);
    const peakAltitude = 230 + Math.min(chordDist * 0.28, 70);
    mid.normalize().multiplyScalar(peakAltitude);

    const curve = new THREE.QuadraticBezierCurve3(startPos, mid, target);

    const animateCamera = (currentTime: number) => {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Smooth sinusoidal cubic easing
      const ease = progress < 0.5
        ? 4 * progress * progress * progress
        : 1 - Math.pow(-2 * progress + 2, 3) / 2;

      const currentPos = curve.getPoint(ease);
      this.camera.position.copy(currentPos);
      this.camera.lookAt(0, 0, 0);
      this.controls.target.set(0, 0, 0);

      if (progress < 1) {
        requestAnimationFrame(animateCamera);
      } else {
        if (onComplete) onComplete();
      }
    };

    requestAnimationFrame(animateCamera);
  }

  public renderExpeditionTrail(
    stops: { lat: number; lng: number }[],
    currentStopIndex: number
  ): void {
    this.clearExpeditionTrail();

    if (!stops || stops.length === 0) return;

    // 1. Draw glowing golden parabolic arcs between all visited waypoints
    for (let i = 0; i < currentStopIndex && i < stops.length - 1; i++) {
      const s1 = stops[i];
      const s2 = stops[i + 1];

      const start = this.geoToVector3(s1.lat, s1.lng, NODE_ELEVATION + 0.3);
      const end = this.geoToVector3(s2.lat, s2.lng, NODE_ELEVATION + 0.3);

      const mid = new THREE.Vector3().addVectors(start, end).multiplyScalar(0.5);
      const dist = start.distanceTo(end);
      const arcAltitude = GLOBE_RADIUS + Math.min(dist * 0.35, 38);
      mid.normalize().multiplyScalar(arcAltitude);

      const curve = new THREE.QuadraticBezierCurve3(start, mid, end);
      const points = curve.getPoints(50);
      const geometry = new THREE.BufferGeometry().setFromPoints(points);

      const material = new THREE.LineBasicMaterial({
        color: new THREE.Color('#FFD166'),
        transparent: true,
        opacity: 0.85,
        linewidth: 2,
      });

      const line = new THREE.Line(geometry, material);
      this.expeditionTrailGroup.add(line);
    }

    // 2. Add waypoint milestone markers for all visited stops
    for (let i = 0; i <= currentStopIndex && i < stops.length; i++) {
      const s = stops[i];
      const isCurrent = i === currentStopIndex;
      const pos = this.geoToVector3(s.lat, s.lng, NODE_ELEVATION + 0.5);

      // Sphere beacon
      const markerGeo = new THREE.SphereGeometry(isCurrent ? 1.8 : 1.2, 16, 16);
      const markerMat = new THREE.MeshBasicMaterial({
        color: new THREE.Color(isCurrent ? '#FFE57F' : '#FFD166'),
        transparent: true,
        opacity: isCurrent ? 1.0 : 0.75,
      });
      const marker = new THREE.Mesh(markerGeo, markerMat);
      marker.position.copy(pos);
      this.expeditionTrailGroup.add(marker);

      // Pulsing halo for the current active stop
      if (isCurrent) {
        const haloGeo = new THREE.RingGeometry(2.2, 3.2, 32);
        const haloMat = new THREE.MeshBasicMaterial({
          color: new THREE.Color('#FFD166'),
          transparent: true,
          opacity: 0.8,
          side: THREE.DoubleSide,
        });
        const halo = new THREE.Mesh(haloGeo, haloMat);
        halo.position.copy(pos);
        halo.lookAt(new THREE.Vector3(0, 0, 0));
        this.expeditionTrailGroup.add(halo);
      }
    }
  }

  public clearExpeditionTrail(): void {
    while (this.expeditionTrailGroup.children.length > 0) {
      const obj = this.expeditionTrailGroup.children[0] as any;
      if (obj.geometry) obj.geometry.dispose();
      if (obj.material) {
        if (Array.isArray(obj.material)) obj.material.forEach((m: any) => m.dispose());
        else obj.material.dispose();
      }
      this.expeditionTrailGroup.remove(obj);
    }
  }

  public geoToVector3(lat: number, lng: number, radius: number = GLOBE_RADIUS): THREE.Vector3 {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lng + 180) * (Math.PI / 180);

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const y = radius * Math.cos(phi);
    const z = radius * Math.sin(phi) * Math.sin(theta);

    return new THREE.Vector3(x, y, z);
  }

  public geoToCartesianArray(lat: number, lng: number, radius: number = GLOBE_RADIUS): [number, number, number] {
    const phi = (90 - lat) * (Math.PI / 180);
    const theta = (lng + 180) * (Math.PI / 180);

    const x = -(radius * Math.sin(phi) * Math.cos(theta));
    const y = radius * Math.cos(phi);
    const z = radius * Math.sin(phi) * Math.sin(theta);

    return [x, y, z];
  }

  public vector3ToGeo(v: THREE.Vector3): { lat: number; lng: number } {
    const phi = Math.acos(Math.max(-1, Math.min(1, v.y / GLOBE_RADIUS)));
    const lat = 90 - (phi * 180) / Math.PI;
    let theta = Math.atan2(v.z, -v.x);
    let lng = (theta * 180) / Math.PI - 180;
    if (lng < -180) lng += 360;
    if (lng > 180) lng -= 360;
    return { lat, lng };
  }

  public findCountryByCoordinate(lat: number, lng: number): CountryMeta | null {
    let closestCountry: CountryMeta | null = null;
    let minDistance = Infinity;

    for (const c of this.countriesList) {
      const [minLng, minLat, maxLng, maxLat] = c.bbox;
      if (lng >= minLng && lng <= maxLng && lat >= minLat && lat <= maxLat) {
        return c;
      }
      // Calculate spherical distance to centroid
      const d = Math.hypot(lat - c.lat, lng - c.lng);
      if (d < minDistance) {
        minDistance = d;
        closestCountry = c;
      }
    }

    return minDistance < 15 ? closestCountry : null;
  }

  private initTooltips(): void {
    this.tooltipEl = document.getElementById('hover-tooltip');
    this.tooltipName = document.getElementById('tooltip-name');
    this.tooltipCulture = document.getElementById('tooltip-culture');
    this.tooltipEpoch = document.getElementById('tooltip-epoch');
    this.tooltipCountry = document.getElementById('tooltip-country');
    this.tooltipArchetype = document.getElementById('tooltip-archetype');

    // Dismiss country/area/myth tooltip immediately when pointer hovers over information dialog or modal overlays
    const inspectorPanel = document.getElementById('inspector-panel');
    if (inspectorPanel) {
      const hide = () => this.hideTooltip();
      inspectorPanel.addEventListener('pointerenter', hide);
      inspectorPanel.addEventListener('pointerover', hide);
      inspectorPanel.addEventListener('pointermove', hide);
      inspectorPanel.addEventListener('mouseenter', hide);
      inspectorPanel.addEventListener('mousemove', hide);
    }

    const compareModal = document.getElementById('compare-modal');
    if (compareModal) {
      const hide = () => this.hideTooltip();
      compareModal.addEventListener('pointerenter', hide);
      compareModal.addEventListener('pointermove', hide);
      compareModal.addEventListener('mouseenter', hide);
    }

    const devPanel = document.getElementById('developer-panel');
    if (devPanel) {
      const hide = () => this.hideTooltip();
      devPanel.addEventListener('pointerenter', hide);
      devPanel.addEventListener('pointerover', hide);
      devPanel.addEventListener('pointermove', hide);
      devPanel.addEventListener('mouseenter', hide);
      devPanel.addEventListener('mousemove', hide);
    }
  }

  public findMythUnderPointer(
    clientX: number,
    clientY: number,
    maxPixelRadius: number = 32
  ): { myth: ActiveMyth; index: number } | null {
    if (this.currentActiveList.length === 0) return null;

    // Guard: Never hit-test myths if cursor is over floating UI overlays
    const timelineEl = document.getElementById('timeline-container');
    if (timelineEl) {
      const tr = timelineEl.getBoundingClientRect();
      if (
        clientX >= tr.left &&
        clientX <= tr.right &&
        clientY >= tr.top &&
        clientY <= tr.bottom
      ) {
        return null;
      }
    }

    const devPanel = document.getElementById('developer-panel');
    if (devPanel) {
      const dr = devPanel.getBoundingClientRect();
      if (
        clientX >= dr.left &&
        clientX <= dr.right &&
        clientY >= dr.top &&
        clientY <= dr.bottom
      ) {
        return null;
      }
    }

    const rect = this.renderer.domElement.getBoundingClientRect();
    let closestDist = maxPixelRadius;
    let found: { myth: ActiveMyth; index: number } | null = null;

    // 0. Check blooming constellation satellites first with highest hit-test precision
    if (this.constellationSatellites.length > 0) {
      for (const sat of this.constellationSatellites) {
        const toCam = new THREE.Vector3().subVectors(this.camera.position, sat.basePos);
        if (sat.basePos.dot(toCam) <= 0) continue;
        const proj = sat.basePos.clone().project(this.camera);
        if (proj.z >= 1.0) continue;
        const screenX = ((proj.x + 1) / 2) * rect.width + rect.left;
        const screenY = ((-proj.y + 1) / 2) * rect.height + rect.top;
        if (Math.hypot(clientX - screenX, clientY - screenY) < maxPixelRadius + 6) {
          return { myth: sat.myth, index: sat.index };
        }
      }
    }

    // 1. Screen-space proximity calculation (generous hit testing)
    for (let i = 0; i < this.currentActiveList.length; i++) {
      const m = this.currentActiveList[i];
      const pos = this.geoToVector3(m.lat, m.lng, NODE_ELEVATION);

      // Check if node is facing camera (not occluded by sphere horizon)
      const toCam = new THREE.Vector3().subVectors(this.camera.position, pos);
      if (pos.dot(toCam) <= 0) {
        continue;
      }

      const proj = pos.clone().project(this.camera);
      if (proj.z >= 1.0) continue;

      const screenX = ((proj.x + 1) / 2) * rect.width + rect.left;
      const screenY = ((-proj.y + 1) / 2) * rect.height + rect.top;

      const dist = Math.hypot(clientX - screenX, clientY - screenY);
      if (dist < closestDist) {
        closestDist = dist;
        found = { myth: m, index: i };
      }
    }

    if (found) return found;

    // 2. 3D Raycasting fallback
    this.mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -(((clientY - rect.top) / rect.height) * 2 - 1);
    this.raycaster.setFromCamera(this.mouse, this.camera);
    if (this.instancedNodes) {
      const intersects = this.raycaster.intersectObject(this.instancedNodes);
      if (intersects.length > 0 && intersects[0].instanceId !== undefined) {
        const idx = intersects[0].instanceId;
        if (idx < this.currentActiveList.length) {
          return { myth: this.currentActiveList[idx], index: idx };
        }
      }
    }

    return null;
  }

  public attachBeacon(lat: number, lng: number): void {
    const pos = this.geoToVector3(lat, lng, NODE_ELEVATION + 0.4);
    this.attachBeaconAtPosition(pos);
  }

  public attachBeaconAtPosition(pos: THREE.Vector3): void {
    if (!this.beaconMesh) return;
    this.beaconMesh.position.copy(pos);
    const normal = pos.clone().normalize();
    this.beaconMesh.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
    this.beaconMesh.visible = true;
  }

  public bloomConstellation(cluster: ActiveMyth[], selectedMythId: string): void {
    const locus = cluster[0];
    const key = `${locus.lat.toFixed(2)},${locus.lng.toFixed(2)}`;

    // If already blooming this exact cluster, update selected state on satellites
    if (this.activeBloomingClusterKey === key) {
      for (const sat of this.constellationSatellites) {
        const isSelected = sat.myth.id === selectedMythId;
        const hex = CULTURE_COLORS[sat.myth.culture] || CULTURE_COLORS.Default;
        const mat = sat.mesh.material as THREE.MeshStandardMaterial;
        mat.color.set(hex);
        mat.emissive.set(isSelected ? 0xfde047 : hex);
        mat.emissiveIntensity = isSelected ? 1.0 : 0.6;
        sat.mesh.scale.set(isSelected ? 1.35 : 1.0, isSelected ? 1.35 : 1.0, isSelected ? 1.35 : 1.0);

        if (isSelected) {
          this.attachBeaconAtPosition(sat.basePos);
        }
      }
      return;
    }

    // Build new constellation bloom
    this.retractConstellation();
    this.activeBloomingClusterKey = key;

    const centerPos = this.geoToVector3(locus.lat, locus.lng, NODE_ELEVATION);
    const normal = centerPos.clone().normalize();

    // Establish tangent coordinate frame
    const up = Math.abs(normal.y) < 0.9 ? new THREE.Vector3(0, 1, 0) : new THREE.Vector3(1, 0, 0);
    const t1 = new THREE.Vector3().crossVectors(up, normal).normalize();
    const t2 = new THREE.Vector3().crossVectors(normal, t1).normalize();

    // Central anchor locus ring
    const anchorGeo = new THREE.RingGeometry(2.4, 3.8, 32);
    const anchorMat = new THREE.MeshBasicMaterial({
      color: 0xfde047,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.85,
      blending: THREE.AdditiveBlending,
    });
    this.locusAnchorRing = new THREE.Mesh(anchorGeo, anchorMat);
    this.locusAnchorRing.position.copy(centerPos);
    this.locusAnchorRing.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), normal);
    this.constellationGroup.add(this.locusAnchorRing);

    const N = cluster.length;
    const spreadRadius = N <= 2 ? 6.2 : N === 3 ? 7.4 : 8.5;

    for (let k = 0; k < N; k++) {
      const myth = cluster[k];
      const isSelected = myth.id === selectedMythId;
      const angle = (2 * Math.PI * k) / N - Math.PI / 2;

      // Project tangent offset onto sphere
      const satPos = centerPos.clone()
        .addScaledVector(t1, Math.cos(angle) * spreadRadius)
        .addScaledVector(t2, Math.sin(angle) * spreadRadius);
      satPos.normalize().multiplyScalar(GLOBE_RADIUS + NODE_ELEVATION + 1.4);

      // Golden connecting stem cord (arched quadratic curve)
      const mid = new THREE.Vector3().addVectors(centerPos, satPos).multiplyScalar(0.5);
      mid.normalize().multiplyScalar(GLOBE_RADIUS + NODE_ELEVATION + 2.4);
      const curve = new THREE.QuadraticBezierCurve3(centerPos, mid, satPos);
      const stemGeo = new THREE.BufferGeometry().setFromPoints(curve.getPoints(24));
      const stemMat = new THREE.LineBasicMaterial({
        color: 0xfde047,
        transparent: true,
        opacity: 0.85,
        blending: THREE.AdditiveBlending,
      });
      const stemLine = new THREE.Line(stemGeo, stemMat);
      this.constellationGroup.add(stemLine);

      // Satellite sphere
      const satGeo = new THREE.SphereGeometry(2.2, 18, 18);
      const hex = CULTURE_COLORS[myth.culture] || CULTURE_COLORS.Default;
      const satMat = new THREE.MeshStandardMaterial({
        color: new THREE.Color(hex),
        emissive: isSelected ? new THREE.Color(0xfde047) : new THREE.Color(hex),
        emissiveIntensity: isSelected ? 1.0 : 0.6,
        roughness: 0.25,
        metalness: 0.8,
      });
      const satMesh = new THREE.Mesh(satGeo, satMat);
      satMesh.position.copy(satPos);
      satMesh.scale.set(isSelected ? 1.35 : 1.0, isSelected ? 1.35 : 1.0, isSelected ? 1.35 : 1.0);
      (satMesh as any).myth = myth;
      (satMesh as any).clusterIndex = k;
      this.constellationGroup.add(satMesh);

      this.constellationSatellites.push({
        mesh: satMesh,
        stem: stemLine,
        myth,
        index: k,
        basePos: satPos.clone(),
      });

      if (isSelected) {
        this.attachBeaconAtPosition(satPos);
      }
    }
  }

  public retractConstellation(): void {
    this.activeBloomingClusterKey = null;
    while (this.constellationGroup.children.length > 0) {
      const obj = this.constellationGroup.children.pop();
      if (obj) {
        if ('geometry' in obj && (obj as any).geometry) {
          (obj as any).geometry.dispose();
        }
        if ('material' in obj && (obj as any).material) {
          (obj as any).material.dispose();
        }
      }
    }
    this.locusAnchorRing = null;
    this.constellationSatellites = [];
  }

  private initEventListeners(): void {
    window.addEventListener('resize', this.onWindowResize.bind(this));

    // Pointer move for real-time hover (ignored on touch devices to avoid stuck popups)
    this.renderer.domElement.addEventListener('pointermove', (event: PointerEvent) => {
      if (event.pointerType === 'touch') return;
      this.checkRaycastHover(event.clientX, event.clientY);
    });

    // Dismiss tooltip when pointer leaves 3D canvas
    this.renderer.domElement.addEventListener('pointerleave', () => {
      this.hideTooltip();
      this.hoveredIndex = -1;
      this.controls.autoRotate = true;
      document.body.style.cursor = 'default';
    });

    this.renderer.domElement.addEventListener('pointerout', () => {
      this.hideTooltip();
    });

    // Deliberate click detection (differentiates orbital dragging from hotspot clicks)
    let pointerDownPos = { x: 0, y: 0 };
    this.renderer.domElement.addEventListener('pointerdown', (e: PointerEvent) => {
      pointerDownPos = { x: e.clientX, y: e.clientY };
    });

    this.renderer.domElement.addEventListener('pointerup', (e: PointerEvent) => {
      // Guard: Ignore clicks that occurred over floating UI elements (timeline, top-bar, etc.)
      const elAtPoint = document.elementFromPoint(e.clientX, e.clientY);
      if (
        elAtPoint &&
        elAtPoint !== this.renderer.domElement &&
        (elAtPoint.closest('#timeline-container') ||
         elAtPoint.closest('#top-bar') ||
         elAtPoint.closest('#inspector-panel') ||
         elAtPoint.closest('#developer-panel') ||
         elAtPoint.closest('#compare-modal'))
      ) {
        return;
      }

      const moveDist = Math.hypot(e.clientX - pointerDownPos.x, e.clientY - pointerDownPos.y);
      if (moveDist < 8) {
        // Intentional click!
        const hit = this.findMythUnderPointer(e.clientX, e.clientY, 36);
        if (hit) {
          this.hideTooltip();
          store.selectMyth(hit.myth.id);
          this.flyToCoordinate(hit.myth.lat, hit.myth.lng);
        } else {
          // Deselect on empty canvas clicks
          store.selectMyth(null);
        }
      }
    });

    // Sync beacon and constellation bloom with store selection
    store.subscribe((state) => {
      if (state.selectedMythId) {
        this.hideTooltip();
        this.controls.autoRotate = false; // Pause rotation while inspecting locus
        const selected = this.currentActiveList.find((m) => m.id === state.selectedMythId) ||
                         state.allMyths.find((m) => m.id === state.selectedMythId);
        if (selected) {
          const cluster = store.getActiveClusterForMyth(selected.id);
          const key = `${selected.lat.toFixed(2)},${selected.lng.toFixed(2)}`;
          if (this.activeBloomingClusterKey !== key) {
            this.flyToCoordinate(selected.lat, selected.lng);
          }
          if (cluster.length > 1) {
            this.bloomConstellation(cluster, selected.id);
          } else {
            this.retractConstellation();
            this.attachBeacon(selected.lat, selected.lng);
          }
        }
      } else {
        this.retractConstellation();
        this.controls.autoRotate = true; // Resume smooth rotation
        if (this.beaconMesh) {
          this.beaconMesh.visible = false;
        }
      }
    });
  }

  private checkRaycastHover(clientX: number, clientY: number): void {
    // Guard 1: If mouse is inside or approaching the open information dialog, hide tooltip immediately
    const inspectorPanel = document.getElementById('inspector-panel');
    if (inspectorPanel && !inspectorPanel.classList.contains('inspector-collapsed')) {
      const r = inspectorPanel.getBoundingClientRect();
      if (
        clientX >= r.left - 12 &&
        clientX <= r.right + 12 &&
        clientY >= r.top - 12 &&
        clientY <= r.bottom + 12
      ) {
        this.hideTooltip();
        this.hoveredIndex = -1;
        document.body.style.cursor = 'default';
        return;
      }
    }

    // Guard 2: If mouse is inside or approaching the developer card, hide tooltip immediately
    const devPanel = document.getElementById('developer-panel');
    if (devPanel) {
      const dr = devPanel.getBoundingClientRect();
      if (
        clientX >= dr.left - 8 &&
        clientX <= dr.right + 8 &&
        clientY >= dr.top - 8 &&
        clientY <= dr.bottom + 8
      ) {
        this.hideTooltip();
        this.hoveredIndex = -1;
        document.body.style.cursor = 'default';
        return;
      }
    }

    // Guard 3: If compare modal is active, hide tooltip
    const compareModal = document.getElementById('compare-modal');
    if (compareModal && !compareModal.classList.contains('modal-hidden')) {
      this.hideTooltip();
      this.hoveredIndex = -1;
      document.body.style.cursor = 'default';
      return;
    }

    // 1. Check if hovering near a myth hotspot
    const mythHit = this.findMythUnderPointer(clientX, clientY, 26);
    if (mythHit) {
      this.hoveredIndex = mythHit.index;
      this.showMythTooltip(mythHit.myth, clientX, clientY);
      document.body.style.cursor = 'pointer';
      this.controls.autoRotate = false; // Pause rotation while hovering on a hotspot
      return;
    }

    this.hoveredIndex = -1;
    this.controls.autoRotate = true; // Resume rotation when leaving hotspot

    // 2. Check if hovering on Earth surface / modern country
    const rect = this.container.getBoundingClientRect();
    this.mouse.x = ((clientX - rect.left) / rect.width) * 2 - 1;
    this.mouse.y = -(((clientY - rect.top) / rect.height) * 2 - 1);
    this.raycaster.setFromCamera(this.mouse, this.camera);

    if (this.globeMesh) {
      const globeIntersects = this.raycaster.intersectObject(this.globeMesh);
      if (globeIntersects.length > 0) {
        const hitPoint = globeIntersects[0].point;
        const { lat, lng } = this.vector3ToGeo(hitPoint);
        const country = this.findCountryByCoordinate(lat, lng);
        if (country) {
          this.showCountryTooltip(country, lat, lng, clientX, clientY);
          document.body.style.cursor = 'crosshair';
          return;
        }
      }
    }

    this.hideTooltip();
    document.body.style.cursor = 'default';
  }

  private showMythTooltip(myth: ActiveMyth, x: number, y: number): void {
    if (!this.tooltipEl) return;
    if (this.tooltipName) this.tooltipName.textContent = myth.name;

    const key = `${myth.lat.toFixed(2)},${myth.lng.toFixed(2)}`;
    const cluster = this.clusterMap.get(key) || [];
    if (cluster.length > 1) {
      if (this.tooltipCulture) {
        this.tooltipCulture.innerHTML = `🏛️ Sacred Epicenter • <span style="color:#fde047;font-weight:700;">${cluster.length} Concurrent Epics</span>`;
      }
    } else {
      if (this.tooltipCulture) this.tooltipCulture.textContent = `${myth.culture} Tradition`;
    }
    if (this.tooltipEpoch) {
      const startStr = myth.epoch_start < 0 ? `${Math.abs(myth.epoch_start)} BCE` : `${myth.epoch_start} CE`;
      const endStr = myth.epoch_end < 0 ? `${Math.abs(myth.epoch_end)} BCE` : `${myth.epoch_end} CE`;
      this.tooltipEpoch.textContent = `${startStr} – ${endStr}`;
    }

    // Modern Country identification
    if (this.tooltipCountry) {
      const country = this.findCountryByCoordinate(myth.lat, myth.lng);
      if (country) {
        this.tooltipCountry.textContent = `📍 Modern: ${country.name} (${country.continent})`;
        this.tooltipCountry.style.display = 'flex';
      } else {
        this.tooltipCountry.style.display = 'none';
      }
    }

    if (this.tooltipArchetype) this.tooltipArchetype.textContent = myth.archetype;

    this.tooltipEl.style.left = `${x}px`;
    this.tooltipEl.style.top = `${y}px`;
    this.tooltipEl.classList.remove('tooltip-hidden');
  }

  private showCountryTooltip(country: CountryMeta, lat: number, lng: number, x: number, y: number): void {
    if (!this.tooltipEl) return;
    if (this.tooltipName) this.tooltipName.textContent = country.name;
    if (this.tooltipCulture) this.tooltipCulture.textContent = 'Modern Nation State';
    if (this.tooltipEpoch) {
      this.tooltipEpoch.textContent = `${Math.abs(lat).toFixed(1)}° ${lat >= 0 ? 'N' : 'S'}, ${Math.abs(lng).toFixed(1)}° ${lng >= 0 ? 'E' : 'W'}`;
    }
    if (this.tooltipCountry) {
      this.tooltipCountry.textContent = `Continent: ${country.continent}`;
      this.tooltipCountry.style.display = 'flex';
    }
    if (this.tooltipArchetype) {
      this.tooltipArchetype.textContent = 'Click to explore historical epics rooted in this geography';
    }

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
        child.material.opacity = 0.5 + 0.3 * Math.sin(this.arcTime);
      }
    });

    // Pulse selection beacon ring
    if (this.beaconMesh && this.beaconMesh.visible) {
      const pulse = 1.0 + 0.18 * Math.sin(this.arcTime * 4);
      this.beaconMesh.scale.set(pulse, pulse, pulse);
    }

    // Animate blooming constellation satellites with breathing celestial pulse
    if (this.constellationSatellites.length > 0) {
      const breath = 1.0 + 0.08 * Math.sin(this.arcTime * 3);
      for (const s of this.constellationSatellites) {
        const isSelected = s.myth.id === store.getState().selectedMythId;
        const base = isSelected ? 1.35 : 1.0;
        s.mesh.scale.set(base * breath, base * breath, base * breath);
      }
      if (this.locusAnchorRing) {
        const ringPulse = 1.0 + 0.12 * Math.sin(this.arcTime * 4);
        this.locusAnchorRing.scale.set(ringPulse, ringPulse, ringPulse);
      }
    }

    this.renderer.render(this.scene, this.camera);
  };

  public destroy(): void {
    cancelAnimationFrame(this.animationFrameId);
    window.removeEventListener('resize', this.onWindowResize);
    this.renderer.dispose();
  }
}
