import { Volume2 } from "lucide-react";
import { Message } from "@/types/chat";
import ServiceCard from "./ServiceCard";

interface MessageBubbleProps {
  message: Message;
}

export default function MessageBubble({ message }: MessageBubbleProps) {
  const isUser = message.role === "user";

  const speak = () => {
    if ("speechSynthesis" in window) {
      const speech = new SpeechSynthesisUtterance(message.content);
      window.speechSynthesis.speak(speech);
    }
  };

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[90%] ${
          isUser
            ? "rounded-2xl rounded-br-md bg-blue-700 px-5 py-3 text-white"
            : "w-full max-w-2xl"
        }`}
      >
        {!isUser && (
          <div className="mb-2 flex items-center gap-2 text-sm font-semibold">
            🤖 SevaMitra AI
            <button
              onClick={speak}
              className="rounded-md p-1 hover:bg-slate-100 dark:hover:bg-slate-800"
              title="Read aloud"
            >
              <Volume2 size={16} />
            </button>
          </div>
        )}

        <p className="whitespace-pre-line text-sm leading-6">
          {message.content}
        </p>

        {message.service && <ServiceCard service={message.service} />}
      </div>
    </div>
  );
}
