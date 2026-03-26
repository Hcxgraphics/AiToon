"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Search, Plus, Check, X, Sparkles } from "lucide-react";
import { CreateCharacterModal } from "./CreateCharacterModal";

const PREDEFINED_CHARACTERS = [
  { id: "c1", name: "Kai", avatar: "K", style: "Hero", gender: "Male", age: "Young Adult", ethnicity: "Asian", color: "hsl(224 100% 71%)" },
  { id: "c2", name: "Luna", avatar: "L", style: "Mystic", gender: "Female", age: "Young Adult", ethnicity: "Mixed", color: "hsl(280 80% 65%)" },
  { id: "c3", name: "Rex", avatar: "R", style: "Villain", gender: "Male", age: "Adult", ethnicity: "European", color: "hsl(0 72% 55%)" },
  { id: "c4", name: "Aria", avatar: "A", style: "Sidekick", gender: "Female", age: "Teen", ethnicity: "African", color: "hsl(142 60% 45%)" },
  { id: "c5", name: "Zane", avatar: "Z", style: "Anti-Hero", gender: "Male", age: "Adult", ethnicity: "Latino", color: "hsl(32 90% 55%)" },
  { id: "c6", name: "Miko", avatar: "M", style: "Support", gender: "Female", age: "Teen", ethnicity: "Asian", color: "hsl(340 75% 60%)" },
  { id: "c7", name: "Drake", avatar: "D", style: "Warrior", gender: "Male", age: "Adult", ethnicity: "Middle Eastern", color: "hsl(200 70% 50%)" },
  { id: "c8", name: "Nova", avatar: "N", style: "Scientist", gender: "Non-Binary", age: "Young Adult", ethnicity: "Mixed", color: "hsl(170 60% 50%)" },
];

const FILTER_CATEGORIES = {
  gender: ["All", "Male", "Female", "Non-Binary"],
  age: ["All", "Teen", "Young Adult", "Adult"],
  ethnicity: ["All", "Asian", "European", "African", "Latino", "Middle Eastern", "Mixed"],
  style: ["All", "Hero", "Villain", "Sidekick", "Anti-Hero", "Mystic", "Support", "Warrior", "Scientist"],
};

const PillFilter = ({ label, options, value, onChange }) => (
  <div className="flex items-center gap-2">
    <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold shrink-0">{label}</span>
    <div className="flex gap-1 flex-wrap">
      {options.map((opt) => (
        <button
          key={opt}
          onClick={() => onChange(opt)}
          className={`px-2.5 py-1 rounded-full text-[11px] font-medium transition-all duration-200 ${
            value === opt
              ? "bg-primary text-primary-foreground"
              : "bg-secondary text-muted-foreground hover:text-foreground hover:bg-secondary/80"
          }`}
        >
          {opt}
        </button>
      ))}
    </div>
  </div>
);

