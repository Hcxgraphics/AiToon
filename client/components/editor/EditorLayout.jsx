'use client';

import { Suspense, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { LeftPanel } from "./LeftPanel";
import { CenterCanvas } from "./CenterCanvas";
import { ChatPanel } from "./ChatPanel";
import { EditorNavbar } from "./EditorNavbar";

const EditorContent = () => {
  const { id } = useParams(); // 🔥 get project_id from URL
  const [project, setProject] = useState(null);
  const [selectedPanelId, setSelectedPanelId] = useState(null);

  // 🔥 Fetch project from backend
  useEffect(() => {
    const fetchProject = async () => {
      try {
        const res = await fetch(`http://localhost:8000/project/${id}`);
        const data = await res.json();

        setProject(data);
      } catch (err) {
        console.error(err);
      }
    };

    if (id) fetchProject();
  }, [id]);

  // 🔥 Loading state
  if (!project) {
    return <div className="p-6">Loading...</div>;
  }

  // 🔥 Convert backend panels → pages (temporary structure)
  const pages = [
    {
      id: "page-1",
      name: "Page 1",
      panels: project.panels || []
    }
  ];

  const allPanels = pages.flatMap((p) => p.panels);
  const selectedPanel =
    allPanels.find((p) => p.id === selectedPanelId) || null;

  return (
    <>
      <EditorNavbar />
      <div className="flex flex-1 overflow-hidden">
        
        {/* Left Panel */}
        <div className="w-[25%] min-w-[280px] max-w-[360px] border-r border-border flex flex-col">
          <LeftPanel
            pages={pages}
            selectedPanel={selectedPanel}
            selectedPanelId={selectedPanelId}
            onSelectPanel={setSelectedPanelId}
          />
        </div>

        {/* Center Canvas */}
        <div className="flex-1 flex flex-col min-w-0">
          <CenterCanvas
            pages={pages}
            selectedPanelId={selectedPanelId}
            onSelectPanel={setSelectedPanelId}
          />
        </div>

        {/* Right Panel */}
        <div className="w-[25%] min-w-[280px] max-w-[360px] border-l border-border flex flex-col">
          <ChatPanel
            allVersions={allPanels.flatMap((p) =>
              (p.versions || []).map((v) => ({
                ...v,
                panelName: p.name
              }))
            )}
          />
        </div>
      </div>
    </>
  );
};

export const EditorLayout = () => {
  return (
    <div className="flex flex-col h-screen w-screen overflow-hidden bg-background">
      <Suspense fallback={null}>
        <EditorContent />
      </Suspense>
    </div>
  );
};