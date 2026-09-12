/**
 * Dual-Tradition Comparative Synthesis Modal for MythosAtlas.
 * Renders structural comparisons powered by the LLM service / structuralist comparative engine.
 */

import { store, ActiveMyth } from '../state/store.ts';

export class CompareModal {
  private modalEl: HTMLElement;
  private closeBtn: HTMLElement;
  private selectA: HTMLSelectElement;
  private selectB: HTMLSelectElement;
  private runBtn: HTMLButtonElement;
  private contentEl: HTMLElement;

  constructor() {
    this.modalEl = document.getElementById('compare-modal')!;
    this.closeBtn = document.getElementById('compare-modal-close')!;
    this.selectA = document.getElementById('compare-select-a') as HTMLSelectElement;
    this.selectB = document.getElementById('compare-select-b') as HTMLSelectElement;
    this.runBtn = document.getElementById('btn-run-comparison') as HTMLButtonElement;
    this.contentEl = document.getElementById('compare-modal-content')!;

    this.initEvents();
  }

  private initEvents(): void {
    this.closeBtn.addEventListener('click', () => {
      store.setCompareModalOpen(false);
    });

    const backdrop = this.modalEl.querySelector('.modal-backdrop');
    if (backdrop) {
      backdrop.addEventListener('click', () => {
        store.setCompareModalOpen(false);
      });
    }

    this.runBtn.addEventListener('click', () => {
      this.executeComparison();
    });

    store.subscribe((state) => {
      if (state.compareModalOpen) {
        this.modalEl.classList.remove('modal-hidden');
        this.populateDropdowns(state.allMyths, state.compareTargetA, state.compareTargetB);
      } else {
        this.modalEl.classList.add('modal-hidden');
      }
    });
  }

  public populateDropdowns(
    myths: ActiveMyth[],
    targetA: string | null,
    targetB: string | null
  ): void {
    if (this.selectA.children.length === 0 && myths.length > 0) {
      // Sort myths alphabetically by culture then name
      const sorted = [...myths].sort((a, b) => {
        if (a.culture !== b.culture) return a.culture.localeCompare(b.culture);
        return a.name.localeCompare(b.name);
      });

      this.selectA.innerHTML = '';
      this.selectB.innerHTML = '';

      for (const m of sorted) {
        const optA = document.createElement('option');
        optA.value = m.id;
        optA.textContent = `[${m.culture}] ${m.name}`;
        this.selectA.appendChild(optA);

        const optB = document.createElement('option');
        optB.value = m.id;
        optB.textContent = `[${m.culture}] ${m.name}`;
        this.selectB.appendChild(optB);
      }
    }

    if (targetA) this.selectA.value = targetA;
    if (targetB) this.selectB.value = targetB;

    // Auto-run if targets were just opened
    if (targetA && targetB && targetA !== targetB) {
      this.executeComparison();
    }
  }

  public async executeComparison(): Promise<void> {
    const mythAId = this.selectA.value;
    const mythBId = this.selectB.value;

    if (!mythAId || !mythBId) return;

    this.contentEl.innerHTML = `
      <div class="compare-placeholder">
        <div style="font-size: 1.8rem; margin-bottom: 12px; animation: pulse-spin 2s infinite linear; display: inline-block;">✦</div>
        <p>Synthesizing structuralist comparative analysis via comparative intelligence engine...</p>
      </div>
    `;

    try {
      const res = await fetch('/api/v1/compare', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          myth_a_id: mythAId,
          myth_b_id: mythBId,
        }),
      });

      if (!res.ok) {
        throw new Error(`Comparison API returned status ${res.status}`);
      }

      const data = await res.json();
      this.renderSynthesis(data);
    } catch (e) {
      this.contentEl.innerHTML = `
        <div class="compare-placeholder" style="color: #ff6b6b;">
          Failed to generate comparative synthesis. Verify backend server is active.
        </div>
      `;
    }
  }

  private renderSynthesis(data: any): void {
    const syn = data.synthesis;
    if (!syn) {
      this.contentEl.innerHTML = `<div class="compare-placeholder">Invalid synthesis format received.</div>`;
      return;
    }

    const arch = syn.character_archetypes || {};
    const motifs = syn.inciting_motifs || {};
    const resol = syn.cosmological_resolution || {};
    const typo = syn.structural_typology || {};
    const takeaways = syn.key_takeaways || [];

    const convergencePercent = Math.round((typo.convergence_score || 0.8) * 100);

    this.contentEl.innerHTML = `
      <div class="synthesis-grid">
        <!-- Structural Typology Banner -->
        <div class="typology-banner">
          <div class="typology-header">
            <span class="typology-type">${typo.classification || 'Structural Parallelism'}</span>
            <span class="typology-score">${convergencePercent}% Structural Alignment</span>
          </div>
          <p class="typology-rationale">${typo.rationale || ''}</p>
        </div>

        <!-- Matrix Sections -->
        <div class="matrix-columns">
          <!-- Column 1: Archetypes & Motifs -->
          <div class="matrix-card">
            <h3 class="matrix-card-title">Character Archetypes</h3>
            <div class="matrix-field">
              <span class="field-label">Protagonist Agency</span>
              <p class="field-value">${arch.protagonist_comparison || 'Heroic ordeal tested by mortality and divine decree.'}</p>
            </div>
            <div class="matrix-field">
              <span class="field-label">Adversary Dynamics</span>
              <p class="field-value">${arch.adversary_dynamics || 'Confrontation between cosmic order and primordial chaos.'}</p>
            </div>
            <div class="matrix-field">
              <span class="field-label">Supernatural Intervention</span>
              <p class="field-value">${arch.supernatural_allies || 'Divine guides and sacred talismans bridging mortal limits.'}</p>
            </div>
          </div>

          <!-- Column 2: Inciting Motifs & Resolutions -->
          <div class="matrix-card">
            <h3 class="matrix-card-title">Narrative Mechanics</h3>
            <div class="matrix-field">
              <span class="field-label">Inciting Catalyst</span>
              <p class="field-value">${motifs.catalyst_event || 'Cosmic disruption breaking equilibrium between gods and mortals.'}</p>
            </div>
            <div class="matrix-field">
              <span class="field-label">Taboo / Transgression</span>
              <p class="field-value">${motifs.taboo_or_transgression || 'Boundary violation and the consequences of mortal hubris.'}</p>
            </div>
            <div class="matrix-field">
              <span class="field-label">Cosmological Reordering</span>
              <p class="field-value">${resol.transformation_of_order || 'Permanent restructuring of social order and sacred geography.'}</p>
            </div>
          </div>
        </div>

        <!-- Enduring Key Takeaways -->
        <div class="takeaways-card">
          <h3 class="matrix-card-title">Comparative Folkloric Takeaways</h3>
          <ul class="takeaways-list">
            ${takeaways.map((t: string) => `<li>${t}</li>`).join('')}
          </ul>
        </div>
      </div>
    `;
  }
}
