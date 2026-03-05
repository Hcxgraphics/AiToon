import { useState } from "react";
import { ChatEditor } from "./ChatEditor";
import { ComicTree } from "./ComicTree";
import { CharacterLibrary } from "./CharacterLibrary";
import { MessageSquare, FolderTree, Users } from "lucide-react";
import type { PageData } from "./EditorLayout";

type Tab = "chat" | "tree" | "characters";

interface LeftPanelProps {
  pages: PageData[];
  selectedPanelId: string | null;
  onSelectPanel: (id: string) => void;
}

export const LeftPanel = ({ pages, selectedPanelId, onSelectPanel }: LeftPanelProps) => {
  const [activeTab, setActiveTab] = useState<Tab>("chat");

  const tabs: { id: Tab; icon: React.ReactNode; label: string }[] = [
    { id: "chat", icon: <MessageSquare size={16} />, label: "Chat" },
    { id: "tree", icon: <FolderTree size={16} />, label: "Pages" },
    { id: "characters", icon: <Users size={16} />, label: "Cast" },
  ];

  return (
    <div className="flex flex-col h-full bg-card">
      {/* Tab bar */}
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

      {/* Content */}
      <div className="flex-1 overflow-hidden">
        {activeTab === "chat" && <ChatEditor />}
        {activeTab === "tree" && (
          <ComicTree
            pages={pages}
            selectedPanelId={selectedPanelId}
            onSelectPanel={onSelectPanel}
          />
        )}
        {activeTab === "characters" && <CharacterLibrary />}
      </div>
    </div>
  );
};
