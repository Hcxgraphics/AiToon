'use client';

import { useState } from "react";
import { ChevronRight, ChevronDown, Plus, FileText, MoreHorizontal, Check, Loader2, AlertTriangle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

const statusIcon = (status) => {
  switch (status) {
    case "generated": return <Check size={12} className="text-success" />;
    case "generating": return <Loader2 size={12} className="text-warning animate-spin" />;
    case "needs-dialogue": return <AlertTriangle size={12} className="text-warning" />;
    case "error": return <AlertTriangle size={12} className="text-destructive" />;
    default: return <div className="w-3 h-3 rounded-full border border-muted-foreground/30" />;
  }
};

export const ComicTree = ({ pages, selectedPanelId, onSelectPanel }) => {
  const [expandedPages, setExpandedPages] = useState(new Set(pages.map((p) => p.id)));

  const togglePage = (pageId) => {
    setExpandedPages((prev) => {
      const next = new Set(prev);
      if (next.has(pageId)) next.delete(pageId);
      else next.add(pageId);
      return next;
    });
  };

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-3 py-2 border-b border-border">
        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Comic Structure</span>
        <button className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors">
          <Plus size={14} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar p-2 space-y-0.5">
        {pages.map((page) => (
          <div key={page.id}>
            <button
              onClick={() => togglePage(page.id)}
              className="w-full flex items-center gap-1.5 px-2 py-1.5 rounded-md text-sm text-foreground hover:bg-surface-hover transition-colors group"
            >
              {expandedPages.has(page.id) ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
              <FileText size={14} className="text-muted-foreground" />
              <span className="flex-1 text-left">{page.name}</span>
              <span className="text-[10px] text-muted-foreground">{page.panels.length}p</span>
              <MoreHorizontal size={14} className="opacity-0 group-hover:opacity-100 text-muted-foreground transition-opacity" />
            </button>

            <AnimatePresence>
              {expandedPages.has(page.id) && (
                <motion.div
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: "auto", opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  transition={{ duration: 0.15 }}
                  className="overflow-hidden"
                >
                  <div className="ml-4 pl-3 border-l border-border/50 space-y-0.5 py-0.5">
                    {page.panels.map((panel) => (
                      <button
                        key={panel.id}
                        onClick={() => onSelectPanel(panel.id)}
                        className={`w-full flex items-center gap-2 px-2 py-1.5 rounded-md text-sm transition-all ${
                          selectedPanelId === panel.id
                            ? "bg-primary/15 text-primary glow-border"
                            : "text-secondary-foreground hover:bg-surface-hover"
                        }`}
                      >
                        {statusIcon(panel.status)}
                        <span className="flex-1 text-left">{panel.name}</span>
                      </button>
                    ))}
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        ))}
      </div>
    </div>
  );
};
