import en from './locales/en.json';
import uk from './locales/uk.json';

export type Language = 'en' | 'uk';

export const languages: Record<Language, string> = {
  en: 'English',
  uk: 'Українська',
};

export const translations = {
  en,
  uk,
};

export const defaultLanguage: Language = 'uk';

export function getTranslation(lang: Language, key: string): string {
  const keys = key.split('.');
  let value: any = translations[lang];
  
  for (const k of keys) {
    value = value?.[k];
  }
  
  return value || key;
}
