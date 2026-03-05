import { useState } from "react";
import { LeftPanel } from "./LeftPanel";
import { CenterCanvas } from "./CenterCanvas";
import { ChatPanel } from "./ChatPanel";

export type PanelData = {
  id: string;
  name: string;
  status: "idle" | "generating" | "generated" | "needs-dialogue" | "editing" | "error";
  image?: string;
  dialogue?: string;
  characters: string[];
  expression?: string;
  pose?: string;
  background?: string;
  bubbleType?: "normal" | "thought" | "whisper" | "shout" | "narration";
  notes?: string;
  versions?: { id: string; label: string; timestamp: string }[];
};

export type PageData = {
  id: string;
  name: string;
  panels: PanelData[];
};

export type GridLayout = {
  id: string;
  name: string;
  rows: number[];
  cols: number[];
};

export const EditorLayout = () => {
  const [selectedPanelId, setSelectedPanelId] = useState<string | null>("p1-1");
  const [pages, setPages] = useState<PageData[]>([
    {
      id: "page-1",
      name: "Page 1",
      panels: [
        {
          id: "p1-1",
          name: "Panel 1",
          status: "generated",
          characters: ["Hero"],
          expression: "Determined",
          pose: "Standing",
          dialogue: "The city never sleeps... and neither do I.",
          background: "Rooftop at night",
          bubbleType: "narration",
          notes: "Opening scene — establish mood and setting",
          versions: [
            { id: "v1", label: "v1 — initial", timestamp: "2 hours ago" },
            { id: "v2", label: "v2 — dialogue change", timestamp: "1 hour ago" },
          ],
        },
        {
          id: "p1-2",
          name: "Panel 2",
          status: "generated",
          characters: ["Hero", "Villain"],
          expression: "Tense",
          pose: "Confrontation",
          dialogue: "You shouldn't have come here.",
          background: "Dark alley",
          bubbleType: "normal",
          notes: "Build tension before fight",
          versions: [{ id: "v1", label: "v1 — initial", timestamp: "1 hour ago" }],
        },
        {
          id: "p1-3",
          name: "Panel 3",
          status: "generating",
          characters: ["Hero"],
          expression: "Action",
          pose: "Leaping",
          background: "Explosion",
          bubbleType: "shout",
          notes: "Climactic action moment",
          versions: [],
        },
      ],
    },
    {
      id: "page-2",
      name: "Page 2",
      panels: [
        {
          id: "p2-1",
          name: "Panel 1",
          status: "needs-dialogue",
          characters: ["Villain"],
          expression: "Menacing",
          pose: "Close-up",
          background: "Shadow",
          bubbleType: "whisper",
          notes: "Villain reveal",
          versions: [],
        },
        {
          id: "p2-2",
          name: "Panel 2",
          status: "idle",
          characters: [],
          notes: "To be designed",
          versions: [],
        },
      ],
    },
  ]);

  const allPanels = pages.flatMap((p) => p.panels);
  const selectedPanel = allPanels.find((p) => p.id === selectedPanelId) || null;

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-background">
      {/* LEFT: Inspector + Pages + Cast */}
      <div className="w-[25%] min-w-[280px] max-w-[360px] border-r border-border flex flex-col">
        <LeftPanel
          pages={pages}
          selectedPanel={selectedPanel}
          selectedPanelId={selectedPanelId}
          onSelectPanel={setSelectedPanelId}
        />
      </div>

      {/* CENTER: Canvas */}
      <div className="flex-1 flex flex-col min-w-0">
        <CenterCanvas
          pages={pages}
          selectedPanelId={selectedPanelId}
          onSelectPanel={setSelectedPanelId}
        />
      </div>

      {/* RIGHT: Chat */}
      <div className="w-[25%] min-w-[280px] max-w-[360px] border-l border-border flex flex-col">
        <ChatPanel allVersions={allPanels.flatMap((p) => (p.versions || []).map((v) => ({ ...v, panelName: p.name })))} />
      </div>
    </div>
  );
};
