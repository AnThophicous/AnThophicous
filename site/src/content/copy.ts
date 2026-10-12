import type { BeatSpec } from '@/ui/Beats';

export const WELCOME_BEATS: BeatSpec[] = [
  { text: 'Welcome.', start: 0, end: 0.15, variant: 'display', place: 'sky', holdIn: true },
  {
    text: 'My name is\nBrenno Leon de Souza Amaral.',
    start: 0.17,
    end: 0.34,
    variant: 'title',
    place: 'sky',
  },
  {
    text: 'I design for the web\nand set it in motion.',
    start: 0.36,
    end: 0.53,
    variant: 'title',
    place: 'sky',
  },
  {
    text: 'Sixteen years old.\nSix of them talking to machines.',
    start: 0.55,
    end: 0.71,
    variant: 'title',
    place: 'sky',
  },
  { text: 'Most people live\nat the surface.', start: 0.73, end: 0.885, variant: 'title', place: 'sky' },
  { text: 'I never could.', start: 0.77, end: 0.885, variant: 'lead', place: 'sea' },
  {
    text: 'There is more beneath this page',
    start: 0.9,
    end: 1,
    variant: 'caption',
    place: 'gate',
    holdOut: true,
  },
];

export const OCEAN_BEATS: BeatSpec[] = [
  {
    text: 'Have you ever been swallowed whole\nby something you were studying?',
    start: 0.1,
    end: 0.27,
    variant: 'lead',
    place: 'sky',
  },
  { text: 'Then you know this place.', start: 0.42, end: 0.54, variant: 'title' },
  { text: 'Every page pulled me\na little deeper.', start: 0.56, end: 0.68, variant: 'title' },
  {
    text: 'Some of them still float up\nwhen I need them.',
    start: 0.7,
    end: 0.8,
    variant: 'lead',
    place: 'top',
  },
  { text: 'Drag a book. Click to open it.', start: 0.7, end: 0.84, variant: 'caption', place: 'bottom' },
  { text: 'Deeper.', start: 0.88, end: 0.97, variant: 'title' },
];

export const ROOM_BEATS: BeatSpec[] = [
  {
    text: 'Somewhere under all of it,\nthere is a room.',
    start: 0.03,
    end: 0.16,
    variant: 'lead',
    place: 'top',
  },
  { text: 'This is where I spend most nights.', start: 0.27, end: 0.44, variant: 'lead', place: 'bottom' },
  { text: 'Building things nobody asked for,', start: 0.47, end: 0.63, variant: 'lead', place: 'bottom' },
  {
    text: 'until they become\nthings people need.',
    start: 0.66,
    end: 0.86,
    variant: 'lead',
    place: 'bottom',
  },
];

export const HELLO_LINES = [
  'Hi. Welcome.',
  "You're a little late,",
  'but I know you came\nto know me better.',
  "I'm glad you did.",
] as const;

export const FALL_LINES = ['If you really want to know me,', "you'll have to fall in."] as const;

export const HORIZON_BEATS: BeatSpec[] = [
  { text: 'An event horizon.', start: 0.08, end: 0.22, variant: 'caption', place: 'top' },
  {
    text: 'Nothing that crosses it\never comes back the same.',
    start: 0.22,
    end: 0.4,
    variant: 'lead',
    place: 'bottom',
  },
  { text: 'Not light.', start: 0.44, end: 0.56, variant: 'title', place: 'bottom' },
  { text: 'Not time.', start: 0.58, end: 0.7, variant: 'title', place: 'bottom' },
  { text: 'Not even doubt.', start: 0.72, end: 0.84, variant: 'title', place: 'bottom' },
];

export const STARS_BEATS: BeatSpec[] = [
  { text: "Inside, it isn't empty.", start: 0.04, end: 0.2, variant: 'title' },
  { text: 'Every star is something I lived.', start: 0.22, end: 0.38, variant: 'title' },
  { text: 'A year. A book.\nA first line of code.', start: 0.4, end: 0.56, variant: 'lead', place: 'bottom' },
  {
    text: 'Hover the brightest ones. Remember with me.',
    start: 0.58,
    end: 0.92,
    variant: 'caption',
    place: 'bottom',
  },
];

export const GLASS_BEATS: BeatSpec[] = [
  { text: 'Look closer.', start: 0.04, end: 0.24, variant: 'title' },
  { text: "You know, don't you?", start: 0.4, end: 0.78, variant: 'display' },
];

export const IDENTITY_BEATS: BeatSpec[] = [
  { text: 'But this is who I am.', start: 0.22, end: 0.42, variant: 'lead' },
  {
    text: 'Designer — Web designer — Front-end developer — Motion',
    start: 0.7,
    end: 1,
    variant: 'caption',
    place: 'bottom',
    holdOut: true,
  },
];

export const ENDING_BEATS: BeatSpec[] = [
  {
    text: 'Most people live at the surface.\nIt is warm there.',
    start: 0.04,
    end: 0.16,
    variant: 'lead',
    place: 'sky',
  },
  {
    text: 'But everything worth finding\nis a little deeper.',
    start: 0.18,
    end: 0.3,
    variant: 'lead',
    place: 'sky',
  },
  { text: 'So follow your dreams.', start: 0.32, end: 0.44, variant: 'title', place: 'sky' },
  {
    text: 'Then go deeper.\nInto reality. Into study. Into yourself.',
    start: 0.46,
    end: 0.6,
    variant: 'lead',
    place: 'sky',
  },
  { text: 'And if it ever feels like drowning,', start: 0.62, end: 0.74, variant: 'lead', place: 'sky' },
  {
    text: "you're only learning\nto breathe underwater.",
    start: 0.74,
    end: 0.88,
    variant: 'title',
    place: 'sky',
  },
];
