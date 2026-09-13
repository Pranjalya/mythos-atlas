/**
 * Side-Panel Entity Inspector for MythosAtlas.
 * Handles on-demand hydration of myth entities, displaying enriched Wikipedia narratives,
 * syncretic edges, and Qdrant semantic motif parallels.
 */

import { store, ActiveMyth } from '../state/store.ts';

export class Inspector {
  private panelEl: HTMLElement;
  private nameEl: HTMLElement;
  private cultureEl: HTMLElement;
  private epochEl: HTMLElement;
  private thumbnailEl: HTMLImageElement;
  private archetypeEl: HTMLElement;
  private coordsEl: HTMLElement;
  private spanEl: HTMLElement;
  private extractEl: HTMLElement;
  private wikiLinkEl: HTMLAnchorElement;
  private syncreticListEl: HTMLElement;
  private parallelsListEl: HTMLElement;
  private fetchParallelsBtn: HTMLButtonElement;
  private compareBtn: HTMLButtonElement;
  private closeBtn: HTMLButtonElement;

  // Cluster Deck Elements for Multi-Myth Epicenters
  private clusterDeckEl: HTMLElement;
  private clusterPillBarEl: HTMLElement;
  private clusterCountEl: HTMLElement;
  private clusterTitleEl: HTMLElement;

  private onFlyTo: (lat: number, lng: number) => void;
  private currentMythId: string | null = null;

  constructor(onFlyTo: (lat: number, lng: number) => void) {
    this.onFlyTo = onFlyTo;

    this.panelEl = document.getElementById('inspector-panel')!;
    this.nameEl = document.getElementById('inspector-name')!;
    this.cultureEl = document.getElementById('inspector-culture')!;
    this.epochEl = document.getElementById('inspector-epoch')!;
    this.thumbnailEl = document.getElementById('inspector-thumbnail') as HTMLImageElement;
    this.archetypeEl = document.getElementById('inspector-archetype')!;
    this.coordsEl = document.getElementById('inspector-coords')!;
    this.spanEl = document.getElementById('inspector-span')!;
    this.extractEl = document.getElementById('inspector-extract')!;
    this.wikiLinkEl = document.getElementById('inspector-wiki-link') as HTMLAnchorElement;
    this.syncreticListEl = document.getElementById('inspector-syncretic-list')!;
    this.parallelsListEl = document.getElementById('inspector-parallels-list')!;
    this.fetchParallelsBtn = document.getElementById('btn-fetch-parallels') as HTMLButtonElement;
    this.compareBtn = document.getElementById('inspector-compare-btn') as HTMLButtonElement;
    this.closeBtn = document.getElementById('inspector-close-btn') as HTMLButtonElement;

    this.clusterDeckEl = document.getElementById('inspector-cluster-deck')!;
    this.clusterPillBarEl = document.getElementById('cluster-pill-bar')!;
    this.clusterCountEl = document.getElementById('cluster-deck-count')!;
    this.clusterTitleEl = document.getElementById('cluster-epicenter-title')!;

    this.initEvents();
  }

  private initEvents(): void {
    this.closeBtn.addEventListener('click', () => {
      this.close();
    });

    // Ensure any floating country/area/myth tooltip vanishes when mouse hovers over information dialog
    const hideHoverTooltip = () => {
      document.getElementById('hover-tooltip')?.classList.add('tooltip-hidden');
    };
    this.panelEl.addEventListener('mouseenter', hideHoverTooltip);
    this.panelEl.addEventListener('pointerenter', hideHoverTooltip);
    this.panelEl.addEventListener('mousemove', hideHoverTooltip);
    this.panelEl.addEventListener('pointermove', hideHoverTooltip);
    this.panelEl.addEventListener('mouseover', hideHoverTooltip);

    this.fetchParallelsBtn.addEventListener('click', () => {
      if (this.currentMythId) {
        this.fetchParallels(this.currentMythId);
      }
    });

    this.compareBtn.addEventListener('click', () => {
      if (this.currentMythId) {
        store.setCompareTargets(this.currentMythId, store.getState().compareTargetB);
        store.setCompareModalOpen(true);
      }
    });

    store.subscribe((state) => {
      if (state.selectedMythId) {
        if (state.selectedMythId !== this.currentMythId) {
          this.hydrateMyth(state.selectedMythId);
        }
      } else {
        if (!this.panelEl.classList.contains('inspector-collapsed')) {
          this.panelEl.classList.add('inspector-collapsed');
          this.currentMythId = null;
        }
      }
    });
  }

  public async hydrateMyth(mythId: string): Promise<void> {
    this.currentMythId = mythId;
    this.panelEl.classList.remove('inspector-collapsed');
    document.getElementById('hover-tooltip')?.classList.add('tooltip-hidden');

    // Check if we have pre-loaded static record for instant preview
    const staticRecord = store.getState().allMyths.find((m) => m.id === mythId);
    if (staticRecord) {
      this.renderBasicInfo(staticRecord);
    }

    // On-demand dynamic hydration from backend
    try {
      this.extractEl.textContent = 'Hydrating enriched narrative from dynamic knowledge layer...';
      const res = await fetch(`/api/v1/myths/${mythId}`);
      if (res.ok) {
        const enriched = await res.json();
        store.setSelectedDetail(enriched);
        this.renderEnrichedDetails(enriched);
      } else {
        if (staticRecord) {
          this.extractEl.textContent = staticRecord.description || 'Mythological narrative record.';
        }
      }
    } catch (e) {
      console.warn('Backend hydration offline, falling back to static record:', e);
      if (staticRecord) {
        this.extractEl.textContent = staticRecord.description || 'Mythological narrative record.';
      }
    }
  }

