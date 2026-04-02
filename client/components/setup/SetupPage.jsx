"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import { ProgressStepper } from "./ProgressStepper";
import { NavigationControls } from "./NavigationControls";
import { ThemeCarousel } from "./ThemeCarousel";
import { CharacterLibrary } from "./CharacterLibrary";
import { StoryForm } from "./StoryForm";

export const SetupPage = () => {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedTheme, setSelectedTheme] = useState(null);
  const [selectedCharacters, setSelectedCharacters] = useState([]);
  const [storyData, setStoryData] = useState({ storyline: "", tagline: "", summary: "" });

  const canProceed = () => {
    if (currentStep === 1) return !!selectedTheme;
    return true;
  };

  const handleNext = () => {
    if (currentStep < 3) setCurrentStep((s) => s + 1);
  };

  const handleBack = () => {
    if (currentStep > 1) setCurrentStep((s) => s - 1);
  };

  const handleSkip = () => {
    if (currentStep < 3) setCurrentStep((s) => s + 1);
  };

  const handleCreateComic = async () => {
  try {
    const res = await fetch("http://localhost:8000/setup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        theme: selectedTheme,
        characters: selectedCharacters,
        storyline: storyData.storyline,
        tagline: storyData.tagline,
        summary: storyData.summary
      })
    });

    if (!res.ok) throw new Error("Failed to create comic");

    const data = await res.json();

    router.push(`/editor/${data.project_id}`);
  } catch (err) {
    console.error(err);
    alert("Something went wrong!");
  }
};

  

  

  const stepContent = {
    1: {
      title: "Choose Your Theme",
      subtitle: "Select a visual style for your comic",
      component: <ThemeCarousel selectedTheme={selectedTheme} onSelectTheme={setSelectedTheme} />,
    },
    2: {
      title: "Choose Characters",
      subtitle: "Select or create characters for your story",
      component: (
        <CharacterLibrary
          selectedCharacters={selectedCharacters}
          onSelectCharacters={setSelectedCharacters}
        />
      ),
    },
    3: {
      title: "Story Basics",
      subtitle: "Give your AI assistant some context",
      component: <StoryForm storyData={storyData} onUpdateStory={setStoryData} />,
    },
  };

  const current = stepContent[currentStep];

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Header */}
      <div className="pt-10 pb-6 text-center">
        <motion.h1
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-3xl md:text-4xl font-bold text-foreground tracking-tight"
          style={{ textShadow: "0 0 40px hsl(224 100% 71% / 0.2)" }}
        >
          Create Your Comic
        </motion.h1>
        <div className="mt-6">
          <ProgressStepper currentStep={currentStep} />
        </div>
      </div>

      {/* Step content */}
      <div className="flex-1 px-6 md:px-12 lg:px-20 pb-4 overflow-y-auto custom-scrollbar">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentStep}
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -30 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="max-w-4xl mx-auto"
          >
            <div className="text-center mb-8">
              <h2 className="text-xl font-semibold text-foreground">{current.title}</h2>
              <p className="text-sm text-muted-foreground mt-1">{current.subtitle}</p>
            </div>
            {current.component}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation */}
      <div className="px-6 md:px-12 lg:px-20 pb-8">
        <NavigationControls
          currentStep={currentStep}
          onBack={handleBack}
          onNext={handleNext}
          onSkip={handleSkip}
          canProceed={canProceed()}
          onCreateComic={handleCreateComic}
        />
      </div>
    </div>
  );
};
