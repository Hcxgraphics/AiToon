"use client";

import { Button } from "@/components/ui/button";
import { ArrowLeft, ArrowRight, Sparkles } from "lucide-react";

export const NavigationControls = ({
  currentStep,
  onBack,
  onNext,
  onSkip,
  canProceed,
  onCreateComic,
}) => {
  const isLastStep = currentStep === 3;
  const showSkip = currentStep > 1;

  return (
    <div className="flex items-center justify-between w-full max-w-2xl mx-auto pt-6">
      <div>
        {currentStep > 1 && (
          <Button
            variant="ghost"
            onClick={onBack}
            className="gap-2 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft size={16} />
            Back
          </Button>
        )}
      </div>

      <div className="flex items-center gap-3">
        {showSkip && (
          <Button
            variant="ghost"
            onClick={onSkip}
            className="text-muted-foreground hover:text-foreground text-sm"
          >
            Skip
          </Button>
        )}

        {isLastStep ? (
          <Button
            onClick={onCreateComic}
            className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90 px-6 h-11 text-sm font-semibold glow-accent"
          >
            <Sparkles size={16} />
            Create Comic
          </Button>
        ) : (
          <Button
            onClick={onNext}
            disabled={!canProceed}
            className="gap-2 bg-primary text-primary-foreground hover:bg-primary/90 px-6 h-11 disabled:opacity-40"
          >
            Next
            <ArrowRight size={16} />
          </Button>
        )}
      </div>
    </div>
  );
};
