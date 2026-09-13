/**
 * ExpeditionManager — Orchestrates Cinematic Curated Expeditions ("Story Mode").
 * Manages the Expedition Gallery, cinematic camera flights, timeline synchronization,
 * glowing celestial journey trails, and floating narrative story cards.
 */

import { store, ActiveMyth } from '../state/store.ts';
import { CURATED_EXPEDITIONS, Expedition, ExpeditionStop } from '../data/expeditions.ts';
import { MythosGlobe, CULTURE_COLORS } from './Globe.ts';
import { Timeline } from './Timeline.ts';

export class ExpeditionManager {
  private globe: MythosGlobe;
  private timeline: Timeline;
  private onNavigateToMyth: (myth: ActiveMyth, customYear?: number) => void;

  // DOM Elements
  private galleryModalEl: HTMLElement;
  private galleryListEl: HTMLElement;
  private galleryCloseBtn: HTMLElement;
  private cinematicHudEl: HTMLElement;

  // Auto-play state
  private autoPlayTimer: number | null = null;
  private autoPlaySecondsLeft: number = 12;
  private autoPlayInterval: number | null = null;
  private isTransitioning: boolean = false;

  constructor(
    globe: MythosGlobe,
    timeline: Timeline,
    onNavigateToMyth: (myth: ActiveMyth, customYear?: number) => void
  ) {
    this.globe = globe;
    this.timeline = timeline;
    this.onNavigateToMyth = onNavigateToMyth;

    this.galleryModalEl = document.getElementById('expedition-gallery-modal') as HTMLElement;
    this.galleryListEl = document.getElementById('expedition-gallery-list') as HTMLElement;
    this.galleryCloseBtn = document.getElementById('expedition-gallery-close-btn') as HTMLElement;
    this.cinematicHudEl = document.getElementById('cinematic-hud') as HTMLElement;

    this.initGallery();
    this.initEventBindings();
    this.subscribeToStore();
  }

  private initGallery(): void {
    if (!this.galleryListEl) return;

    this.galleryListEl.innerHTML = CURATED_EXPEDITIONS.map((exp) => `
      <div class="expedition-card" data-expedition-id="${exp.id}">
        <div class="exp-card-header">
          <div class="exp-hero-badge">
            <span class="exp-hero-icon">${exp.heroIcon}</span>
            <span class="exp-badge-text">${exp.badge}</span>
          </div>
          <span class="exp-duration-pill">${exp.durationLabel}</span>
        </div>
        <h3 class="exp-card-title">${exp.title}</h3>
        <h4 class="exp-card-subtitle">${exp.subtitle}</h4>
        <p class="exp-card-synopsis">${exp.synopsis}</p>
        <div class="exp-tradition-tags">
          ${exp.traditionTags.map((tag) => `<span class="exp-tag">${tag}</span>`).join('')}
        </div>
        <button class="exp-start-cta" data-expedition-id="${exp.id}">
          <span>Embark on Odyssey</span>
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="9 18 15 12 9 6"></polyline>
          </svg>
        </button>
      </div>
    `).join('');

    // Attach click listeners to cards
    this.galleryListEl.querySelectorAll('.expedition-card, .exp-start-cta').forEach((el) => {
      el.addEventListener('click', (e) => {
        const target = e.currentTarget as HTMLElement;
        const expId = target.dataset.expeditionId;
        if (expId) {
          const exp = CURATED_EXPEDITIONS.find((item) => item.id === expId);
          if (exp) {
            this.startExpedition(exp);
          }
        }
      });
    });
  }

