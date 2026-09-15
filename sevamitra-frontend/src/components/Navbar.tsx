"use client";

import { Moon, Sun, Globe } from "lucide-react";
import { Language } from "@/types/chat";

interface NavbarProps {
  language: Language;
  setLanguage: (language: Language) => void;
  darkMode: boolean;
  setDarkMode: (value: boolean) => void;
}

export default function Navbar({
  language,
  setLanguage,
  darkMode,
  setDarkMode,
}: NavbarProps) {
  return (
    <header className="sticky top-0 z-50 border-b border-slate-200 bg-white/95 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-700 text-xl">
            🇮🇳
          </div>

          <div>
            <h1 className="text-lg font-bold text-slate-900 dark:text-white">
              SevaMitra AI
            </h1>
            <p className="hidden text-xs text-slate-500 sm:block">
              Government Service Guide
            </p>
          </div>
        </div>

        {/* Right side */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border px-3 py-2 dark:border-slate-700">
            <Globe size={16} />

            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value as Language)}
              className="bg-transparent text-sm outline-none dark:bg-slate-950"
            >
              <option>English</option>
              <option>Hindi</option>
              <option>Telugu</option>
            </select>
          </div>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="rounded-lg border p-2 hover:bg-slate-100 dark:border-slate-700 dark:hover:bg-slate-800"
          >
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
