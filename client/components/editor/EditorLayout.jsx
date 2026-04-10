'use client';

import { Suspense, useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { LeftPanel } from "./LeftPanel";
import { CenterCanvas } from "./CenterCanvas";
import { ChatPanel } from "./ChatPanel";
import { EditorNavbar } from "./EditorNavbar";

const EditorContent = () => {
  const { id } = useParams();

  const [project, setProject] = useState(null);
  const [selectedPanelId, setSelectedPanelId] = useState(null);
  const [generatedImages, setGeneratedImages] = useState({}); // ✅ NEW

  // 🔥 LOAD GENERATED IMAGES
  useEffect(() => {
    const stored = localStorage.getItem("generatedImages");
    if (stored) {
      const parsed = JSON.parse(stored);

      console.log("🖼️ Raw stored:", parsed);
      
      // 🔥 Flexible normalization - handle numeric or "panel-X" keys
      const normalized = {};
      Object.keys(parsed).forEach((key) => {
        let numKey = parseInt(key);
        if (isNaN(numKey)) {
          numKey = parseInt(key.split("-")[1] || key);
        }
        if (!isNaN(numKey)) {
          normalized[numKey] = parsed[key];
        }
      });

      console.log("🖼️ Normalized images:", normalized);
      setGeneratedImages(normalized);
    }
  }, []);


  // Fetch project
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

  // Auto-select first panel
  useEffect(() => {
    if (project?.panels?.length > 0) {
      setSelectedPanelId(project.panels[0].panel_id);
    }
  }, [project]);

  if (!project) {
    return <div className="p-6">Loading...</div>;
  }

  // Character Map
  const characterMap = Object.fromEntries(
    (project.characters || []).map((c) => [c.char_id, c])
  );

  // Normalize panels + FALLBACK if empty
  let panels = (project.panels || []).map((p) => ({
    id: p.panel_id,
    name: `Panel ${p.panel_id}`,
    scene: p.scene_description || 'Scene',
    characters: p.characters || [],
    dialogues: p.dialogues || [],
    narration: p.narration || '',
    raw: p,
  }));

  // 🔥 FALLBACK: Create panels from generatedImages if project empty
  if (panels.length === 0 && Object.keys(generatedImages).length > 0) {
    console.log('🔥 Using image-based fallback panels');
    const imageKeys = Object.keys(generatedImages).map(k => parseInt(k)).sort((a,b)=>a-b);
    panels = imageKeys.map(id => ({
      id,
      name: `Panel ${id}`,
      scene: 'Generated scene',
      characters: [],
      dialogues: [],
      narration: '',
      raw: {},
    }));
  }

  const pages = [{
    id: "page-1",
    name: "Page 1",
    panels,
  }];


  const allPanels = pages.flatMap((p) => p.panels);

  const selectedPanel =
    allPanels.find((p) => p.id === selectedPanelId) || null;

  return (
    <>
      <EditorNavbar />

      <div className="flex flex-1 overflow-hidden">

        {/* LEFT PANEL */}
        <div className="w-[25%] min-w-[280px] max-w-[360px] border-r border-border flex flex-col">
          <LeftPanel
            pages={pages}
            selectedPanel={selectedPanel}
            selectedPanelId={selectedPanelId}
            onSelectPanel={setSelectedPanelId}
            characterMap={characterMap}
          />
        </div>

        {/* CENTER CANVAS */}
        <div className="flex-1 flex flex-col min-w-0">
          <CenterCanvas
            pages={pages}
            selectedPanelId={selectedPanelId}
            onSelectPanel={setSelectedPanelId}
            generatedImages={generatedImages} // ✅ THIS WAS MISSING
          />
        </div>

        {/* RIGHT PANEL */}
        <div className="w-[25%] min-w-[280px] max-w-[360px] border-l border-border flex flex-col">
          <ChatPanel
            project={project}
            allVersions={allPanels.map((p) => ({
              text: p.scene,
              panelName: p.name,
            }))}
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