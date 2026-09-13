/**
 * Random Pilgrim Mode ("Surprise Me").
 * Sweeps the camera over the 3D globe to an extraordinary mythic narrative,
 * automatically synchronizes the spatio-temporal epoch, and hydrates the inspector.
 */

import { store, ActiveMyth } from '../state/store.ts';

export class PilgrimMode {
  private onNavigateToMyth: (myth: ActiveMyth, targetYear: number) => void;
  private surpriseBtns: HTMLElement[];

  constructor(onNavigateToMyth: (myth: ActiveMyth, targetYear: number) => void) {
    this.onNavigateToMyth = onNavigateToMyth;
    this.surpriseBtns = Array.from(document.querySelectorAll('#btn-surprise-me'));

    this.initEvents();
  }

  private initEvents(): void {
    this.surpriseBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        this.triggerSurprise();
      });
    });
  }

  public triggerSurprise(): void {
    const allMyths = store.getState().allMyths;
    if (!allMyths || allMyths.length === 0) return;

    const currentId = store.getState().selectedMythId;
    const candidates = allMyths.filter((m) => m.id !== currentId);
    const pool = candidates.length > 0 ? candidates : allMyths;

    // Pick random myth
    const randomIndex = Math.floor(Math.random() * pool.length);
    const selected = pool[randomIndex];

    // Calculate historical year epoch where this myth flourished
    let targetYear = Math.round((selected.epoch_start + selected.epoch_end) / 2);
    targetYear = Math.max(-4000, Math.min(1500, targetYear));

    // Animate compass icon on surprise buttons
    this.surpriseBtns.forEach((btn) => {
      const icon = btn.querySelector('.surprise-icon');
      if (icon) {
        icon.animate(
          [
            { transform: 'rotate(0deg) scale(1)' },
            { transform: 'rotate(720deg) scale(1.3)' },
            { transform: 'rotate(1080deg) scale(1)' },
          ],
          { duration: 800, easing: 'cubic-bezier(0.16, 1, 0.3, 1)' }
        );
      }
    });

    this.onNavigateToMyth(selected, targetYear);
  }
}
