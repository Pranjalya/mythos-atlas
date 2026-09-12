/**
 * Global UI State Store for MythosAtlas.
 * Implements a lightweight reactive subscription pattern for zero-latency state synchronization.
 */

export interface ActiveMyth {
  id: string;
  name: string;
  lat: number;
  lng: number;
  epoch_start: number;
  epoch_end: number;
  culture: string;
  archetype: string;
  intensity: number;
  thumbnail: string;
  syncretic_ids: string[];
  description: string;
  cartesian: [number, number, number];
}

export interface AppState {
  currentYear: number;
  isPlaying: boolean;
  playSpeed: number;
  activeMyths: ActiveMyth[];
  allMyths: ActiveMyth[];
  selectedMythId: string | null;
  selectedMythDetail: any | null;
  filterCulture: string;
  showSyncretismArcs: boolean;
  showCountryBorders: boolean;
  compareModalOpen: boolean;
  compareTargetA: string | null;
  compareTargetB: string | null;
}

type Listener = (state: AppState) => void;

class Store {
  private state: AppState = {
    currentYear: -1200,
    isPlaying: false,
    playSpeed: 10,
    activeMyths: [],
    allMyths: [],
    selectedMythId: null,
    selectedMythDetail: null,
    filterCulture: 'all',
    showSyncretismArcs: true,
    showCountryBorders: true,
    compareModalOpen: false,
    compareTargetA: 'Q248352', // Epic of Gilgamesh
    compareTargetB: 'Q190828', // Popol Vuh
  };

  private listeners: Set<Listener> = new Set();

  public getState(): AppState {
    return this.state;
  }

  public subscribe(listener: Listener): () => void {
    this.listeners.add(listener);
    listener(this.state);
    return () => this.listeners.delete(listener);
  }

  private notify(): void {
    for (const listener of this.listeners) {
      listener(this.state);
    }
  }

  public setYear(year: number): void {
    if (this.state.currentYear !== year) {
      this.state.currentYear = year;
      this.notify();
    }
  }

  public togglePlay(): void {
    this.state.isPlaying = !this.state.isPlaying;
    this.notify();
  }

  public setPlaying(playing: boolean): void {
    this.state.isPlaying = playing;
    this.notify();
  }

  public setActiveMyths(myths: ActiveMyth[]): void {
    this.state.activeMyths = myths;
    this.notify();
  }

  public setAllMyths(myths: ActiveMyth[]): void {
    this.state.allMyths = myths;
    this.notify();
  }

  public selectMyth(mythId: string | null): void {
    this.state.selectedMythId = mythId;
    this.notify();
  }

  public setSelectedDetail(detail: any | null): void {
    this.state.selectedMythDetail = detail;
    this.notify();
  }

  public setFilterCulture(culture: string): void {
    this.state.filterCulture = culture;
    this.notify();
  }

  public toggleSyncretismArcs(): void {
    this.state.showSyncretismArcs = !this.state.showSyncretismArcs;
    this.notify();
  }

  public toggleCountryBorders(): void {
    this.state.showCountryBorders = !this.state.showCountryBorders;
    this.notify();
  }

  public setCompareModalOpen(open: boolean): void {
    this.state.compareModalOpen = open;
    this.notify();
  }

  public setCompareTargets(targetA: string | null, targetB: string | null): void {
    if (targetA !== undefined) this.state.compareTargetA = targetA;
    if (targetB !== undefined) this.state.compareTargetB = targetB;
    this.notify();
  }
}

export const store = new Store();
