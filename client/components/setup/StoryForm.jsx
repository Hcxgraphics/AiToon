"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { BookOpen, Tag, FileText, Sparkles, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";

const AI_SUGGESTIONS = {
  storyline: [
    "A young vigilante discovers they can enter comic book dimensions, but each world they visit starts collapsing behind them.",
    "In a city where superpowers are common, a powerless detective solves crimes that heroes can't.",
    "Two rival artists discover their drawings come to life — and their creations are at war.",
  ],
  tagline: [
    "Every hero has an origin. This one has a deadline.",
    "Not all battles are fought with fists.",
    "The ink is mightier than the sword.",
    "Between panels, legends are born.",
  ],
  summary: [
    "Set in a neon-lit metropolis, our protagonist navigates a world of shifting alliances while uncovering a conspiracy that threatens reality itself.",
    "A coming-of-age story wrapped in action and mystery, following unlikely heroes as they discover what it truly means to fight for something.",
  ],
};

export const StoryForm = ({ storyData, onUpdateStory }) => {
  const [suggesting, setSuggesting] = useState(null);

  const handleSuggest = (key) => {
    setSuggesting(key);
    // Simulate AI delay
    const handleAISuggest = async (type) => {
  const res = await fetch("http://localhost:8000/ai/suggest", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      type,
      context: storyData.storyline || selectedTheme
    })
  });

  const data = await res.json();

  setStoryData((prev) => ({
    ...prev,
    [type]: data.suggestion
  }));
};  };

  const fields = [
    { key: "storyline", label: "Storyline", icon: <BookOpen size={16} />, placeholder: "Describe your comic's main storyline...", rows: 3, required: true },
    { key: "tagline", label: "Tagline", icon: <Tag size={16} />, placeholder: "A short catchy phrase for your comic...", rows: 1, required: true },
    { key: "summary", label: "Summary", icon: <FileText size={16} />, placeholder: "Optional — a brief summary for AI context...", rows: 4, required: false },
  ];

  return (
    <div className="w-full max-w-xl mx-auto space-y-5">
      {fields.map((field, i) => (
        <motion.div
          key={field.key}
          initial={{ opacity: 0, y: 15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: i * 0.1 }}
        >
          <div className="flex items-center justify-between mb-2">
            <label className="flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground font-semibold">
              {field.icon}
              {field.label}
              {!field.required && (
                <span className="text-[10px] normal-case tracking-normal text-muted-foreground/60">(optional)</span>
              )}
            </label>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => handleSuggest(field.key)}
              disabled={suggesting === field.key}
              className="h-7 px-2.5 text-[11px] gap-1.5 text-primary hover:text-primary hover:bg-primary/10 rounded-lg"
            >
              {suggesting === field.key ? (
                <Loader2 size={12} className="animate-spin" />
              ) : (
                <Sparkles size={12} />
              )}
              AI Suggest
            </Button>
          </div>
          {field.rows > 1 ? (
            <textarea
              value={storyData[field.key] || ""}
              onChange={(e) => onUpdateStory({ ...storyData, [field.key]: e.target.value })}
              placeholder={field.placeholder}
              rows={field.rows}
              className="w-full px-5 py-4 rounded-xl bg-secondary border border-border text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 resize-none transition-all leading-relaxed"
            />
          ) : (
            <input
              type="text"
              value={storyData[field.key] || ""}
              onChange={(e) => onUpdateStory({ ...storyData, [field.key]: e.target.value })}
              placeholder={field.placeholder}
              className="w-full h-12 px-5 rounded-xl bg-secondary border border-border text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
            />
          )}
        </motion.div>
      ))}
    </div>
  );
};
