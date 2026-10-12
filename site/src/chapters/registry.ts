import type { Context } from '@/app/Context';
import { SECTIONS, type SectionId } from '@/story/sections';
import type { Chapter } from './Chapter';
import { PlaceholderChapter } from './PlaceholderChapter';

export function createChapters(context: Context): Map<SectionId, Chapter> {
  const chapters = new Map<SectionId, Chapter>();
  SECTIONS.forEach((spec, index) => {
    chapters.set(spec.id, new PlaceholderChapter(context, spec, index % 2 ? 0.05 : 0.9));
  });
  return chapters;
}
