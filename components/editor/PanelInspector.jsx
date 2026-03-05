'use client';

import { Sparkles, StickyNote } from "lucide-react";
import { motion } from "framer-motion";

const BUBBLE_TYPES = ["normal", "thought", "whisper", "shout", "narration"];

const DIALOGUE_SUGGESTIONS = ["Improve dialogue", "Add reaction panel"];
const NOTES_SUGGESTIONS = ["Adjust pacing", "Change camera angle"];

export const PanelInspector = ({ panel }) => {
  if (!panel) {
    return (
      <div className="flex items-center justify-center h-full bg-card">
        <p className="text-sm text-muted-foreground">Select a panel to edit</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="px-4 py-3 border-b border-border flex-shrink-0">
        <h3 className="text-sm font-semibold text-foreground">{panel.name}</h3>
        <div className="flex items-center gap-1.5 mt-1">
          <div className={`w-2 h-2 rounded-full ${
            panel.status === "generated" ? "bg-success" :
            panel.status === "generating" ? "bg-warning animate-pulse" :
            panel.status === "error" ? "bg-destructive" :
            "bg-muted-foreground/40"
          }`} />
          <span className="text-[10px] text-muted-foreground capitalize">{panel.status.replace("-", " ")}</span>
        </div>
      </div>

      <div className="flex-1 p-3 space-y-3 overflow-y-auto custom-scrollbar">
        <Field label="Characters">
          <div className="flex flex-wrap gap-1">
            {panel.characters.length > 0 ? panel.characters.map((c) => (
              <span key={c} className="text-[11px] px-2 py-0.5 rounded-full bg-primary/15 text-primary border border-primary/20">
                {c}
              </span>
            )) : <span className="text-[11px] text-muted-foreground">None</span>}
          </div>
        </Field>

        <div className="grid grid-cols-2 gap-2">
          <InputField label="Expression" value={panel.expression} />
          <InputField label="Pose" value={panel.pose} />
        </div>

        <InputField label="Background" value={panel.background} />

        <Field label="Dialogue">
          <textarea
            defaultValue={panel.dialogue || ""}
            placeholder="Enter dialogue..."
            className="w-full bg-secondary text-foreground text-xs rounded-lg p-2 min-h-[48px] resize-none outline-none focus:ring-1 focus:ring-primary/50 placeholder:text-muted-foreground"
          />
          <div className="flex flex-wrap gap-1 mt-1.5">
            {BUBBLE_TYPES.map((type) => (
              <button
                key={type}
                className={`text-[10px] px-1.5 py-0.5 rounded-md capitalize transition-colors ${
                  panel.bubbleType === type
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-muted-foreground hover:text-foreground"
                }`}
              >
                {type}
              </button>
            ))}
          </div>
          <div className="flex flex-wrap gap-1 mt-1.5">
            {DIALOGUE_SUGGESTIONS.map((s) => (
              <button key={s} className="flex items-center gap-1 text-[10px] px-2 py-1 rounded-md bg-primary/5 text-primary border border-primary/10 hover:bg-primary/10 transition-colors">
                <Sparkles size={9} /> {s}
              </button>
            ))}
          </div>
        </Field>

        <Field label="Scene Notes" icon={<StickyNote size={11} />}>
          <textarea
            defaultValue={panel.notes || ""}
            placeholder="Add narrative context..."
            className="w-full bg-secondary text-foreground text-xs rounded-lg p-2 min-h-[40px] resize-none outline-none focus:ring-1 focus:ring-primary/50 placeholder:text-muted-foreground"
          />
          <div className="flex flex-wrap gap-1 mt-1.5">
            {NOTES_SUGGESTIONS.map((s) => (
              <button key={s} className="flex items-center gap-1 text-[10px] px-2 py-1 rounded-md bg-primary/5 text-primary border border-primary/10 hover:bg-primary/10 transition-colors">
                <Sparkles size={9} /> {s}
              </button>
            ))}
          </div>
        </Field>
      </div>
    </div>
  );
};

const Field = ({ label, icon, children }) => (
  <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.15 }}>
    <div className="flex items-center gap-1 mb-1">
      {icon}
      <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">{label}</span>
    </div>
    {children}
  </motion.div>
);

const InputField = ({ label, value }) => (
  <div>
    <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider block mb-1">{label}</span>
    <input
      defaultValue={value || ""}
      className="w-full text-xs text-foreground bg-secondary rounded-md px-2 py-1.5 outline-none focus:ring-1 focus:ring-primary/50"
    />
  </div>
);
