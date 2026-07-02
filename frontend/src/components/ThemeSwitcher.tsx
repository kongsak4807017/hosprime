import React, { useState, useEffect } from 'react';

export const ThemeSwitcher: React.FC = () => {
  const [theme, setTheme] = useState<'dark' | 'light'>('dark');

  useEffect(() => {
    const saved = localStorage.getItem('theme') || 'dark';
    setTheme(saved as 'dark' | 'light');
    if (saved === 'light') {
      document.documentElement.classList.add('light-theme');
    } else {
      document.documentElement.classList.remove('light-theme');
    }
  }, []);

  const toggleTheme = () => {
    const next = theme === 'dark' ? 'light' : 'dark';
    setTheme(next);
    localStorage.setItem('theme', next);
    if (next === 'light') {
      document.documentElement.classList.add('light-theme');
    } else {
      document.documentElement.classList.remove('light-theme');
    }
  };

  return (
    <button
      onClick={toggleTheme}
      className="glass px-3.5 py-1.5 rounded-xl text-xs font-semibold text-slate-300 hover:text-white border border-slate-800 hover:border-gold-500/50 transition-all duration-200 flex items-center gap-2"
    >
      <span>{theme === 'dark' ? '🌙 Dark Mode' : '☀️ Light Mode'}</span>
    </button>
  );
};
