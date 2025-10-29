import { Globe } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { Language, languages } from '../i18n/i18nConfig';

export default function LanguageSwitch() {
  const { language, setLanguage } = useLanguage();

  const handleLanguageChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    setLanguage(e.target.value as Language);
  };

  return (
    <div className="flex items-center space-x-2">
      <Globe className="w-4 h-4 text-gray-500" />
      <select
        value={language}
        onChange={handleLanguageChange}
        className="text-sm border border-gray-300 rounded-lg px-2 py-1 focus:ring-2 focus:ring-orange-500 focus:border-orange-500 bg-white"
      >
        {(Object.keys(languages) as Language[]).map((lang) => (
          <option key={lang} value={lang}>
            {languages[lang]}
          </option>
        ))}
      </select>
    </div>
  );
}