  private renderBasicInfo(m: ActiveMyth): void {
    this.nameEl.textContent = m.name;
    this.cultureEl.textContent = m.culture;

    const startStr = m.epoch_start < 0 ? `${Math.abs(m.epoch_start)} BCE` : `${m.epoch_start} CE`;
    const endStr = m.epoch_end < 0 ? `${Math.abs(m.epoch_end)} BCE` : `${m.epoch_end} CE`;
    this.epochEl.textContent = `${startStr} – ${endStr}`;
    this.spanEl.textContent = `${startStr} to ${endStr}`;

    this.archetypeEl.textContent = m.archetype;
    this.coordsEl.textContent = `${Math.abs(m.lat)}° ${m.lat >= 0 ? 'N' : 'S'}, ${Math.abs(m.lng)}° ${m.lng >= 0 ? 'E' : 'W'}`;

    if (m.thumbnail) {
      this.thumbnailEl.src = m.thumbnail;
    } else {
      this.thumbnailEl.src = 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=600&auto=format&fit=crop&q=80';
    }

    this.renderClusterDeck(m);

    this.parallelsListEl.innerHTML = `<div class="empty-state-hint">Click "Find Parallels" to query semantic motif vectors in Qdrant.</div>`;
  }

  private renderClusterDeck(currentMyth: ActiveMyth): void {
    const cluster = store.getActiveClusterForMyth(currentMyth.id);
    if (cluster.length <= 1) {
      this.clusterDeckEl.classList.add('cluster-deck-hidden');
      this.clusterPillBarEl.innerHTML = '';
      return;
    }

    this.clusterDeckEl.classList.remove('cluster-deck-hidden');
    this.clusterCountEl.textContent = `${cluster.length} Concurrent Epics`;
    
    // Extract concise epicenter title
    const rawTitle = currentMyth.name.split(' (')[0];
    const cleanLocusName = rawTitle.length > 28 ? rawTitle.substring(0, 26) + '…' : rawTitle;
    this.clusterTitleEl.textContent = `${cleanLocusName} Locus`;

    this.clusterPillBarEl.innerHTML = '';
    cluster.forEach((m, idx) => {
      const pill = document.createElement('button');
      const isCurrent = m.id === currentMyth.id;
      pill.className = `cluster-pill ${isCurrent ? 'active' : ''}`;
      pill.setAttribute('role', 'tab');
      pill.setAttribute('aria-selected', isCurrent ? 'true' : 'false');
      pill.title = `${m.name} (${m.culture} • ${m.archetype})`;

      const shortName = m.name.length > 24 ? m.name.substring(0, 22) + '…' : m.name;
      pill.innerHTML = `
        <span class="pill-badge">${idx + 1}</span>
        <span class="pill-label">${shortName}</span>
      `;

      pill.addEventListener('click', (e) => {
        e.stopPropagation();
        if (m.id !== this.currentMythId) {
          store.selectMyth(m.id);
        }
      });

      this.clusterPillBarEl.appendChild(pill);
    });
  }

  private renderEnrichedDetails(data: any): void {
    if (data.extract) {
      this.extractEl.textContent = data.extract;
    }
    if (data.wikipedia_url) {
      this.wikiLinkEl.href = data.wikipedia_url;
      this.wikiLinkEl.style.display = 'inline-block';
    } else {
      this.wikiLinkEl.style.display = 'none';
    }

    // Render syncretic counterparts
    this.syncreticListEl.innerHTML = '';
    const syncretic = data.syncretic_targets || [];
    if (syncretic.length === 0) {
      this.syncreticListEl.innerHTML = `<div class="empty-state-hint">No direct syncretic counterparts recorded.</div>`;
    } else {
      for (const target of syncretic) {
        const card = document.createElement('div');
        card.className = 'syncretic-card';
        card.innerHTML = `
          <div>
            <div class="card-title">${target.name}</div>
            <div class="card-culture">${target.culture} Tradition</div>
          </div>
          <span class="badge">Fly &rarr;</span>
        `;
        card.addEventListener('click', () => {
          this.onFlyTo(target.lat, target.lng);
          store.selectMyth(target.id);
        });
        this.syncreticListEl.appendChild(card);
      }
    }
  }

  private async fetchParallels(mythId: string): Promise<void> {
    this.parallelsListEl.innerHTML = `<div class="empty-state-hint">Searching 384D motif vector space in Qdrant...</div>`;

    try {
      const res = await fetch(`/api/v1/parallels/${mythId}?limit=3`);
      if (res.ok) {
        const parallels = await res.json();
        this.parallelsListEl.innerHTML = '';
        if (parallels.length === 0) {
          this.parallelsListEl.innerHTML = `<div class="empty-state-hint">No close global parallels identified.</div>`;
          return;
        }

        for (const p of parallels) {
          const card = document.createElement('div');
          card.className = 'parallel-card';
          const matchPercent = Math.round(p.score * 100);
          card.innerHTML = `
            <div>
              <div class="card-title">${p.name}</div>
              <div class="card-culture">${p.culture} • ${p.archetype}</div>
            </div>
            <span class="score-badge">${matchPercent}% Match</span>
          `;
          card.addEventListener('click', () => {
            store.setCompareTargets(this.currentMythId, p.id);
            store.setCompareModalOpen(true);
          });
          this.parallelsListEl.appendChild(card);
        }
      }
    } catch (e) {
      this.parallelsListEl.innerHTML = `<div class="empty-state-hint">Failed to retrieve vector parallels from backend.</div>`;
    }
  }

  public close(): void {
    this.panelEl.classList.add('inspector-collapsed');
    this.clusterDeckEl.classList.add('cluster-deck-hidden');
    this.clusterPillBarEl.innerHTML = '';
    this.currentMythId = null;
    if (store.getState().selectedMythId !== null) {
      store.selectMyth(null);
    }
  }
}
