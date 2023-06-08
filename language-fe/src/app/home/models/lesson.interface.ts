import { Word } from './word.interface';

interface Lesson {
  id?: any;
  language: string;
  description: string;
  title: string;
  text?: string;
  words?: Word[];
  known_words?: number;
  unknown_words?: number;
  marked_words?: number;
}

export { Lesson };
