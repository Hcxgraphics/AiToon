"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Check } from "lucide-react";

const THEMES = [
  { id: "neo", title: "Neo", image: "/themes/neo.jpg", description: "Futuristic neon-drenched visuals with bold digital aesthetics and vibrant glowing accents." },
  { id: "cyberpunk", title: "Cyberpunk", image: "/themes/cyberpunk.jpg", description: "Rain-soaked dystopian streets lit by holographic signs and moody atmospheric lighting." },
  { id: "anime-craft", title: "Anime Craft", image: "/themes/anime-craft.jpg", description: "Colorful cel-shaded anime style with vibrant characters and detailed hand-drawn feel." },
  { id: "noir", title: "Noir", image: "/themes/noir.jpg", description: "High-contrast black and white with dramatic shadows inspired by classic detective comics." },
  { id: "manga", title: "Manga Style", image: "/themes/manga.jpg", description: "Traditional Japanese manga with dynamic ink lines, screentones, and action-packed panels." },
  { id: "manhwa", title: "Korean Manhwa", image: "/themes/manhwa.jpg", description: "Full-color Korean webtoon aesthetic with soft shading and beautiful character designs." },
  { id: "manhua", title: "Chinese Manhua", image: "/themes/manhua.jpg", description: "Traditional ink wash meets modern comic with wuxia-inspired martial arts scenes." },
  { id: "chibi", title: "Chibi Kawaii", image: "/themes/chibi.jpg", description: "Adorable super-deformed characters with big sparkly eyes and pastel color palettes." },
];

export const ThemeCarousel = ({ selectedTheme, onSelectTheme }) => {
  const scrollRef = useRef(null);
  const [hoveredId, setHoveredId] = useState(null);
  const autoScrollRef = useRef(null);
  const isDragging = useRef(false);
  const isHoveringCarousel = useRef(false);
  const startX = useRef(0);
  const scrollLeftPos = useRef(0);

  const startAutoScroll = useCallback(() => {
    if (autoScrollRef.current) cancelAnimationFrame(autoScrollRef.current);
    const scroll = () => {
      const el = scrollRef.current;
      if (!el || isDragging.current || isHoveringCarousel.current) {
        autoScrollRef.current = requestAnimationFrame(scroll);
        return;
      }
      el.scrollLeft += 0.4;
      if (el.scrollLeft >= el.scrollWidth - el.clientWidth) {
        el.scrollLeft = 0;
      }
      autoScrollRef.current = requestAnimationFrame(scroll);
    };
    autoScrollRef.current = requestAnimationFrame(scroll);
  }, []);

  useEffect(() => {
    startAutoScroll();
    return () => {
      if (autoScrollRef.current) cancelAnimationFrame(autoScrollRef.current);
    };
  }, [startAutoScroll]);

  const handleMouseDown = (e) => {
    isDragging.current = true;
    startX.current = e.pageX - scrollRef.current.offsetLeft;
    scrollLeftPos.current = scrollRef.current.scrollLeft;
  };

  const handleMouseMove = (e) => {
    if (!isDragging.current) return;
    e.preventDefault();
    const x = e.pageX - scrollRef.current.offsetLeft;
    const walk = (x - startX.current) * 1.5;
    scrollRef.current.scrollLeft = scrollLeftPos.current - walk;
  };

  const handleMouseUp = () => {
    isDragging.current = false;
  };

  const handleCarouselEnter = () => { isHoveringCarousel.current = true; };
  const handleCarouselLeave = () => {
    isHoveringCarousel.current = false;
    isDragging.current = false;
  };

  return (
    <div className="w-full">
      <div
        ref={scrollRef}
        onMouseDown={handleMouseDown}
        onMouseMove={handleMouseMove}
        onMouseUp={handleMouseUp}
        onMouseEnter={handleCarouselEnter}
        onMouseLeave={handleCarouselLeave}
        className="flex gap-5 overflow-x-auto pb-4 cursor-grab active:cursor-grabbing snap-x snap-mandatory"
        style={{ scrollbarWidth: "none", msOverflowStyle: "none", WebkitOverflowScrolling: "touch" }}
      >
        {[...THEMES, ...THEMES].map((theme, i) => {
          const isSelected = selectedTheme === theme.id;
          const isHovered = hoveredId === `${theme.id}-${i}`;

          return (
            <motion.div
              key={`${theme.id}-${i}`}
              className="flex-shrink-0 snap-center"
              animate={{ scale: isHovered ? 1.05 : 1 }}
              transition={{ type: "spring", stiffness: 300, damping: 20 }}
            >
              <div
                onClick={() => onSelectTheme(theme.id)}
                onMouseEnter={() => setHoveredId(`${theme.id}-${i}`)}
                onMouseLeave={() => setHoveredId(null)}
                className={`relative w-[220px] h-[300px] rounded-2xl overflow-hidden cursor-pointer transition-all duration-300 group ${
                  isSelected
                    ? "ring-2 ring-primary glow-border"
                    : "ring-1 ring-border hover:ring-primary/40"
                }`}
              >
                <img
                  src={theme.image}
                  alt={theme.title}
                  className="w-full h-full object-cover transition-all duration-500"
                  draggable={false}
                />
                <div className={`absolute inset-0 bg-black/0 transition-all duration-300 ${isHovered ? "bg-black/50" : ""}`} />
                <div className="absolute bottom-0 left-0 right-0 p-4 bg-gradient-to-t from-black/80 via-black/40 to-transparent">
                  <h3 className="text-sm font-bold text-white">{theme.title}</h3>
                </div>
                <AnimatePresence>
                  {isHovered && (
                    <motion.div
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: 10 }}
                      transition={{ duration: 0.2 }}
                      className="absolute inset-0 flex items-center justify-center p-5"
                    >
                      <p className="text-xs text-white/90 text-center leading-relaxed">{theme.description}</p>
                    </motion.div>
                  )}
                </AnimatePresence>
                {isSelected && (
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    className="absolute top-3 right-3 w-7 h-7 rounded-full bg-primary flex items-center justify-center"
                  >
                    <Check size={14} className="text-primary-foreground" />
                  </motion.div>
                )}
              </div>
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
