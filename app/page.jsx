'use client';

import GalleryHero from "@/components/blocks/gallery-hero";
import HeroSpline from "@/components/blocks/hero-spline";

export default function Home() {
  return (
    <main className="bg-background text-foreground scroll-smooth">
      <GalleryHero />
      <HeroSpline />
    </main>
  );
}
