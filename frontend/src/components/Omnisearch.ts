/**
 * Omnisearch & Semantic Knowledge Navigator ("Ask the Atlas").
 * Provides dual-engine discovery: instant 0ms client-side keyword & archetype matching
 * plus AI Semantic Vector Search over Qdrant Cloud embeddings.
 */

import { store, ActiveMyth } from '../state/store.ts';
import { CULTURE_COLORS } from './Globe.ts';
import { API_BASE } from '../config.ts';

export interface SemanticSearchResult {
  id: string;
  name: string;
  culture: string;
  archetype: string;
  score: number;
  thumbnail?: string;
  description?: string;
  extract?: string;
}

export class Omnisearch {
  private modalEl: HTMLElement;
  private inputEl: HTMLInputElement;
  private resultsEl: HTMLElement;
  private spinnerEl: HTMLElement;
  private closeBtn: HTMLElement;
  private backdropEl: HTMLElement;
  private triggerBtn: HTMLElement | null;
  private tabButtons: NodeListOf<HTMLButtonElement>;

  private currentMode: 'all' | 'semantic' | 'keyword' = 'all';
  private debounceTimer: number | null = null;
  private activeIndex: number = -1;
  private currentResults: (ActiveMyth & { matchType?: 'instant' | 'semantic'; score?: number })[] = [];
  private onNavigateToMyth: (myth: ActiveMyth) => void;

  constructor(onNavigateToMyth: (myth: ActiveMyth) => void) {
    this.onNavigateToMyth = onNavigateToMyth;

    this.modalEl = document.getElementById('omnisearch-modal')!;
    this.inputEl = document.getElementById('omnisearch-input') as HTMLInputElement;
    this.resultsEl = document.getElementById('omnisearch-results')!;
    this.spinnerEl = document.getElementById('omnisearch-spinner')!;
    this.closeBtn = document.getElementById('omnisearch-close-btn')!;
    this.backdropEl = this.modalEl.querySelector('.omnisearch-backdrop')!;
    this.triggerBtn = document.getElementById('btn-open-search');
    this.tabButtons = this.modalEl.querySelectorAll('.omnisearch-tab');

    this.initEvents();
  }

