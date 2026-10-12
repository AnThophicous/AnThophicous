import type { Context } from '@/app/Context';
import { SECTIONS, type SectionId } from '@/story/sections';
import { BookCard } from '@/ui/BookCard';
import { HorizonLine } from '@/webgl/surface/HorizonLine';
import type { Chapter } from './Chapter';
import { OceanChapter } from './ocean/OceanChapter';
import { PlaceholderChapter } from './PlaceholderChapter';
import { RoomChapter } from './room/RoomChapter';
import { WelcomeChapter } from './welcome/WelcomeChapter';

export function createChapters(context: Context): Map<SectionId, Chapter> {
  const line = new HorizonLine();
  const card = new BookCard();
  const chapters = new Map<SectionId, Chapter>();
  chapters.set('welcome', new WelcomeChapter(context, line));
  chapters.set('ocean', new OceanChapter(context, line, card));
  chapters.set('room', new RoomChapter(context));
  SECTIONS.forEach((spec, index) => {
    if (!chapters.has(spec.id))
      chapters.set(spec.id, new PlaceholderChapter(context, spec, index % 2 ? 0.05 : 0.9));
  });
  return chapters;
}
