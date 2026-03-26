'use client';

import { X, Plus, Minus, LayoutGrid } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const PRESET_LAYOUTS = [
  { id: "2-row", name: "2 Vertical", rows: 2, cols: 1 },
  { id: "3-row", name: "3 Vertical", rows: 3, cols: 1 },
  { id: "4-row", name: "4 Vertical", rows: 4, cols: 1 },
  { id: "2x2", name: "2×2 Grid", rows: 2, cols: 2 },
  { id: "3x1-1x2", name: "3+1 Split", rows: 3, cols: 1 },
  { id: "webtoon", name: "Webtoon Strip", rows: 5, cols: 1 },
];

export const GridManager = ({ open, onClose, config, onChange }) => {
  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          className="absolute top-12 left-4 z-50 w-64 bg-card border border-border rounded-xl shadow-lg overflow-hidden"
        >
          <div className="flex items-center justify-between px-3 py-2 border-b border-border">
            <div className="flex items-center gap-1.5">
              <LayoutGrid size={13} className="text-primary" />
              <span className="text-xs font-semibold text-foreground">Grid Layout</span>
            </div>
            <button onClick={onClose} className="p-1 rounded text-muted-foreground hover:text-foreground transition-colors">
              <X size={14} />
            </button>
          </div>

          <div className="p-3 border-b border-border">
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider block mb-2">Presets</span>
            <div className="grid grid-cols-3 gap-1.5">
              {PRESET_LAYOUTS.map((preset) => (
                <button
                  key={preset.id}
                  onClick={() => onChange({ rows: preset.rows, cols: preset.cols, preset: preset.id })}
                  className={`flex flex-col items-center gap-1 p-2 rounded-lg text-[10px] transition-colors ${
                    config.preset === preset.id
                      ? "bg-primary/15 text-primary border border-primary/30"
                      : "bg-secondary text-muted-foreground hover:text-foreground hover:bg-surface-hover"
                  }`}
                >
                  <PresetIcon rows={preset.rows} cols={preset.cols} active={config.preset === preset.id} />
                  {preset.name}
                </button>
              ))}
            </div>
          </div>

          <div className="p-3">
            <span className="text-[10px] font-semibold text-muted-foreground uppercase tracking-wider block mb-2">Manual Grid</span>
            <div className="flex items-center gap-4">
              <ControlRow
                label="Rows"
                value={config.rows}
                onChange={(v) => onChange({ ...config, rows: v, preset: null })}
              />
              <ControlRow
                label="Cols"
                value={config.cols}
                onChange={(v) => onChange({ ...config, cols: v, preset: null })}
              />
            </div>

            <div className="mt-3 p-2 bg-secondary rounded-lg">
              <div
                className="grid gap-1 w-full"
                style={{
                  gridTemplateRows: `repeat(${config.rows}, 1fr)`,
                  gridTemplateColumns: `repeat(${config.cols}, 1fr)`,
                  aspectRatio: `${config.cols} / ${config.rows}`,
                }}
              >
                {Array.from({ length: config.rows * config.cols }).map((_, i) => (
                  <div key={i} className="rounded bg-muted-foreground/20 border border-border/50 min-h-[12px]" />
                ))}
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};

const ControlRow = ({ label, value, onChange }) => (
  <div className="flex items-center gap-2">
    <span className="text-[11px] text-muted-foreground w-8">{label}</span>
    <button
      onClick={() => onChange(Math.max(1, value - 1))}
      className="p-1 rounded bg-secondary text-muted-foreground hover:text-foreground transition-colors"
    >
      <Minus size={12} />
    </button>
    <span className="text-xs text-foreground w-4 text-center">{value}</span>
    <button
      onClick={() => onChange(Math.min(6, value + 1))}
      className="p-1 rounded bg-secondary text-muted-foreground hover:text-foreground transition-colors"
    >
      <Plus size={12} />
    </button>
  </div>
);

const PresetIcon = ({ rows, cols, active }) => (
  <div
    className="grid gap-[2px] w-6 h-8"
    style={{
      gridTemplateRows: `repeat(${Math.min(rows, 4)}, 1fr)`,
      gridTemplateColumns: `repeat(${cols}, 1fr)`,
    }}
  >
    {Array.from({ length: Math.min(rows, 4) * cols }).map((_, i) => (
      <div key={i} className={`rounded-[1px] ${active ? "bg-primary/60" : "bg-muted-foreground/30"}`} />
    ))}
  </div>
);
