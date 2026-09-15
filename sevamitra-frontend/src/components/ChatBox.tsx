"use client";

import { Send } from "lucide-react";
import { FormEvent } from "react";
import VoiceButton from "./VoiceButton";

interface ChatBoxProps {
  input: string;
  setInput: (value: string) => void;
  onSend: () => void;
  listening: boolean;
  onVoice: () => void;
  loading: boolean;
}

export default function ChatBox({
  input,
  setInput,
  onSend,
  listening,
  onVoice,
  loading,
}: ChatBoxProps) {
  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();

    if (!loading && input.trim()) {
      onSend();
    }
  };

  return (
    <div className="sticky bottom-0 border-t border-slate-200 bg-white/95 p-4 backdrop-blur dark:border-slate-800 dark:bg-slate-950/95">
      <form
        onSubmit={handleSubmit}
        className="mx-auto flex max-w-4xl items-center gap-2 rounded-2xl border border-slate-300 bg-white p-2 shadow-sm dark:border-slate-700 dark:bg-slate-900"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about any government service..."
          disabled={loading}
          className="min-w-0 flex-1 bg-transparent px-3 py-3 text-sm outline-none dark:text-white"
        />

        <VoiceButton listening={listening} onClick={onVoice} />

        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="rounded-xl bg-blue-700 p-3 text-white transition hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-40"
        >
          <Send size={20} />
        </button>
      </form>

      <p className="mx-auto mt-2 max-w-4xl text-center text-xs text-slate-400">
        SevaMitra provides guidance based on available government information.
      </p>
    </div>
  );
}
