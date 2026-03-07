"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";

export const CreateCharacterModal = ({ isOpen, onClose, onCreate }) => {
  const [form, setForm] = useState({
    name: "",
    style: "Hero",
    gender: "Male",
    age: "Young Adult",
    ethnicity: "Mixed",
  });

  const handleSubmit = () => {
    if (!form.name.trim()) return;
    onCreate(form);
    setForm({ name: "", style: "Hero", gender: "Male", age: "Young Adult", ethnicity: "Mixed" });
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            onClick={(e) => e.stopPropagation()}
            className="w-full max-w-md p-6 rounded-2xl bg-card border border-border shadow-2xl"
          >
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-bold text-foreground">Create Character</h3>
              <button onClick={onClose} className="p-1.5 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground transition-colors">
                <X size={18} />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-1.5 block">Name</label>
                <input
                  type="text"
                  value={form.name}
                  onChange={(e) => setForm((f) => ({ ...f, name: e.target.value }))}
                  placeholder="Enter character name..."
                  className="w-full h-11 px-4 rounded-xl bg-secondary border border-border text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                />
              </div>

              {[
                { key: "style", options: ["Hero", "Villain", "Sidekick", "Anti-Hero", "Mystic", "Support", "Warrior", "Scientist"] },
                { key: "gender", options: ["Male", "Female", "Non-Binary"] },
                { key: "age", options: ["Teen", "Young Adult", "Adult"] },
                { key: "ethnicity", options: ["Asian", "European", "African", "Latino", "Middle Eastern", "Mixed"] },
              ].map(({ key, options }) => (
                <div key={key}>
                  <label className="text-xs uppercase tracking-wider text-muted-foreground font-semibold mb-1.5 block">{key}</label>
                  <select
                    value={form[key]}
                    onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
                    className="w-full h-11 px-4 rounded-xl bg-secondary border border-border text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/50"
                  >
                    {options.map((opt) => (
                      <option key={opt} value={opt}>{opt}</option>
                    ))}
                  </select>
                </div>
              ))}
            </div>

            <div className="flex justify-end gap-3 mt-6">
              <Button variant="ghost" onClick={onClose}>Cancel</Button>
              <Button onClick={handleSubmit} disabled={!form.name.trim()} className="bg-primary text-primary-foreground hover:bg-primary/90">
                Create
              </Button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
