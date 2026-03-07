"use client";

import { useRef } from "react";
import InfiniteGallery from "@/components/ui/InfiniteGallery";

const images = [
  { src: "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?w=800&auto=format&fit=crop", alt: "Comic Art 1" },
  { src: "https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?w=800&auto=format&fit=crop", alt: "Comic Art 2" },
  { src: "https://images.unsplash.com/photo-1601814933824-fd0b574dd592?w=800&auto=format&fit=crop", alt: "Comic Art 3" },
  { src: "https://images.unsplash.com/photo-1635241161466-541f065683ba?w=800&auto=format&fit=crop", alt: "Comic Art 4" },
  { src: "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=800&auto=format&fit=crop", alt: "Comic Art 5" },
  { src: "https://images.unsplash.com/photo-1579783902614-a3fb3927b6a5?w=800&auto=format&fit=crop", alt: "Comic Art 6" },
  { src: "https://images.unsplash.com/photo-1618519764620-7403abdbdfe9?w=800&auto=format&fit=crop", alt: "Comic Art 7" },
  { src: "https://images.unsplash.com/photo-1569003339405-ea396a5a8a90?w=800&auto=format&fit=crop", alt: "Comic Art 8" },
];

export default function GalleryHero() {
  const nextSectionRef = useRef(null);

  const handleScrollClick = () => {
    const nextSection = document.querySelector('[data-section="hero-spline"]');
    if (nextSection) {
      nextSection.scrollIntoView({ behavior: "smooth" });
    } else {
      window.scrollBy({ top: window.innerHeight, behavior: "smooth" });
    }
  };

  return (
    <section className="relative w-full h-screen overflow-hidden bg-background">
      {/* 3D Gallery with Scroll Animation */}
      <div className="absolute inset-0 z-0">
        <InfiniteGallery
          images={images}
          speed={1.2}
          visibleCount={12}
          fadeSettings={{
            fadeIn: { start: 0.05, end: 0.25 },
            fadeOut: { start: 0.4, end: 0.43 },
          }}
          blurSettings={{
            blurIn: { start: 0.0, end: 0.1 },
            blurOut: { start: 0.4, end: 0.43 },
            maxBlur: 8.0,
          }}
        />
      </div>

      {/* Gradient overlays */}
      <div className="absolute inset-0 z-10 bg-gradient-to-b from-background/80 via-transparent to-background pointer-events-none" />
      <div className="absolute inset-0 z-10 bg-gradient-to-r from-background/40 via-transparent to-background/40 pointer-events-none" />

      {/* Title */}
      <div className="absolute inset-0 z-20 flex flex-col items-center justify-center pointer-events-none text-white">
        <h1 className="text-7xl md:text-9xl font-bold tracking-tighter drop-shadow-2xl">
          AiToon
        </h1>
        <p className="mt-4 text-lg md:text-xl max-w-md text-center">
          AI-Powered Comic Creation Studio
        </p>
      </div>

     

      {/* Mouse Scroll Button */}
      <div className="absolute mb-10 bottom-0 left-0 right-0 z-20 flex justify-center pointer-events-auto">
        <button
          onClick={handleScrollClick}
          className="mouse-btn"
          aria-label="Scroll to next section"
        >
          <div className="mouse-scroll" />
        </button>

      {/* <div className="absolute bottom-20 left-0 right-0 z-20 text-center font-mono uppercase text-[11px] font-semibold text-foreground/70 pointer-events-none">
        <p>Scroll</p>
      </div> */}
      </div>
    </section>
  );
}
