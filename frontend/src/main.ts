/**
 * MythosAtlas Main Application Entry Point.
 * Initializes the Rust WASM Interval Tree, hydrates static cartographic payload,
 * mounts Three.js 3D WebGL presentation layer, and binds reactive UI controls.
 */

// @ts-ignore
import initWasm, { load_records, query_timeline } from './wasm/engine_wasm.js';
import { store, ActiveMyth } from './state/store.ts';
import { MythosGlobe } from './components/Globe.ts';
import { Timeline } from './components/Timeline.ts';
import { Inspector } from './components/Inspector.ts';
import { CompareModal } from './components/CompareModal.ts';

async function bootstrap() {
  console.log('🏛️ Initializing MythosAtlas Spatio-Temporal Core...');

  try {
    // 1. Initialize WebAssembly module
    await initWasm();
    console.log('⚡ WebAssembly core compiled & loaded successfully.');

    // 2. Fetch pre-baked lean static dataset (<5MB)
    const staticRes = await fetch('/data/static_myths.json');
    if (!staticRes.ok) {
      throw new Error(`Failed to load static myths bundle: ${staticRes.statusText}`);
    }
    const staticText = await staticRes.text();
    const staticJson: ActiveMyth[] = JSON.parse(staticText);

    // 3. Load records into Rust in-memory 1D Interval Tree
    const loadSuccess = load_records(staticText);
    if (!loadSuccess) {
      console.warn('WASM load_records reported warning during deserialization.');
    }
    console.log(`🌲 In-memory 1D Interval Tree indexed ${staticJson.length} global myth records.`);

    store.setAllMyths(staticJson);

    // 4. Initialize 3D Globe presentation layer
    const globe = new MythosGlobe('canvas-container');

    // 5. Initialize Side-panel Inspector
    const inspector = new Inspector((lat, lng) => {
      globe.flyToCoordinate(lat, lng);
    });

    // 6. Initialize Comparative Copilot Modal
    const compareModal = new CompareModal();

    // 7. Initialize Timeline Scrubber with 0ms WASM query function
    const timeline = new Timeline((year: number) => {
      try {
        const results = query_timeline(year);
        return Array.isArray(results) ? results : [];
      } catch (err) {
        console.error('WASM query_timeline error:', err);
        return [];
      }
    });

    // 8. Bind reactive updates to Globe
    store.subscribe((state) => {
      globe.updateActiveMyths(state.activeMyths);
    });

    // 9. Wire top bar filter controls
    const cultureSelect = document.getElementById('culture-filter') as HTMLSelectElement;
    if (cultureSelect) {
      cultureSelect.addEventListener('change', (e) => {
        const culture = (e.target as HTMLSelectElement).value;
        store.setFilterCulture(culture);
        timeline.updateYear(store.getState().currentYear);
      });
    }

    const syncretismToggle = document.getElementById('btn-toggle-syncretism') as HTMLButtonElement;
    if (syncretismToggle) {
      syncretismToggle.addEventListener('click', () => {
        store.toggleSyncretismArcs();
        syncretismToggle.classList.toggle('active', store.getState().showSyncretismArcs);
        globe.updateActiveMyths(store.getState().activeMyths);
      });
    }

    const openCompareBtn = document.getElementById('btn-open-compare') as HTMLButtonElement;
    if (openCompareBtn) {
      openCompareBtn.addEventListener('click', () => {
        store.setCompareModalOpen(true);
      });
    }

    const resetViewBtn = document.getElementById('btn-reset-view') as HTMLButtonElement;
    if (resetViewBtn) {
      resetViewBtn.addEventListener('click', () => {
        globe.resetView();
      });
    }

    // Trigger initial year update (-1200 BCE)
    timeline.updateYear(-1200);

    console.log('✨ MythosAtlas 3D Knowledge Engine Ready at 60+ FPS.');
  } catch (error) {
    console.error('Fatal initialization error:', error);
    const container = document.getElementById('canvas-container');
    if (container) {
      container.innerHTML = `
        <div style="padding: 40px; color: #ff6b6b; font-family: monospace; z-index: 100; position: relative;">
          <h2>Failed to initialize MythosAtlas Core</h2>
          <pre>${String(error)}</pre>
        </div>
      `;
    }
  }
}

// Start application
bootstrap();