  private initEventBindings(): void {
    // Open Gallery Trigger in Header
    const triggerBtn = document.getElementById('btn-start-expedition');
    if (triggerBtn) {
      triggerBtn.addEventListener('click', () => {
        this.openGallery();
      });
    }

    // Close Gallery
    if (this.galleryCloseBtn) {
      this.galleryCloseBtn.addEventListener('click', () => {
        this.closeGallery();
      });
    }

    // Close on backdrop click
    if (this.galleryModalEl) {
      this.galleryModalEl.addEventListener('click', (e) => {
        if (e.target === this.galleryModalEl) {
          this.closeGallery();
        }
      });
    }

    // Global Keyboard navigation
    window.addEventListener('keydown', (e) => {
      const state = store.getState();

      if (e.key === 'Escape') {
        if (state.expeditionGalleryOpen) {
          this.closeGallery();
        } else if (state.activeExpedition) {
          this.exitExpedition();
        }
      }

      if (state.activeExpedition) {
        if (e.key === 'ArrowRight') {
          e.preventDefault();
          this.nextStep();
        } else if (e.key === 'ArrowLeft') {
          e.preventDefault();
          this.prevStep();
        } else if (e.code === 'Space') {
          // Toggle auto play
          const activeTag = (document.activeElement?.tagName || '').toLowerCase();
          if (activeTag !== 'input' && activeTag !== 'textarea') {
            e.preventDefault();
            this.toggleAutoPlay();
          }
        }
      }
    });
  }

  private subscribeToStore(): void {
    let prevExpeditionId: string | null = null;
    let prevStepIndex: number = -1;

    store.subscribe((state) => {
      // Toggle gallery modal visibility
      if (this.galleryModalEl) {
        if (state.expeditionGalleryOpen) {
          this.galleryModalEl.classList.remove('modal-hidden');
        } else {
          this.galleryModalEl.classList.add('modal-hidden');
        }
      }

      // Handle active expedition change
      const currentExp = state.activeExpedition;
      if (currentExp) {
        document.body.classList.add('expedition-mode-active');
        if (this.cinematicHudEl) this.cinematicHudEl.classList.remove('hud-hidden');

        if (currentExp.id !== prevExpeditionId || state.currentExpeditionStepIndex !== prevStepIndex) {
          prevExpeditionId = currentExp.id;
          prevStepIndex = state.currentExpeditionStepIndex;
          this.renderHud(currentExp, state.currentExpeditionStepIndex);
        }
      } else if (prevExpeditionId !== null) {
        document.body.classList.remove('expedition-mode-active');
        if (this.cinematicHudEl) this.cinematicHudEl.classList.add('hud-hidden');
        const inspector = document.getElementById('inspector-panel');
        inspector?.classList.remove('expedition-inspect-open');
        prevExpeditionId = null;
        prevStepIndex = -1;
        this.stopAutoPlay();
      }
    });
  }

  public openGallery(): void {
    const filterControls = document.getElementById('filter-controls');
    filterControls?.classList.remove('mobile-open');
    store.setExpeditionGalleryOpen(true);
  }

  public closeGallery(): void {
    store.setExpeditionGalleryOpen(false);
  }

  public startExpedition(expedition: Expedition): void {
    store.startExpedition(expedition);
    this.goToStep(0);
  }

  public exitExpedition(): void {
    this.stopAutoPlay();
    this.globe.clearExpeditionTrail();
    store.exitExpedition();
  }

  public nextStep(): void {
    const state = store.getState();
    if (!state.activeExpedition) return;
    const nextIdx = state.currentExpeditionStepIndex + 1;
    if (nextIdx < state.activeExpedition.stops.length) {
      this.goToStep(nextIdx);
    } else {
      // Reached finale
      this.goToStep(state.activeExpedition.stops.length);
    }
  }

  public prevStep(): void {
    const state = store.getState();
    if (!state.activeExpedition) return;
    const prevIdx = Math.max(0, state.currentExpeditionStepIndex - 1);
    this.goToStep(prevIdx);
  }

