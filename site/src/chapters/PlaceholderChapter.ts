import * as THREE from 'three';
import { createLayer, type Context } from '@/app/Context';
import type { SectionSpec } from '@/story/sections';
import { Beats } from '@/ui/Beats';
import type { View } from '@/webgl/View';
import type { Chapter, ChapterOutput, Frame } from './Chapter';

class FlatView implements View {
  readonly scene = new THREE.Scene();
  readonly camera = new THREE.PerspectiveCamera();

  constructor(tone: number) {
    this.scene.background = new THREE.Color(tone, tone, tone);
  }

  resize(): void {}
}

export class PlaceholderChapter implements Chapter {
  readonly id;
  readonly view: View;
  private readonly layer: HTMLElement;
  private readonly beats: Beats;

  constructor(context: Context, spec: SectionSpec, tone: number) {
    this.id = spec.id;
    this.view = new FlatView(tone);
    this.layer = createLayer(context, spec.id);
    this.beats = new Beats(this.layer, [{ text: spec.title, start: 0.05, end: 0.95, variant: 'title' }]);
    this.layer.style.color = tone > 0.5 ? '#000' : '#fff';
  }

  async prepare(): Promise<void> {}

  enter(): void {
    this.layer.classList.add('is-active');
  }

  leave(): void {
    this.layer.classList.remove('is-active');
  }

  update(progress: number, _frame: Frame, output: ChapterOutput): void {
    this.beats.update(progress);
    output.meter = { label: 'Progress', value: `${Math.round(progress * 100)} %` };
  }
}
