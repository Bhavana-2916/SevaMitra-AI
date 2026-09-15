"use client";

import { useState } from "react";

import Navbar from "@/components/Navbar";
import WelcomeScreen from "@/components/WelcomeScreen";
import MessageBubble from "@/components/MessageBubble";
import ChatBox from "@/components/ChatBox";

import { Language, Message } from "@/types/chat";
import { sendMessage } from "@/lib/api";

export default function Home() {
  const [language, setLanguage] = useState<Language>("English");
  const [darkMode, setDarkMode] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [listening, setListening] = useState(false);

  const handleSend = async () => {
    const question = input.trim();

    if (!question || loading) return;

    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const response = await sendMessage(question, language);

      const aiMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: response.answer,
        service: response.service,
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch {
      const errorMessage: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        content: "Sorry, I couldn't process your request. Please try again.",
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleVoice = () => {
    setListening(!listening);
    // Real speech recognition will be connected later.
  };

  return (
    <main
      className={
        darkMode
          ? "dark min-h-screen bg-slate-950 text-white"
          : "min-h-screen bg-slate-50 text-slate-900"
      }
    >
      <Navbar
        language={language}
        setLanguage={setLanguage}
        darkMode={darkMode}
        setDarkMode={setDarkMode}
      />

      <div className="mx-auto flex min-h-[calc(100vh-73px)] max-w-6xl flex-col">
        {/* Chat area */}
        <div className="flex-1 px-4">
          {messages.length === 0 ? (
            <WelcomeScreen />
          ) : (
            <div className="mx-auto max-w-4xl space-y-6 py-8">
              {messages.map((message) => (
                <MessageBubble key={message.id} message={message} />
              ))}

              {loading && (
                <div className="flex items-center gap-2 text-sm text-slate-500">
                  <span>🤖</span>
                  <span>SevaMitra is thinking...</span>
                  <span className="animate-pulse">● ● ●</span>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Input */}
        <ChatBox
          input={input}
          setInput={setInput}
          onSend={handleSend}
          listening={listening}
          onVoice={handleVoice}
          loading={loading}
        />
      </div>
    </main>
  );
}
