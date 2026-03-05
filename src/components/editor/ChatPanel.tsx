import { useState } from "react";
import { Send, RotateCcw, Sparkles, History, X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const SUGGESTED_PROMPTS = [
  "Create opening scene",
  "Add hero to panel 2",
  "Rewrite dialogue for tension",
  "Change lighting to night",
];

const CONTEXT_CHIPS = ["+Hero", "+Villain", "+Panel 2", "+Night scene"];

type Message = { role: "user" | "assistant"; content: string };

interface ChatPanelProps {
  allVersions: { id: string; label: string; timestamp: string; panelName: string }[];
}

export const ChatPanel = ({ allVersions }: ChatPanelProps) => {
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Welcome to your comic studio! I can help you create scenes, write dialogue, and design panels. What would you like to work on?" },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const sendMessage = () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");
    setIsTyping(true);
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "I'll work on that for you. Generating the scene with the specified parameters..." },
      ]);
      setIsTyping(false);
    }, 1500);
  };

  const injectChip = (chip: string) => {
    setInput((prev) => (prev ? `${prev} ${chip}` : chip));
  };

  return (
    <div className="flex flex-col h-full bg-card relative">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border flex-shrink-0">
        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">AI Chat</span>
        <button
          onClick={() => setShowHistory(true)}
          className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors"
          title="Version History"
        >
          <History size={15} />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-3">
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2 }}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div className={`max-w-[85%] rounded-lg px-3 py-2 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-primary text-primary-foreground"
                  : "bg-secondary text-secondary-foreground"
              }`}>
                {msg.content}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <div className="flex justify-start">
            <div className="bg-secondary rounded-lg px-3 py-2 text-sm">
              <span className="inline-flex gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse [animation-delay:0.2s]" />
                <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse [animation-delay:0.4s]" />
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Bottom: Suggestions, chips, input */}
      <div className="px-3 pb-2 flex-shrink-0">
        <div className="flex flex-wrap gap-1.5 mb-2">
          {SUGGESTED_PROMPTS.map((prompt) => (
            <button
              key={prompt}
              onClick={() => setInput(prompt)}
              className="text-[10px] px-2 py-1 rounded-md bg-secondary text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors"
            >
              <Sparkles size={10} className="inline mr-1" /> {prompt}
            </button>
          ))}
        </div>

        <div className="flex flex-wrap gap-1 mb-2">
          {CONTEXT_CHIPS.map((chip) => (
            <button
              key={chip}
              onClick={() => injectChip(chip)}
              className="text-[10px] px-2 py-0.5 rounded-full border border-primary/30 text-primary hover:bg-primary/10 transition-colors"
            >
              {chip}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-2 bg-secondary rounded-lg p-1.5">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Describe your scene..."
            className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground outline-none px-2"
          />
          <button
            onClick={() => setMessages([messages[0]])}
            className="p-1.5 rounded-md text-muted-foreground hover:text-foreground transition-colors"
            title="Reset chat"
          >
            <RotateCcw size={14} />
          </button>
          <button
            onClick={sendMessage}
            disabled={!input.trim()}
            className="p-1.5 rounded-md bg-primary text-primary-foreground disabled:opacity-40 transition-all hover:opacity-90"
          >
            <Send size={14} />
          </button>
        </div>
      </div>

      {/* Version History Modal */}
      <AnimatePresence>
        {showHistory && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-background/80 backdrop-blur-sm z-50 flex flex-col"
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-border">
              <span className="text-sm font-semibold text-foreground">Version History</span>
              <button onClick={() => setShowHistory(false)} className="p-1 rounded-md text-muted-foreground hover:text-foreground transition-colors">
                <X size={16} />
              </button>
            </div>
            <div className="flex-1 overflow-y-auto custom-scrollbar p-4 space-y-2">
              {allVersions.length > 0 ? allVersions.map((v) => (
                <div key={`${v.panelName}-${v.id}`} className="flex items-center justify-between px-3 py-2 rounded-lg bg-secondary text-sm">
                  <div>
                    <span className="text-foreground">{v.label}</span>
                    <span className="text-[10px] text-muted-foreground ml-2">({v.panelName})</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-muted-foreground">{v.timestamp}</span>
                    <button className="text-[10px] px-2 py-0.5 rounded bg-primary/10 text-primary hover:bg-primary/20 transition-colors">Revert</button>
                  </div>
                </div>
              )) : (
                <p className="text-sm text-muted-foreground text-center py-8">No versions yet</p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};
