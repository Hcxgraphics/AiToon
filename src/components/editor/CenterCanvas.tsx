import { useState } from "react";
import {
  ZoomIn, ZoomOut, MessageSquare, Grid3X3, ChevronLeft, ChevronRight,
  Download, Pencil, RefreshCw, Trash2, Copy, Camera,
} from "lucide-react";
import { motion } from "framer-motion";
import type { PageData } from "./EditorLayout";
import { GridManager, type GridConfig } from "./GridManager";
import comicPanel1 from "@/assets/comic-panel-1.jpg";
import comicPanel2 from "@/assets/comic-panel-2.jpg";
import comicPanel3 from "@/assets/comic-panel-3.jpg";
import comicPanel4 from "@/assets/comic-panel-4.jpg";

const panelImages: Record<string, string> = {
  "p1-1": comicPanel1,
  "p1-2": comicPanel2,
  "p1-3": comicPanel3,
  "p2-1": comicPanel4,
};

interface CenterCanvasProps {
  pages: PageData[];
  selectedPanelId: string | null;
  onSelectPanel: (id: string) => void;
}

export const CenterCanvas = ({ pages, selectedPanelId, onSelectPanel }: CenterCanvasProps) => {
  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [showBubbles, setShowBubbles] = useState(true);
  const [showGridManager, setShowGridManager] = useState(false);
  const [zoom, setZoom] = useState(100);
  const [gridConfig, setGridConfig] = useState<GridConfig>({ rows: 2, cols: 2, preset: "2x2" });

  const currentPage = pages[currentPageIndex];

  return (
    <div className="flex flex-col h-full bg-canvas relative">
      {/* Toolbar */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-card/50 backdrop-blur-sm">
        <div className="flex items-center gap-1">
          <button onClick={() => setZoom((z) => Math.max(50, z - 10))} className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors">
            <ZoomOut size={16} />
          </button>
          <span className="text-xs text-muted-foreground w-10 text-center">{zoom}%</span>
          <button onClick={() => setZoom((z) => Math.min(200, z + 10))} className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors">
            <ZoomIn size={16} />
          </button>
          <div className="w-px h-4 bg-border mx-1" />
          <button onClick={() => setShowBubbles(!showBubbles)} className={`p-1.5 rounded-md transition-colors ${showBubbles ? "text-primary bg-primary/10" : "text-muted-foreground hover:text-foreground hover:bg-surface-hover"}`}>
            <MessageSquare size={16} />
          </button>
          <button onClick={() => setShowGridManager(!showGridManager)} className={`p-1.5 rounded-md transition-colors ${showGridManager ? "text-primary bg-primary/10" : "text-muted-foreground hover:text-foreground hover:bg-surface-hover"}`}>
            <Grid3X3 size={16} />
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button onClick={() => setCurrentPageIndex((i) => Math.max(0, i - 1))} disabled={currentPageIndex === 0} className="p-1.5 rounded-md text-muted-foreground hover:text-foreground disabled:opacity-30 transition-colors">
            <ChevronLeft size={16} />
          </button>
          <span className="text-xs text-foreground font-medium">{currentPage.name}</span>
          <button onClick={() => setCurrentPageIndex((i) => Math.min(pages.length - 1, i + 1))} disabled={currentPageIndex === pages.length - 1} className="p-1.5 rounded-md text-muted-foreground hover:text-foreground disabled:opacity-30 transition-colors">
            <ChevronRight size={16} />
          </button>
        </div>

        <div className="flex items-center gap-1">
          <button className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors" title="Edit Mode">
            <Pencil size={16} />
          </button>
          <button className="p-1.5 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors" title="Export">
            <Download size={16} />
          </button>
        </div>
      </div>

      {/* Grid Manager Popover */}
      <GridManager
        open={showGridManager}
        onClose={() => setShowGridManager(false)}
        config={gridConfig}
        onChange={setGridConfig}
      />

      {/* Canvas */}
      <div className="flex-1 overflow-auto custom-scrollbar flex items-center justify-center p-8">
        <div
          className="grid gap-3"
          style={{
            transform: `scale(${zoom / 100})`,
            transformOrigin: "center center",
            gridTemplateRows: `repeat(${gridConfig.rows}, 1fr)`,
            gridTemplateColumns: `repeat(${gridConfig.cols}, 1fr)`,
            maxWidth: "700px",
            width: "100%",
          }}
        >
          {currentPage.panels.map((panel, i) => {
            const isSelected = selectedPanelId === panel.id;
            const img = panelImages[panel.id];

            return (
              <motion.div
                key={panel.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                onClick={() => onSelectPanel(panel.id)}
                className={`relative rounded-lg overflow-hidden cursor-pointer group transition-all duration-200 ${
                  isSelected ? "ring-2 ring-primary glow-accent" : "ring-1 ring-border hover:ring-primary/40"
                }`}
                style={{ aspectRatio: gridConfig.cols === 1 ? "16/9" : "4/3" }}
              >
                {img ? (
                  <img src={img} alt={panel.name} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full bg-secondary flex items-center justify-center">
                    <span className="text-muted-foreground text-sm">{panel.name}</span>
                  </div>
                )}

                {panel.status === "generating" && (
                  <div className="absolute inset-0 shimmer opacity-60" />
                )}

                {showBubbles && panel.dialogue && (
                  <div className="absolute bottom-3 left-3 right-3">
                    <div className={`rounded-lg px-3 py-2 text-xs max-w-[80%] ${
                      panel.bubbleType === "thought" ? "bg-foreground/80 text-background italic rounded-[20px]" :
                      panel.bubbleType === "narration" ? "bg-background/90 text-foreground border border-border" :
                      panel.bubbleType === "shout" ? "bg-foreground text-background font-bold uppercase" :
                      panel.bubbleType === "whisper" ? "bg-foreground/60 text-background text-[10px] italic" :
                      "bg-foreground/90 text-background"
                    }`}>
                      {panel.dialogue}
                    </div>
                  </div>
                )}

                {/* Hover actions — includes Change camera angle */}
                <div className="absolute top-2 right-2 flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  {[
                    { icon: <RefreshCw size={12} />, title: "Regenerate" },
                    { icon: <MessageSquare size={12} />, title: "Edit dialogue" },
                    { icon: <Copy size={12} />, title: "Duplicate" },
                    { icon: <Camera size={12} />, title: "Camera angle" },
                    { icon: <Trash2 size={12} />, title: "Delete" },
                  ].map((action) => (
                    <button
                      key={action.title}
                      title={action.title}
                      className="p-1.5 rounded-md bg-background/80 text-foreground hover:bg-primary hover:text-primary-foreground transition-colors backdrop-blur-sm"
                      onClick={(e) => e.stopPropagation()}
                    >
                      {action.icon}
                    </button>
                  ))}
                </div>

                <div className="absolute top-2 left-2 text-[10px] px-1.5 py-0.5 rounded bg-background/70 text-foreground backdrop-blur-sm">
                  {panel.name}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Mini Timeline */}
      <div className="border-t border-border bg-card/50 backdrop-blur-sm px-4 py-2">
        <div className="flex items-center gap-2 overflow-x-auto custom-scrollbar">
          {pages.flatMap((page) =>
            page.panels.map((panel) => (
              <button
                key={panel.id}
                onClick={() => onSelectPanel(panel.id)}
                className={`flex-shrink-0 w-16 h-10 rounded-md overflow-hidden border transition-all ${
                  selectedPanelId === panel.id
                    ? "border-primary ring-1 ring-primary/50"
                    : "border-border/50 hover:border-muted-foreground/50"
                }`}
              >
                {panelImages[panel.id] ? (
                  <img src={panelImages[panel.id]} alt={panel.name} className="w-full h-full object-cover" />
                ) : (
                  <div className="w-full h-full bg-secondary flex items-center justify-center">
                    <span className="text-[8px] text-muted-foreground">{panel.name}</span>
                  </div>
                )}
              </button>
            ))
          )}
        </div>
      </div>
    </div>
  );
};