export const CharacterLibrary = ({ selectedCharacters, onSelectCharacters }) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filters, setFilters] = useState({ gender: "All", age: "All", ethnicity: "All", style: "All" });
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [customCharacters, setCustomCharacters] = useState([]);
  const [activeFilterTab, setActiveFilterTab] = useState("gender");

  const allCharacters = [...PREDEFINED_CHARACTERS, ...customCharacters];

  const filteredCharacters = allCharacters.filter((char) => {
    if (searchQuery && !char.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    if (filters.gender !== "All" && char.gender !== filters.gender) return false;
    if (filters.age !== "All" && char.age !== filters.age) return false;
    if (filters.ethnicity !== "All" && char.ethnicity !== filters.ethnicity) return false;
    if (filters.style !== "All" && char.style !== filters.style) return false;
    return true;
  });

  const toggleCharacter = (id) => {
    onSelectCharacters(
      selectedCharacters.includes(id)
        ? selectedCharacters.filter((c) => c !== id)
        : [...selectedCharacters, id]
    );
  };

  const handleCreateCharacter = (char) => {
    const newChar = {
      ...char,
      id: `custom-${Date.now()}`,
      avatar: char.name[0].toUpperCase(),
      color: `hsl(${Math.floor(Math.random() * 360)} 70% 55%)`,
    };
    setCustomCharacters((prev) => [...prev, newChar]);
    toggleCharacter(newChar.id);
    setShowCreateModal(false);
  };

  const filterTabs = Object.keys(FILTER_CATEGORIES);

  return (
    <div className="w-full space-y-4">
      {/* Search */}
      <div className="relative">
        <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
        <input
          type="text"
          placeholder="Search characters..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full h-10 pl-10 pr-4 rounded-xl bg-secondary border border-border text-sm text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
        />
      </div>

      {/* Filter tabs + pills */}
      <div className="p-3 rounded-xl bg-card/50 border border-border space-y-3">
        <div className="flex gap-1">
          {filterTabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveFilterTab(tab)}
              className={`px-3 py-1.5 rounded-lg text-[11px] font-semibold uppercase tracking-wider transition-all ${
                activeFilterTab === tab
                  ? "bg-primary/15 text-primary"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {tab}
              {filters[tab] !== "All" && (
                <span className="ml-1 w-1.5 h-1.5 rounded-full bg-primary inline-block" />
              )}
            </button>
          ))}
        </div>
        <PillFilter
          label=""
          options={FILTER_CATEGORIES[activeFilterTab]}
          value={filters[activeFilterTab]}
          onChange={(val) => setFilters((f) => ({ ...f, [activeFilterTab]: val }))}
        />
      </div>

      {/* Selected characters */}
      {selectedCharacters.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedCharacters.map((id) => {
            const char = allCharacters.find((c) => c.id === id);
            if (!char) return null;
            return (
              <motion.div
                key={id}
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-primary/15 border border-primary/30 text-xs text-primary"
              >
                <span className="font-medium">{char.name}</span>
                <button onClick={() => toggleCharacter(id)} className="hover:text-foreground transition-colors">
                  <X size={12} />
                </button>
              </motion.div>
            );
          })}
        </div>
      )}

      {/* Character grid — Create New first */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
        {/* Create new character — first item */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          onClick={() => setShowCreateModal(true)}
          className="p-4 rounded-xl cursor-pointer border-2 border-dashed border-border hover:border-primary/40 transition-all flex flex-col items-center justify-center gap-2 min-h-[140px] panel-hover-glow"
        >
          <div className="w-12 h-12 rounded-full bg-secondary flex items-center justify-center text-muted-foreground">
            <Plus size={20} />
          </div>
          <span className="text-xs font-medium text-muted-foreground">Create New</span>
        </motion.div>

        {filteredCharacters.map((char, i) => {
          const isSelected = selectedCharacters.includes(char.id);
          return (
            <motion.div
              key={char.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.03 }}
              onClick={() => toggleCharacter(char.id)}
              className={`relative p-4 rounded-xl cursor-pointer transition-all duration-200 border ${
                isSelected
                  ? "bg-primary/10 border-primary/40 glow-border"
                  : "bg-card border-border hover:border-primary/30 panel-hover-glow"
              }`}
            >
              <div className="flex flex-col items-center gap-2">
                <div
                  className="w-12 h-12 rounded-full flex items-center justify-center text-lg font-bold"
                  style={{ backgroundColor: char.color + "22", color: char.color }}
                >
                  {char.avatar}
                </div>
                <span className="text-sm font-medium text-foreground">{char.name}</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-secondary text-muted-foreground">
                  {char.style}
                </span>
              </div>
              {isSelected && (
                <motion.div
                  initial={{ scale: 0 }}
                  animate={{ scale: 1 }}
                  className="absolute top-2 right-2 w-5 h-5 rounded-full bg-primary flex items-center justify-center"
                >
                  <Check size={10} className="text-primary-foreground" />
                </motion.div>
              )}
            </motion.div>
          );
        })}
      </div>

      <CreateCharacterModal
        isOpen={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onCreate={handleCreateCharacter}
      />
    </div>
  );
};
