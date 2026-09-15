"use client";

import { Mic, MicOff } from "lucide-react";

interface VoiceButtonProps {
  listening: boolean;
  onClick: () => void;
}

export default function VoiceButton({ listening, onClick }: VoiceButtonProps) {
  return (
    <button
      onClick={onClick}
      title={listening ? "Stop listening" : "Voice input"}
      className={`rounded-xl p-3 transition ${
        listening
          ? "bg-red-500 text-white"
          : "text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800"
      }`}
    >
      {listening ? <MicOff size={20} /> : <Mic size={20} />}
    </button>
  );
}
