"use client";

import dynamic from "next/dynamic";

const InfiniteGallery = dynamic(
  () => import("@/components/ui/3d-gallery-photography"),
  { ssr: false }
);

const images = [
  "/gallery/comic-1.jpg",
  "/gallery/comic-2.jpg",
  "/gallery/comic-3.jpg",
  "/gallery/comic-4.jpg",
  "/gallery/comic-5.jpg",
  "/gallery/comic-6.jpg",
];

export default function GalleryHero() {
  return (
    <section className="relative w-full h-screen overflow-hidden bg-background">
      {/* 3D Gallery */}
      <div className="absolute inset-0 z-0">
        <InfiniteGallery images={images} />
      </div>

      {/* Gradient overlays */}
      <div className="absolute inset-0 z-10 bg-gradient-to-b from-background/80 via-transparent to-background pointer-events-none" />
      <div className="absolute inset-0 z-10 bg-gradient-to-r from-background/40 via-transparent to-background/40 pointer-events-none" />

      {/* Title */}
      <div className="absolute inset-0 z-20 flex flex-col items-center justify-center pointer-events-none">
        <h1 className="text-7xl md:text-9xl font-bold tracking-tighter text-foreground drop-shadow-2xl"
            style={{ textShadow: "0 0 60px hsl(var(--primary) / 0.4)" }}>
          AiToon
        </h1>
        <p className="mt-4 text-lg md:text-xl text-muted-foreground max-w-md text-center">
          AI-Powered Comic Creation Studio
        </p>

        {/* Scroll indicator */}
        <div className="absolute bottom-12 animate-bounce">
          <div className="w-6 h-10 rounded-full border-2 border-muted-foreground/50 flex items-start justify-center p-1.5">
            <div className="w-1.5 h-2.5 rounded-full bg-muted-foreground/70" />
          </div>
        </div>
      </div>
    </section>
  );
}
