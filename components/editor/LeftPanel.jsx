'use client';

import { useState } from "react";
import { PanelInspector } from "./PanelInspector";
import { ComicTree } from "./ComicTree";
import { CharacterLibrary } from "./CharacterLibrary";
import { FileSliders as Sliders, FolderTree, Users } from "lucide-react";

export const LeftPanel = ({ pages, selectedPanel, selectedPanelId, onSelectPanel }) => {
  const [activeTab, setActiveTab] = useState("inspector");

  const tabs = [
    { id: "inspector", icon: <Sliders size={16} />, label: "Panel" },
    { id: "tree", icon: <FolderTree size={16} />, label: "Pages" },
    { id: "characters", icon: <Users size={16} />, label: "Cast" },
  ];

  return (
    <div className="flex flex-col h-full bg-card">
      <div className="flex border-b border-border">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex-1 flex items-center justify-center gap-1.5 py-3 text-xs font-medium transition-colors ${
              activeTab === tab.id
                ? "text-primary border-b-2 border-primary"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab.icon}
            {tab.label}
          </button>
        ))}
      </div>

      <div className="flex-1 overflow-hidden">
        {activeTab === "inspector" && <PanelInspector panel={selectedPanel} />}
        {activeTab === "tree" && (
          <ComicTree pages={pages} selectedPanelId={selectedPanelId} onSelectPanel={onSelectPanel} />
        )}
        {activeTab === "characters" && <CharacterLibrary />}
      </div>
    </div>
  );
};
