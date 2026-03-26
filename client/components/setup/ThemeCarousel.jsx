"use client";

import { useState, useRef, useEffect, useMemo } from "react";
import { motion, AnimatePresence, useAnimationControls } from "framer-motion";
import { Check, ChevronLeft, ChevronRight } from "lucide-react";

const THEMES = [
  { id: "neo", title: "Neo", image: "/themes/neo.jpg", description: "Futuristic neon-drenched visuals with bold digital aesthetics." },
  { id: "cyberpunk", title: "Cyberpunk", image: "/themes/cyberpunk.jpg", description: "Rain-soaked dystopian streets lit by holographic signs." },
  { id: "anime-craft", title: "Anime Craft", image: "/themes/anime-craft.jpg", description: "Colorful cel-shaded anime style with vibrant characters." },
  { id: "noir", title: "Noir", image: "/themes/noir.jpg", description: "High-contrast black and white with dramatic shadows." },
  { id: "manga", title: "Manga Style", image: "/themes/manga.jpg", description: "Traditional Japanese manga with dynamic ink lines." },
  { id: "manhwa", title: "Korean Manhwa", image: "/themes/manhwa.jpg", description: "Full-color Korean webtoon aesthetic with soft shading." },
  { id: "manhua", title: "Chinese Manhua", image: "/themes/manhua.jpg", description: "Traditional ink wash meets modern comic." },
  { id: "chibi", title: "Chibi Kawaii", image: "/themes/chibi.jpg", description: "Adorable super-deformed characters with big sparkly eyes." },
];

export const ThemeCarousel = ({ selectedTheme, onSelectTheme }) => {
  const controls = useAnimationControls();
  const [hoveredId, setHoveredId] = useState(null);
  
  // Configuration
  const ITEM_WIDTH = 220;
  const GAP = 20;
  const SINGLE_SET_WIDTH = (ITEM_WIDTH + GAP) * THEMES.length;
  const SPEED = 50; // Pixels per second

  // We use a triple-cloned list for seamless wrapping
  const displayThemes = useMemo(() => [...THEMES, ...THEMES, ...THEMES], []);
  
  // Track the current X position to resume from the exact spot
  const xPos = useRef(0);
  const lastTimestamp = useRef(0);
  const isRequesting = useRef(true);

  const startAnimation = (currentX) => {
    isRequesting.current = true;
    // Calculate remaining distance to complete one full cycle
    const distanceLeft = SINGLE_SET_WIDTH + currentX; 
    const duration = Math.abs(distanceLeft) / SPEED;

    controls.start({
      x: [currentX, -SINGLE_SET_WIDTH],
      transition: {
        duration: duration,
        ease: "linear",
        repeat: Infinity,
        repeatType: "loop",
        repeatDelay: 0,
      },
    });
  };

  useEffect(() => {
    startAnimation(0);
    return () => controls.stop();
  }, [controls]);

  // Handle Manual Navigation
  const handleNav = (direction) => {
    controls.stop();
    const moveAmount = (ITEM_WIDTH + GAP) * direction;
    let newX = xPos.current + moveAmount;
    
    // Boundary check for infinite feel
    if (newX > 0) newX = -SINGLE_SET_WIDTH;
    if (newX < -SINGLE_SET_WIDTH) newX = 0;
    
    xPos.current = newX;
    controls.set({ x: newX });
    // Resume after a short delay if not hovering
    if (!hoveredId) startAnimation(newX);
  };

  return (
    <div className="group relative w-full overflow-hidden py-12 bg-background">
      {/* Navigation Buttons - Visible on group hover */}
      <div className="absolute inset-y-0 left-4 z-20 flex items-center opacity-0 group-hover:opacity-100 transition-opacity">
        <button 
          onClick={() => handleNav(1)}
          className="p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/20 hover:bg-white/20 text-white"
        >
          <ChevronLeft size={24} />
        </button>
      </div>
      <div className="absolute inset-y-0 right-4 z-20 flex items-center opacity-0 group-hover:opacity-100 transition-opacity">
        <button 
          onClick={() => handleNav(-1)}
          className="p-3 rounded-full bg-white/10 backdrop-blur-md border border-white/20 hover:bg-white/20 text-white"
        >
          <ChevronRight size={24} />
        </button>
      </div>

      {/* Edge Fades */}
      <div className="absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-background to-transparent z-10 pointer-events-none" />
      <div className="absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-background to-transparent z-10 pointer-events-none" />

      <motion.div
        className="flex gap-5"
        animate={controls}
        onUpdate={(latest) => {
            xPos.current = latest.x;
        }}
        style={{ width: "max-content" }}
      >
        {displayThemes.map((theme, i) => {
          const uniqueKey = `${theme.id}-${i}`;
          const isSelected = selectedTheme === theme.id;
          const isHovered = hoveredId === uniqueKey;

          return (
            <div key={uniqueKey} className="flex-shrink-0">
              <motion.div
                whileHover={{ y: -10 }}
                onMouseEnter={() => {
                  setHoveredId(uniqueKey);
                  controls.stop(); // Stop exactly where we are
                }}
                onMouseLeave={() => {
                  setHoveredId(null);
                  startAnimation(xPos.current); // Resume from exact current X
                }}
                onClick={() => onSelectTheme(theme.id)}
                className={`relative w-[220px] h-[300px] rounded-2xl overflow-hidden cursor-pointer transition-shadow duration-300 ${
                  isSelected ? "ring-4 ring-primary ring-offset-4 ring-offset-background" : "ring-1 ring-border"
                }`}
              >
                <img
                  src={theme.image}
                  alt={theme.title}
                  className="w-full h-full object-cover pointer-events-none"
                />

                <div className={`absolute inset-0 bg-black/70 transition-opacity duration-300 flex flex-col justify-center px-6 text-center ${isHovered ? "opacity-100" : "opacity-0"}`}>
                  <p className="text-xs text-white/90 leading-relaxed italic">
                    "{theme.description}"
                  </p>
                </div>

                <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/90 to-transparent">
                  <h3 className="text-sm font-bold text-white uppercase tracking-tighter">{theme.title}</h3>
                </div>

                {isSelected && (
                  <div className="absolute top-4 right-4 w-8 h-8 rounded-full bg-primary flex items-center justify-center shadow-lg">
                    <Check size={18} className="text-primary-foreground stroke-[3px]" />
                  </div>
                )}
              </motion.div>
            </div>
          );
        })}
      </motion.div>
    </div>
  );
};