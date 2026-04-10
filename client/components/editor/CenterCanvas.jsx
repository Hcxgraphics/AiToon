"use client";

import { useState } from "react";
import {
  ZoomIn, ZoomOut, MessageSquare, Grid3x3 as Grid3X3,
  ChevronLeft, ChevronRight, Download, Pencil,
  RefreshCw, Trash2, Copy, Camera
} from "lucide-react";
import { motion } from "framer-motion";
import { GridManager } from "./GridManager";

export const CenterCanvas = ({
  pages,
  selectedPanelId,
  onSelectPanel,
  generatedImages // ✅ NEW PROP
}) => {

  const [currentPageIndex, setCurrentPageIndex] = useState(0);
  const [showBubbles, setShowBubbles] = useState(true);
  const [showGridManager, setShowGridManager] = useState(false);
  const [zoom, setZoom] = useState(100);
  const [gridConfig, setGridConfig] = useState({ rows: 2, cols: 2, preset: "2x2" });

  const currentPage = pages[currentPageIndex] || {panels: []};
  
  console.log('🎨 Canvas Debug:', {
    pagesLength: pages.length,
    currentPageIndex,
    currentPanels: currentPage.panels?.length || 0,
    generatedImagesKeys: Object.keys(generatedImages),
    sampleImage: generatedImages[1]
  });

  return (
    <div className="flex flex-col h-full bg-canvas relative">

      {/* TOP BAR */}
      <div className="flex items-center justify-between px-4 py-2 border-b border-border bg-card/50 backdrop-blur-sm">

        {/* LEFT CONTROLS */}
        <div className="flex items-center gap-1">
          <button onClick={() => setZoom((z) => Math.max(50, z - 10))} className="p-1.5 rounded-md">
            <ZoomOut size={16} />
          </button>

          <span className="text-xs w-10 text-center">{zoom}%</span>

          <button onClick={() => setZoom((z) => Math.min(200, z + 10))} className="p-1.5 rounded-md">
            <ZoomIn size={16} />
          </button>

          <button onClick={() => setShowBubbles(!showBubbles)} className="p-1.5 rounded-md">
            <MessageSquare size={16} />
          </button>

          <button onClick={() => setShowGridManager(!showGridManager)} className="p-1.5 rounded-md">
            <Grid3X3 size={16} />
          </button>
        </div>

        {/* PAGE SWITCH */}
        <div className="flex items-center gap-2">
          <button onClick={() => setCurrentPageIndex((i) => Math.max(0, i - 1))}>
            <ChevronLeft size={16} />
          </button>

          <span className="text-xs font-medium">{currentPage.name}</span>

          <button onClick={() => setCurrentPageIndex((i) => Math.min(pages.length - 1, i + 1))}>
            <ChevronRight size={16} />
          </button>
        </div>

        {/* RIGHT ACTIONS */}
        <div className="flex gap-1">
          <button><Pencil size={16} /></button>
          <button><Download size={16} /></button>
        </div>
      </div>

      <GridManager
        open={showGridManager}
        onClose={() => setShowGridManager(false)}
        config={gridConfig}
        onChange={setGridConfig}
      />

      {/* CANVAS */}
      <div className="flex-1 overflow-auto flex items-center justify-center p-8">
        <div
          className="grid gap-3"
          style={{
            transform: `scale(${zoom / 100})`,
            gridTemplateRows: `repeat(${gridConfig.rows}, 1fr)`,
            gridTemplateColumns: `repeat(${gridConfig.cols}, 1fr)`,
            height: "clamp(400px, 80vh, 900px)",
            maxWidth: "700px",
            width: "100%",
          }}

        >
          {currentPage.panels.map((panel, i) => {

            const isSelected = selectedPanelId === panel.id;

            // ✅ IMPORTANT: Use generated images
            const img = generatedImages?.[panel.id];

            return (
              <motion.div
                key={panel.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.05 }}
                onClick={() => onSelectPanel(panel.id)}
                className={`relative rounded-lg overflow-hidden cursor-pointer aspect-[3/4] ${
                  isSelected ? "ring-2 ring-primary" : "ring-1 ring-border"
                }`}

              >
                {img ? (
                  <img 
                    src={img} 
                    crossOrigin="anonymous"
                    alt={`Panel ${panel.id}`}
                    className="w-full h-full object-cover"
                    onLoad={() => console.log(`✅ Panel ${panel.id} loaded:`, img)}
                    onError={(e) => {
                      console.error(`❌ Panel ${panel.id} failed:`, img);
                      e.target.style.display = 'none';
                    }}
                  />
                ) : (

                  <div className="w-full h-full bg-secondary flex items-center justify-center">
                    <span>{panel.name}</span>
                  </div>
                )}

                {/* Dialogue */}
                {showBubbles && panel.dialogue && (
                  <div className="absolute bottom-3 left-3 right-3 text-xs bg-black/70 text-white p-2 rounded">
                    {panel.dialogue}
                  </div>
                )}

              </motion.div>
            );
          })}
        </div>
      </div>

      {/* THUMBNAILS */}
      <div className="border-t px-4 py-2">
        <div className="flex gap-2 overflow-x-auto">
          {pages.flatMap((page) =>
            page.panels.map((panel) => {
              const thumbImg = generatedImages?.[panel.id];

              return (
                <button key={panel.id} onClick={() => onSelectPanel(panel.id)} className="w-16 h-10 flex-shrink-0">
                  {thumbImg ? (
                    <img 
                      src={thumbImg} 
                      crossOrigin="anonymous"
                      alt={`Thumb ${panel.id}`}
                      className="w-full h-full object-cover rounded"
                      onError={(e) => e.target.style.display = 'none'}
                    />
                  ) : (
                    <div className="bg-secondary w-full h-full rounded flex items-center justify-center text-xs text-muted-foreground">
                      {panel.id}
                    </div>
                  )}
                </button>
              );
            })
          )}

        </div>
      </div>
    </div>
  );
};