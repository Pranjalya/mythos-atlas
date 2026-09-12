/**
 * Spatio-Temporal Timeline Controller for MythosAtlas.
 * Controls temporal scrubbing (-4000 BCE to 1500 CE) with instant client-side WASM filtering.
 */

import { store } from '../state/store.ts';

export interface EpochMetadata {
  start: number;
  end: number;
  name: string;
  subtext: string;
}

export const EPOCHS: EpochMetadata[] = [
  {
    start: -4000,
    end: -2000,
    name: 'Early Bronze Age',
    subtext: 'First Urban Centers & Archaic Cosmogonies',
  },
  {
    start: -2000,
    end: -1200,
    name: 'Middle & Late Bronze Age',
    subtext: 'Heroic Epics, Deluge Cycles & Chaoskampf',
  },
  {
    start: -1200,
    end: -500,
    name: 'Bronze Collapse & Early Iron Age',
    subtext: 'Codification of Sacred Hymns & Oral Epics',
  },
  {
    start: -500,
    end: 0,
    name: 'Axial Age & Classical Antiquity',
    subtext: 'Homeric Tragedies, Upanishads & Philosophical Metaphysics',
  },
  {
    start: 0,
    end: 500,
    name: 'Imperial & Late Antiquity',
    subtext: 'Pan-Eurasian Trade Routes & Syncretic Amalgamation',
  },
  {
    start: 500,
    end: 1500,
    name: 'Medieval & Post-Classical Era',
    subtext: 'Norse Eddas, Journey to the West, Popol Vuh & Mali Empires',
  },
];

export class Timeline {
  private slider: HTMLInputElement;
  private yearDisplay: HTMLElement;
  private epochNameDisplay: HTMLElement;
  private playBtn: HTMLButtonElement;
  private playIcon: SVGElement | null;
  private epochPills: NodeListOf<HTMLButtonElement>;

  private queryWasmFn: (year: number) => any[];
  private animInterval: number | null = null;

  constructor(queryWasmFn: (year: number) => any[]) {
    this.queryWasmFn = queryWasmFn;

    this.slider = document.getElementById('timeline-slider') as HTMLInputElement;
    this.yearDisplay = document.getElementById('current-year-display')!;
    this.epochNameDisplay = document.getElementById('current-epoch-name')!;
    this.playBtn = document.getElementById('btn-play-timeline') as HTMLButtonElement;
    this.playIcon = document.getElementById('play-icon') as unknown as SVGElement;
    this.epochPills = document.querySelectorAll('.epoch-pill');

    this.initEvents();
    this.updateYear(parseInt(this.slider.value, 10));
  }

  private initEvents(): void {
    // Isolate timeline clicks and gestures from canvas/globe orbit handlers
    const timelineContainer = document.getElementById('timeline-container');
    if (timelineContainer) {
      ['pointerdown', 'pointerup', 'mousedown', 'mouseup', 'click'].forEach((evt) => {
        timelineContainer.addEventListener(evt, (e) => {
          e.stopPropagation();
        });
      });
    }

    // Slider scrub (input event fires smoothly at 60fps while dragging)
    this.slider.addEventListener('input', () => {
      const year = parseInt(this.slider.value, 10);
      this.updateYear(year);
    });

    // Play/Pause button
    this.playBtn.addEventListener('click', () => {
      store.togglePlay();
    });

    // Epoch quick jump pills
    this.epochPills.forEach((pill) => {
      pill.addEventListener('click', () => {
        const year = parseInt(pill.dataset.year || '0', 10);
        this.slider.value = year.toString();
        this.updateYear(year);
      });
    });

    // Subscribe to store state
    store.subscribe((state) => {
      if (state.isPlaying && !this.animInterval) {
        this.startPlayLoop();
      } else if (!state.isPlaying && this.animInterval) {
        this.stopPlayLoop();
      }
    });
  }

  public updateYear(year: number): void {
    store.setYear(year);

    // Format display string (e.g. -1200 -> "1200 BCE", 800 -> "800 CE")
    const yearStr = year < 0 ? `${Math.abs(year)} BCE` : year === 0 ? '1 CE' : `${year} CE`;
    this.yearDisplay.textContent = yearStr;

    // Determine current epoch metadata
    const currentEpoch = EPOCHS.find((e) => year >= e.start && year <= e.end) || EPOCHS[EPOCHS.length - 1];
    this.epochNameDisplay.textContent = `${currentEpoch.name} • ${currentEpoch.subtext}`;

    // Update active epoch pill
    this.epochPills.forEach((pill) => {
      const pillYear = parseInt(pill.dataset.year || '0', 10);
      pill.classList.toggle('active', Math.abs(pillYear - year) < 300);
    });

    // High-frequency client-side WASM Interval Tree Query (0ms roundtrip)
    const active = this.queryWasmFn(year);

    // Apply culture filter if selected
    const filter = store.getState().filterCulture;
    const filtered = filter === 'all' ? active : active.filter((m) => m.culture === filter);

    store.setActiveMyths(filtered);

    const activeCountEl = document.getElementById('active-count');
    if (activeCountEl) {
      activeCountEl.textContent = filtered.length.toString();
    }
  }

  private startPlayLoop(): void {
    if (this.playIcon) {
      // Show pause symbol
      this.playIcon.innerHTML = `<rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/>`;
    }

    this.animInterval = window.setInterval(() => {
      let current = parseInt(this.slider.value, 10);
      current += 15;
      if (current > 1500) {
        current = -4000;
      }
      this.slider.value = current.toString();
      this.updateYear(current);
    }, 100);
  }

  private stopPlayLoop(): void {
    if (this.animInterval) {
      clearInterval(this.animInterval);
      this.animInterval = null;
    }
    if (this.playIcon) {
      // Show play symbol
      this.playIcon.innerHTML = `<polygon points="5 3 19 12 5 21 5 3"/>`;
    }
  }
}