  public goToStep(index: number): void {
    const state = store.getState();
    const exp = state.activeExpedition;
    if (!exp) return;

    if (index >= exp.stops.length) {
      // Render finale state
      store.setExpeditionStep(exp.stops.length);
      this.renderFinale(exp);
      return;
    }

    const stop = exp.stops[index];
    store.setExpeditionStep(index);

    // Sync timeline epoch with WASM 1D interval tree
    this.timeline.updateYear(stop.year);

    // Find active myth in store
    const myth = store.getState().allMyths.find((m) => m.id === stop.mythId);
    if (myth) {
      store.selectMyth(myth.id);
    }

    // Trigger cinematic camera glide
    this.isTransitioning = true;
    this.globe.cinematicFlyToCoordinate(stop.lat, stop.lng, 1800, () => {
      this.isTransitioning = false;
    });

    // Render golden celestial journey trail
    this.globe.renderExpeditionTrail(exp.stops, index);

    // Reset auto-play timer countdown
    this.resetAutoPlayTimer();
  }

  public toggleAutoPlay(): void {
    const state = store.getState();
    if (state.isExpeditionAutoPlaying) {
      this.stopAutoPlay();
    } else {
      this.startAutoPlay();
    }
  }

  private startAutoPlay(): void {
    store.setExpeditionAutoPlay(true);
    this.resetAutoPlayTimer();
    this.updateAutoPlayUi(true);
  }

  private stopAutoPlay(): void {
    store.setExpeditionAutoPlay(false);
    if (this.autoPlayTimer) clearTimeout(this.autoPlayTimer);
    if (this.autoPlayInterval) clearInterval(this.autoPlayInterval);
    this.autoPlayTimer = null;
    this.autoPlayInterval = null;
    this.updateAutoPlayUi(false);
  }

  private resetAutoPlayTimer(): void {
    if (!store.getState().isExpeditionAutoPlaying) return;

    if (this.autoPlayTimer) clearTimeout(this.autoPlayTimer);
    if (this.autoPlayInterval) clearInterval(this.autoPlayInterval);

    this.autoPlaySecondsLeft = 12;

    this.autoPlayInterval = window.setInterval(() => {
      this.autoPlaySecondsLeft--;
      const label = document.getElementById('exp-countdown-label');
      if (label) label.textContent = `${this.autoPlaySecondsLeft}s`;

      if (this.autoPlaySecondsLeft <= 0) {
        clearInterval(this.autoPlayInterval!);
      }
    }, 1000);

    this.autoPlayTimer = window.setTimeout(() => {
      const state = store.getState();
      if (state.activeExpedition) {
        if (state.currentExpeditionStepIndex < state.activeExpedition.stops.length - 1) {
          this.nextStep();
        } else {
          this.goToStep(state.activeExpedition.stops.length);
        }
      }
    }, 12000);
  }

  private updateAutoPlayUi(isPlaying: boolean): void {
    const playBtn = document.getElementById('exp-autoplay-btn');
    if (playBtn) {
      playBtn.classList.toggle('playing', isPlaying);
      playBtn.innerHTML = isPlaying
        ? `<span class="exp-btn-icon">⏸</span><span>Auto <span id="exp-countdown-label">${this.autoPlaySecondsLeft}s</span></span>`
        : `<span class="exp-btn-icon">▶</span><span>Auto-Play</span>`;
    }
  }

