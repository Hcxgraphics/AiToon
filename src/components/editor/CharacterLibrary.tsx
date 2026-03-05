import { Plus, Smile, Move, Shirt, MessageCircle } from "lucide-react";
import { motion } from "framer-motion";

const CHARACTERS = [
  { id: "hero", name: "Hero", expression: "Determined", color: "hsl(224 100% 71%)" },
  { id: "villain", name: "Villain", expression: "Menacing", color: "hsl(0 72% 55%)" },
  { id: "sidekick", name: "Sidekick", expression: "Cheerful", color: "hsl(142 60% 45%)" },
];

const ACTIONS = [
  { icon: <Plus size={12} />, label: "Add to scene" },
  { icon: <Smile size={12} />, label: "Expression" },
  { icon: <Move size={12} />, label: "Pose" },
  { icon: <Shirt size={12} />, label: "Outfit" },
  { icon: <MessageCircle size={12} />, label: "Dialogue" },
];

export const CharacterLibrary = () => {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center justify-between px-3 py-2 border-b border-border">
        <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">Characters</span>
        <button className="p-1 rounded-md text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors">
          <Plus size={14} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto custom-scrollbar p-3 space-y-2">
        {CHARACTERS.map((char, i) => (
          <motion.div
            key={char.id}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.05 }}
            className="panel-surface p-3 panel-hover-glow cursor-pointer"
          >
            <div className="flex items-center gap-3 mb-2">
              <div
                className="w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold"
                style={{ backgroundColor: char.color + "22", color: char.color }}
              >
                {char.name[0]}
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-sm font-medium text-foreground">{char.name}</div>
                <div className="text-[10px] text-muted-foreground flex items-center gap-1">
                  <Smile size={10} /> {char.expression}
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-1">
              {ACTIONS.map((action) => (
                <button
                  key={action.label}
                  className="flex items-center gap-1 text-[10px] px-2 py-1 rounded-md bg-secondary text-muted-foreground hover:text-foreground hover:bg-surface-hover transition-colors"
                >
                  {action.icon}
                  {action.label}
                </button>
              ))}
            </div>
          </motion.div>
        ))}
      </div>
    </div>
  );
};
