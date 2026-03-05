import { RefreshCw, Camera, Copy, Trash2, Sparkles, History, StickyNote } from "lucide-react";
import { motion } from "framer-motion";
import type { PanelData } from "./EditorLayout";

const BUBBLE_TYPES = ["normal", "thought", "whisper", "shout", "narration"] as const;

const AI_SUGGESTIONS = [
  "Improve dialogue",
  "Add reaction panel",
  "Adjust pacing",
  "Change camera angle",
];

interface RightInspectorProps {
  panel: PanelData | null;
}

export const RightInspector = ({ panel }: RightInspectorProps) => {
  if (!panel) {
    return (
      <div className="flex items-center justify-center h-full bg-card">
        <p className="text-sm text-muted-foreground">Select a panel to inspect</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full bg-card overflow-y-auto custom-scrollbar">
      {/* Header */}
      <div className="px-4 py-3 border-b border-border">
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

      <div className="p-4 space-y-5">
        {/* Quick Actions */}
        <Section title="Quick Actions">
          <div className="grid grid-cols-2 gap-1.5">
            {[
              { icon: <RefreshCw size={13} />, label: "Regenerate" },
              { icon: <Camera size={13} />, label: "Camera" },
              { icon: <Copy size={13} />, label: "Duplicate" },
              { icon: <Trash2 size={13} />, label: "Delete" },
            ].map((a) => (
              <button key={a.label} className="flex items-center gap-1.5 px-2.5 py-2 rounded-md bg-secondary text-secondary-foreground text-xs hover:bg-surface-hover transition-colors">
                {a.icon} {a.label}
              </button>
            ))}
          </div>
        </Section>

        {/* Characters */}
        <Section title="Characters">
          <div className="flex flex-wrap gap-1.5">
            {panel.characters.length > 0 ? panel.characters.map((c) => (
              <span key={c} className="text-xs px-2.5 py-1 rounded-full bg-primary/15 text-primary border border-primary/20">
                {c}
              </span>
            )) : <span className="text-xs text-muted-foreground">No characters</span>}
          </div>
        </Section>

        {/* Properties */}
        <Section title="Properties">
          <div className="space-y-2">
            <Field label="Expression" value={panel.expression} />
            <Field label="Pose" value={panel.pose} />
            <Field label="Background" value={panel.background} />
          </div>
        </Section>

        {/* Dialogue */}
        <Section title="Dialogue">
          <textarea
            defaultValue={panel.dialogue || ""}
            placeholder="Enter dialogue..."
            className="w-full bg-secondary text-foreground text-sm rounded-lg p-2.5 min-h-[60px] resize-none outline-none focus:ring-1 focus:ring-primary/50 placeholder:text-muted-foreground"
          />
          <div className="flex flex-wrap gap-1 mt-2">
            {BUBBLE_TYPES.map((type) => (
              <button
                key={type}
                className={`text-[10px] px-2 py-1 rounded-md capitalize transition-colors ${
                  panel.bubbleType === type
                    ? "bg-primary text-primary-foreground"
                    : "bg-secondary text-muted-foreground hover:text-foreground"
                }`}
              >
                {type}
              </button>
            ))}
          </div>
        </Section>

        {/* Scene Notes */}
        <Section title="Scene Notes" icon={<StickyNote size={12} />}>
          <textarea
            defaultValue={panel.notes || ""}
            placeholder="Add narrative context..."
            className="w-full bg-secondary text-foreground text-sm rounded-lg p-2.5 min-h-[50px] resize-none outline-none focus:ring-1 focus:ring-primary/50 placeholder:text-muted-foreground"
          />
        </Section>

        {/* Version History */}
        {panel.versions && panel.versions.length > 0 && (
          <Section title="Versions" icon={<History size={12} />}>
            <div className="space-y-1">
              {panel.versions.map((v, i) => (
                <button
                  key={v.id}
                  className={`w-full flex items-center justify-between px-2.5 py-1.5 rounded-md text-xs transition-colors ${
                    i === panel.versions!.length - 1
                      ? "bg-primary/10 text-primary"
                      : "bg-secondary text-muted-foreground hover:text-foreground hover:bg-surface-hover"
                  }`}
                >
                  <span>{v.label}</span>
                  <span className="text-[10px]">{v.timestamp}</span>
                </button>
              ))}
            </div>
          </Section>
        )}

        {/* AI Suggestions */}
        <Section title="AI Suggestions" icon={<Sparkles size={12} />}>
          <div className="space-y-1">
            {AI_SUGGESTIONS.map((s) => (
              <button
                key={s}
                className="w-full flex items-center gap-2 px-2.5 py-2 rounded-md text-xs bg-primary/5 text-primary border border-primary/10 hover:bg-primary/10 transition-colors text-left"
              >
                <Sparkles size={11} className="flex-shrink-0" />
                {s}
              </button>
            ))}
          </div>
        </Section>
      </div>
    </div>
  );
};

const Section = ({ title, icon, children }: { title: string; icon?: React.ReactNode; children: React.ReactNode }) => (
  <motion.div initial={{ opacity: 0, y: 4 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.2 }}>
    <div className="flex items-center gap-1.5 mb-2">
      {icon}
      <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider">{title}</span>
    </div>
    {children}
  </motion.div>
);

const Field = ({ label, value }: { label: string; value?: string }) => (
  <div className="flex items-center justify-between">
    <span className="text-xs text-muted-foreground">{label}</span>
    <input
      defaultValue={value || ""}
      className="text-xs text-foreground bg-secondary rounded-md px-2 py-1 w-[55%] outline-none focus:ring-1 focus:ring-primary/50"
    />
  </div>
);
