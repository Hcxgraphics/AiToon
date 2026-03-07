"use client";

import { motion } from "framer-motion";
import { Check } from "lucide-react";

const STEPS = [
  { id: 1, label: "Theme" },
  { id: 2, label: "Characters" },
  { id: 3, label: "Story" },
];

export const ProgressStepper = ({ currentStep }) => {
  return (
    <div className="flex items-center justify-center gap-0">
      {STEPS.map((step, i) => {
        const isComplete = currentStep > step.id;
        const isActive = currentStep === step.id;

        return (
          <div key={step.id} className="flex items-center">
            <div className="flex flex-col items-center gap-1.5">
              <motion.div
                initial={false}
                animate={{
                  scale: isActive ? 1.1 : 1,
                  backgroundColor: isComplete
                    ? "hsl(224 100% 71%)"
                    : isActive
                    ? "hsl(222 18% 16%)"
                    : "hsl(222 18% 11%)",
                  borderColor: isActive
                    ? "hsl(224 100% 71%)"
                    : isComplete
                    ? "hsl(224 100% 71%)"
                    : "hsl(222 14% 22%)",
                }}
                transition={{ type: "spring", stiffness: 400, damping: 25 }}
                className="w-9 h-9 rounded-full border-2 flex items-center justify-center text-xs font-bold"
                style={{
                  boxShadow: isActive
                    ? "0 0 20px hsl(224 100% 71% / 0.3)"
                    : "none",
                }}
              >
                {isComplete ? (
                  <Check size={16} className="text-primary-foreground" />
                ) : (
                  <span
                    className={
                      isActive ? "text-primary" : "text-muted-foreground"
                    }
                  >
                    {step.id}
                  </span>
                )}
              </motion.div>
              <span
                className={`text-[11px] font-medium ${
                  isActive
                    ? "text-primary"
                    : isComplete
                    ? "text-foreground"
                    : "text-muted-foreground"
                }`}
              >
                {step.label}
              </span>
            </div>
            {i < STEPS.length - 1 && (
              <div className="w-16 h-[2px] mx-2 mb-5 rounded-full overflow-hidden bg-border">
                <motion.div
                  initial={false}
                  animate={{ scaleX: isComplete ? 1 : 0 }}
                  transition={{ duration: 0.4, ease: "easeInOut" }}
                  className="h-full bg-primary origin-left"
                />
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
};
