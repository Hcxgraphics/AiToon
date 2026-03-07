"use client";

import { motion } from "framer-motion";
import { BookOpen, Tag, FileText } from "lucide-react";

export const StoryForm = ({ storyData, onUpdateStory }) => {
  const fields = [
    {
      key: "storyline",
      label: "Storyline",
      icon: <BookOpen size={16} />,
      placeholder: "Describe your comic's main storyline...",
      rows: 3,
      required: true,
    },
    {
      key: "tagline",
      label: "Tagline",
      icon: <Tag size={16} />,
      placeholder: "A short catchy phrase for your comic...",
      rows: 1,
      required: true,
    },
    {
      key: "summary",
      label: "Summary",
      icon: <FileText size={16} />,
      placeholder: "Optional — a brief summary for AI context...",
      rows: 4,
      required: false,
    },
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
          <label className="flex items-center gap-2 text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-2">
            {field.icon}
            {field.label}
            {!field.required && (
              <span className="text-[10px] normal-case tracking-normal text-muted-foreground/60">(optional)</span>
            )}
          </label>
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