  private renderHud(exp: Expedition, stepIndex: number): void {
    if (!this.cinematicHudEl) return;

    if (stepIndex >= exp.stops.length) {
      this.renderFinale(exp);
      return;
    }

    const stop = exp.stops[stepIndex];
    const totalStops = exp.stops.length;
    const isFirst = stepIndex === 0;
    const isLast = stepIndex === totalStops - 1;
    const cultureColor = CULTURE_COLORS[stop.culture] || '#E6B86A';

    const formattedYear =
      stop.year < 0 ? `${Math.abs(stop.year)} BCE` : `${stop.year} CE`;

    this.cinematicHudEl.innerHTML = `
      <!-- Top Chapter Progress Bar -->
      <div class="cinematic-top-bar">
        <div class="exp-top-left">
          <span class="exp-active-icon">${exp.heroIcon}</span>
          <div class="exp-title-meta">
            <span class="exp-parent-title">${exp.title}</span>
            <span class="exp-step-indicator">Chapter ${stop.chapterNumber} of ${totalStops}</span>
          </div>
        </div>

        <div class="exp-progress-track" role="tablist" aria-label="Expedition Chapters">
          ${exp.stops.map((s, idx) => `
            <button
              class="exp-dot-btn ${idx === stepIndex ? 'active' : ''} ${idx < stepIndex ? 'visited' : ''}"
              data-step-index="${idx}"
              title="Chapter ${s.chapterNumber}: ${s.chapterTitle}"
              aria-label="Go to Chapter ${s.chapterNumber}: ${s.chapterTitle}"
            >
              <span class="dot-inner"></span>
            </button>
          `).join('')}
        </div>

        <div class="exp-top-actions">
          <button id="exp-autoplay-btn" class="exp-action-pill ${store.getState().isExpeditionAutoPlaying ? 'playing' : ''}" title="Toggle Auto-Play (Spacebar)">
            ${store.getState().isExpeditionAutoPlaying
              ? `<span class="exp-btn-icon">⏸</span><span>Auto <span id="exp-countdown-label">${this.autoPlaySecondsLeft}s</span></span>`
              : `<span class="exp-btn-icon">▶</span><span>Auto-Play</span>`}
          </button>
          <button id="exp-prev-btn" class="exp-nav-btn" ${isFirst ? 'disabled' : ''} title="Previous Chapter (Left Arrow)" aria-label="Previous Chapter">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
          </button>
          <button id="exp-next-btn" class="exp-nav-btn exp-nav-primary" title="Next Chapter (Right Arrow)" aria-label="Next Chapter">
            <span>${isLast ? 'Finish' : 'Next'}</span>
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
          <button id="exp-exit-btn" class="exp-exit-btn" title="Exit Expedition (ESC)" aria-label="Exit Expedition">&times;</button>
        </div>
      </div>

      <!-- Floating Narrative Story Card -->
      <div class="cinematic-story-card">
        <div class="story-card-header">
          <div class="story-meta-tags">
            <span class="story-chapter-badge">Chapter ${stop.chapterNumber}</span>
            <span class="story-culture-badge" style="color: ${cultureColor}; border-color: ${cultureColor}44; background: ${cultureColor}15;">
              <span class="culture-dot" style="background: ${cultureColor};"></span>
              ${stop.culture}
            </span>
            <span class="story-epoch-pill">${formattedYear}</span>
          </div>
        </div>

        <h2 class="story-chapter-title">${stop.chapterTitle}</h2>
        <h3 class="story-myth-name">${stop.mythName}</h3>

        <p class="story-narrative-prose">${stop.narrativeLead}</p>

        <div class="story-insight-box">
          <div class="insight-label">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            <span>Comparative Archetype Thread</span>
          </div>
          <p class="insight-text">${stop.comparativeInsight}</p>
        </div>

        <div class="story-motifs-row">
          ${stop.keyMotifs.map((m) => `<span class="story-motif-tag">#${m}</span>`).join('')}
        </div>

        <div class="story-card-footer">
          <button id="story-inspect-btn" class="story-btn-secondary" title="Open Full Archaeological Record">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path>
              <path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>
            </svg>
            <span>Inspect Narrative</span>
          </button>
          ${
            stepIndex > 0
              ? `<button id="story-compare-btn" class="story-btn-primary" title="Launch Comparative Copilot against previous stop">
                   <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                     <rect x="3" y="3" width="7" height="18" rx="1" />
                     <rect x="14" y="3" width="7" height="18" rx="1" />
                   </svg>
                   <span>Compare with Ch. ${stepIndex}</span>
                 </button>`
              : ''
          }
        </div>
      </div>
    `;

    // Wire HUD controls
    const exitBtn = document.getElementById('exp-exit-btn');
    if (exitBtn) exitBtn.addEventListener('click', () => this.exitExpedition());

    const prevBtn = document.getElementById('exp-prev-btn');
    if (prevBtn) prevBtn.addEventListener('click', () => this.prevStep());

    const nextBtn = document.getElementById('exp-next-btn');
    if (nextBtn) nextBtn.addEventListener('click', () => this.nextStep());

    const autoPlayBtn = document.getElementById('exp-autoplay-btn');
    if (autoPlayBtn) autoPlayBtn.addEventListener('click', () => this.toggleAutoPlay());

    // Step dots
    this.cinematicHudEl.querySelectorAll('.exp-dot-btn').forEach((dot) => {
      dot.addEventListener('click', (e) => {
        const target = e.currentTarget as HTMLElement;
        const idx = parseInt(target.dataset.stepIndex || '0', 10);
        this.goToStep(idx);
      });
    });

    // Story Card Actions
    const inspectBtn = document.getElementById('story-inspect-btn');
    if (inspectBtn) {
      inspectBtn.addEventListener('click', () => {
        const inspector = document.getElementById('inspector-panel');
        if (inspector) {
          inspector.classList.toggle('expedition-inspect-open');
        }
        store.selectMyth(stop.mythId);
      });
    }

    const compareBtn = document.getElementById('story-compare-btn');
    if (compareBtn && stepIndex > 0) {
      compareBtn.addEventListener('click', () => {
        const prevStop = exp.stops[stepIndex - 1];
        store.setCompareTargets(prevStop.mythId, stop.mythId);
        store.setCompareModalOpen(true);
      });
    }
  }

  private renderFinale(exp: Expedition): void {
    if (!this.cinematicHudEl) return;

    this.stopAutoPlay();

    this.cinematicHudEl.innerHTML = `
      <div class="cinematic-top-bar">
        <div class="exp-top-left">
          <span class="exp-active-icon">${exp.heroIcon}</span>
          <div class="exp-title-meta">
            <span class="exp-parent-title">${exp.title}</span>
            <span class="exp-step-indicator">Odyssey Complete</span>
          </div>
        </div>
        <div class="exp-top-actions">
          <button id="exp-exit-btn-finale" class="exp-exit-btn" title="Exit Expedition" aria-label="Exit Expedition">&times;</button>
        </div>
      </div>

      <div class="cinematic-story-card finale-card">
        <div class="finale-badge">✨ Odyssey Concluded</div>
        <h2 class="finale-title">${exp.title}</h2>
        <p class="finale-prose">
          You have traced this narrative thread across <strong>${exp.stops.length} foundational chapters</strong> and multiple millennia, revealing how distinct civilizations arrived at symmetrical sacred answers to existence.
        </p>

        <div class="finale-actions">
          <button id="finale-synthesize-btn" class="finale-cta-primary">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
            <span>Synthesize Odyssey with AI</span>
          </button>
          <button id="finale-restart-btn" class="finale-cta-secondary">
            <span>Replay Odyssey</span>
          </button>
          <button id="finale-explore-btn" class="finale-cta-secondary">
            <span>More Expeditions</span>
          </button>
        </div>
      </div>
    `;

    document.getElementById('exp-exit-btn-finale')?.addEventListener('click', () => this.exitExpedition());
    document.getElementById('finale-restart-btn')?.addEventListener('click', () => this.goToStep(0));
    document.getElementById('finale-explore-btn')?.addEventListener('click', () => {
      this.exitExpedition();
      this.openGallery();
    });

    const synthBtn = document.getElementById('finale-synthesize-btn');
    if (synthBtn) {
      synthBtn.addEventListener('click', () => {
        // Compare first stop and culmination stop in Gemini modal
        const first = exp.stops[0].mythId;
        const last = exp.stops[exp.stops.length - 1].mythId;
        store.setCompareTargets(first, last);
        store.setCompareModalOpen(true);
      });
    }
  }
}
