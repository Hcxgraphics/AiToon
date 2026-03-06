'use client';

import dynamic from "next/dynamic";

const GalleryHero = dynamic(
  () => import("@/components/blocks/gallery-hero"),
  { ssr: false }
);

const HeroSpline = dynamic(
  () => import("@/components/blocks/hero-spline"),
  { ssr: false }
);

export default function Home() {
  return (
    <main className="bg-background text-foreground scroll-smooth">
      <GalleryHero />
      <HeroSpline />
    </main>
  );
}
