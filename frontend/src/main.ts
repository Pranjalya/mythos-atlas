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
import { Omnisearch } from './components/Omnisearch.ts';
import { PilgrimMode } from './components/PilgrimMode.ts';
import { ExpeditionManager } from './components/ExpeditionManager.ts';

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

    // Attach to window for direct interaction and inspection
    (window as any).store = store;
    (window as any).globe = globe;
    (window as any).inspector = inspector;

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

    const bordersToggle = document.getElementById('btn-toggle-borders') as HTMLButtonElement;
    if (bordersToggle) {
      bordersToggle.addEventListener('click', () => {
        store.toggleCountryBorders();
        bordersToggle.classList.toggle('active', store.getState().showCountryBorders);
        globe.toggleCountryBorders(store.getState().showCountryBorders);
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
        if (window.innerWidth <= 900) {
          const filterControls = document.getElementById('filter-controls');
          filterControls?.classList.remove('mobile-open');
        }
      });
    }

    const resetViewBtn = document.getElementById('btn-reset-view') as HTMLButtonElement;
    if (resetViewBtn) {
      resetViewBtn.addEventListener('click', () => {
        globe.resetView();
      });
    }

    // Wire mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle') as HTMLButtonElement;
    const filterControls = document.getElementById('filter-controls') as HTMLElement;
    if (mobileMenuToggle && filterControls) {
      mobileMenuToggle.addEventListener('click', (e) => {
        e.stopPropagation();
        filterControls.classList.toggle('mobile-open');
      });
    }

    // Wire developer card minimize/expand toggle
    const devToggleBtn = document.getElementById('dev-panel-toggle') as HTMLButtonElement;
    const devCollapsedBtn = document.getElementById('dev-panel-collapsed-btn') as HTMLButtonElement;
    const devPanel = document.getElementById('developer-panel') as HTMLElement;
    if (devToggleBtn && devPanel && devCollapsedBtn) {
      const toggleDevPanel = (e: Event) => {
        e.stopPropagation();
        devPanel.classList.toggle('collapsed');
      };
      devToggleBtn.addEventListener('click', toggleDevPanel);
      devCollapsedBtn.addEventListener('click', toggleDevPanel);

      // Close developer card if clicking outside when expanded
      document.addEventListener('click', (e) => {
        if (!devPanel.classList.contains('collapsed')) {
          const target = e.target as HTMLElement;
          if (!devPanel.contains(target)) {
            devPanel.classList.add('collapsed');
          }
        }
      });
    }

    // Unified navigation handler for search and surprise pilgrim discovery
    const navigateToMyth = (myth: ActiveMyth, customYear?: number) => {
      // Check if myth is active in current year
      const currentYear = store.getState().currentYear;
      const isCurrentlyActive = currentYear >= myth.epoch_start && currentYear <= myth.epoch_end;

      if (!isCurrentlyActive || customYear !== undefined) {
        let targetYear = customYear !== undefined ? customYear : Math.round((myth.epoch_start + myth.epoch_end) / 2);
        targetYear = Math.max(-4000, Math.min(1500, targetYear));
        timeline.updateYear(targetYear);
      }

      // If culture filter currently hides this myth, reset to 'all'
      if (store.getState().filterCulture !== 'all') {
        store.setFilterCulture('all');
        const cultureSelect = document.getElementById('culture-filter') as HTMLSelectElement;
        if (cultureSelect) cultureSelect.value = 'all';
      }

      // Fly camera and select myth
      globe.flyToCoordinate(myth.lat, myth.lng);
      store.selectMyth(myth.id);
    };

    // 10. Initialize Omnisearch ("Ask the Atlas")
    const omnisearch = new Omnisearch((myth) => {
      navigateToMyth(myth);
    });

    // 11. Initialize "Surprise Me" (Random Pilgrim Mode)
    const pilgrimMode = new PilgrimMode((myth, targetYear) => {
      navigateToMyth(myth, targetYear);
    });

    // 12. Initialize Cinematic Curated Expeditions ("Story Mode")
    const expeditionManager = new ExpeditionManager(globe, timeline, (myth, customYear) => {
      navigateToMyth(myth, customYear);
    });

    (window as any).omnisearch = omnisearch;
    (window as any).pilgrimMode = pilgrimMode;
    (window as any).expeditionManager = expeditionManager;

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