  private initEvents(): void {
    // Global Cmd+K / Ctrl+K and / shortcut listener
    window.addEventListener('keydown', (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        this.toggle();
        return;
      }

      // Close on Escape if open
      if (e.key === 'Escape' && this.isOpen()) {
        e.preventDefault();
        this.close();
        return;
      }

      // Arrow navigation inside results list when open
      if (this.isOpen()) {
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          this.moveActive(1);
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          this.moveActive(-1);
        } else if (e.key === 'Enter') {
          e.preventDefault();
          if (this.activeIndex >= 0 && this.activeIndex < this.currentResults.length) {
            this.selectResult(this.currentResults[this.activeIndex]);
          }
        }
      }
    });

    // Trigger button click
    this.triggerBtn?.addEventListener('click', () => {
      this.open();
    });

    // Close buttons & backdrop
    this.closeBtn.addEventListener('click', () => this.close());
    this.backdropEl.addEventListener('click', () => this.close());

    // Filter tab switching
    this.tabButtons.forEach((tab) => {
      tab.addEventListener('click', () => {
        this.tabButtons.forEach((t) => t.classList.remove('active'));
        tab.classList.add('active');
        this.currentMode = tab.dataset.mode as any;
        this.performSearch(this.inputEl.value.trim());
      });
    });

    // Real-time input handling
    this.inputEl.addEventListener('input', () => {
      const query = this.inputEl.value.trim();
      this.handleInput(query);
    });
  }

  public open(): void {
    this.modalEl.classList.remove('omnisearch-hidden');
    document.getElementById('hover-tooltip')?.classList.add('tooltip-hidden');
    this.inputEl.value = '';
    this.inputEl.focus();
    this.showEmptyState();
  }

  public close(): void {
    this.modalEl.classList.add('omnisearch-hidden');
    this.inputEl.blur();
    this.activeIndex = -1;
  }

  public toggle(): void {
    if (this.isOpen()) {
      this.close();
    } else {
      this.open();
    }
  }

  public isOpen(): boolean {
    return !this.modalEl.classList.contains('omnisearch-hidden');
  }

  private handleInput(query: string): void {
    if (!query) {
      this.showEmptyState();
      return;
    }

    // 1. If keyword mode: execute pure client-side 0ms search
    if (this.currentMode === 'keyword') {
      const instantResults = this.searchLocalKeywords(query);
      this.renderResults(instantResults);
      return;
    }

    // 2. For 'all' and 'semantic': instant client results first, then debounce AI semantic search
    const instantResults = this.searchLocalKeywords(query);
    this.renderResults(instantResults);

    if (this.debounceTimer) {
      window.clearTimeout(this.debounceTimer);
    }

    this.debounceTimer = window.setTimeout(async () => {
      await this.performSemanticSearch(query, instantResults);
    }, 240);
  }

  private performSearch(query: string): void {
    this.handleInput(query);
  }

  private searchLocalKeywords(query: string): (ActiveMyth & { matchType: 'instant'; score: number })[] {
    const q = query.toLowerCase();
    const all = store.getState().allMyths;

    const matches: { myth: ActiveMyth; score: number }[] = [];

    for (const m of all) {
      const nameMatch = m.name.toLowerCase().includes(q);
      const cultureMatch = m.culture.toLowerCase().includes(q);
      const archetypeMatch = m.archetype.toLowerCase().includes(q);
      const descMatch = m.description ? m.description.toLowerCase().includes(q) : false;

      if (nameMatch || cultureMatch || archetypeMatch || descMatch) {
        let score = 0.7;
        if (m.name.toLowerCase().startsWith(q)) score = 1.0;
        else if (nameMatch) score = 0.9;
        else if (archetypeMatch) score = 0.85;
        else if (cultureMatch) score = 0.8;

        matches.push({ myth: m, score });
      }
    }

    matches.sort((a, b) => b.score - a.score);

    return matches.slice(0, 10).map((m) => ({
      ...m.myth,
      matchType: 'instant' as const,
      score: m.score,
    }));
  }

  private async performSemanticSearch(
    query: string,
    existingInstant: (ActiveMyth & { matchType: 'instant'; score: number })[]
  ): Promise<void> {
    this.spinnerEl.classList.remove('spinner-hidden');

    try {
      const res = await fetch(`${API_BASE}/api/v1/myths/search/semantic?q=${encodeURIComponent(query)}&limit=8`);
      if (!res.ok) throw new Error(`Semantic search returned HTTP ${res.status}`);

      const semanticData: SemanticSearchResult[] = await res.json();
      const allMyths = store.getState().allMyths;

      const semanticResults: (ActiveMyth & { matchType: 'semantic'; score: number })[] = [];

      for (const s of semanticData) {
        const full = allMyths.find((m) => m.id === s.id);
        if (full) {
          semanticResults.push({
            ...full,
            matchType: 'semantic' as const,
            score: s.score,
          });
        }
      }

      if (this.currentMode === 'semantic') {
        this.renderResults(semanticResults);
      } else {
        // Merge without duplicates: Semantic results take priority for natural language queries
        const seen = new Set<string>();
        const merged: (ActiveMyth & { matchType: 'instant' | 'semantic'; score: number })[] = [];

        // Put top semantic results first
        for (const sr of semanticResults) {
          if (!seen.has(sr.id)) {
            seen.add(sr.id);
            merged.push(sr);
          }
        }

        // Append remaining instant keyword matches
        for (const ir of existingInstant) {
          if (!seen.has(ir.id)) {
            seen.add(ir.id);
            merged.push(ir);
          }
        }

        this.renderResults(merged);
      }
    } catch (err) {
      console.warn('Semantic AI search fallback to keyword:', err);
      if (this.currentMode === 'semantic') {
        this.renderResults(existingInstant);
      }
    } finally {
      this.spinnerEl.classList.add('spinner-hidden');
    }
  }

  private renderResults(results: (ActiveMyth & { matchType?: 'instant' | 'semantic'; score?: number })[]): void {
    this.currentResults = results;
    this.resultsEl.innerHTML = '';
    this.activeIndex = -1;

    if (results.length === 0) {
      this.resultsEl.innerHTML = `
        <div class="omnisearch-empty-state">
          <div class="omnisearch-empty-icon">🔍</div>
          <h4>No mythic narratives found</h4>
          <p>Try searching for broader motifs like <em>"sun"</em>, <em>"flood"</em>, <em>"trickster"</em>, or asking <em>"Where did dragon myths come from?"</em></p>
        </div>
      `;
      return;
    }

    results.forEach((m, idx) => {
      const item = document.createElement('div');
      item.className = 'omnisearch-result-item';
      item.setAttribute('role', 'option');
      item.setAttribute('data-index', String(idx));

      const cultureColor = CULTURE_COLORS[m.culture] || '#e6b86a';
      const startStr = m.epoch_start < 0 ? `${Math.abs(m.epoch_start)} BCE` : `${m.epoch_start} CE`;
      const endStr = m.epoch_end < 0 ? `${Math.abs(m.epoch_end)} BCE` : `${m.epoch_end} CE`;

      const isSemantic = m.matchType === 'semantic';
      const pct = m.score ? Math.round(m.score * 100) : 100;
      const tagHtml = isSemantic
        ? `<span class="match-tag match-semantic">🔮 ${pct}% Semantic</span>`
        : `<span class="match-tag match-instant">⚡ Instant Match</span>`;

      const thumbHtml = m.thumbnail
        ? `<img class="result-thumb" src="${m.thumbnail}" alt="${m.name}" onerror="this.style.display='none'" />`
        : `<div class="result-thumb-placeholder" style="color:${cultureColor}; border-color:${cultureColor}40">${m.name.charAt(0)}</div>`;

      item.innerHTML = `
        <div class="result-main">
          ${thumbHtml}
          <div class="result-info">
            <div class="result-title-row">
              <h4 class="result-title">${m.name}</h4>
              <span class="badge" style="background:${cultureColor}20; color:${cultureColor}; border-color:${cultureColor}40">${m.culture}</span>
            </div>
            <p class="result-archetype">${m.archetype}</p>
          </div>
        </div>
        <div class="result-badge-col">
          ${tagHtml}
          <span class="result-epoch">${startStr} – ${endStr}</span>
        </div>
      `;

      item.addEventListener('click', () => {
        this.selectResult(m);
      });

      this.resultsEl.appendChild(item);
    });

    // Auto-select first item
    this.setActiveIndex(0);
  }

  private moveActive(direction: number): void {
    if (this.currentResults.length === 0) return;
    let nextIndex = this.activeIndex + direction;
    if (nextIndex < 0) nextIndex = this.currentResults.length - 1;
    if (nextIndex >= this.currentResults.length) nextIndex = 0;
    this.setActiveIndex(nextIndex);
  }

  private setActiveIndex(index: number): void {
    this.activeIndex = index;
    const items = this.resultsEl.querySelectorAll('.omnisearch-result-item');
    items.forEach((item, idx) => {
      if (idx === index) {
        item.classList.add('active');
        (item as HTMLElement).scrollIntoView({ block: 'nearest' });
      } else {
        item.classList.remove('active');
      }
    });
  }

  private selectResult(m: ActiveMyth): void {
    this.close();
    this.onNavigateToMyth(m);
  }

  private showEmptyState(): void {
    this.resultsEl.innerHTML = `
      <div class="omnisearch-empty-state">
        <div class="omnisearch-empty-icon">✨</div>
        <h4>Ask the Atlas or Search Any Epic</h4>
        <p>Type keywords like <em>"immortality"</em>, <em>"Gilgamesh"</em>, <em>"underworld"</em>, or natural language questions like <em>"Where did dragon myths come from?"</em> or <em>"Show me female sun deities"</em>.</p>
      </div>
    `;
    this.currentResults = [];
    this.activeIndex = -1;
  }
}
