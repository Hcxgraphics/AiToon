"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";

// Direct dynamic import of the 3D gallery component with ssr disabled
const Gallery3DContent = dynamic(
  () => import("./Gallery3DContent"),
  {
    ssr: false,
    loading: () => (
      <div className="w-full h-full flex items-center justify-center bg-transparent">
        <div className="text-muted-foreground">Loading 3D gallery...</div>
      </div>
    ),
  }
);

export default function InfiniteGallery({ 
  images,
  speed = 1,
  visibleCount = 8,
  fadeSettings = {
    fadeIn: { start: 0.05, end: 0.25 },
    fadeOut: { start: 0.4, end: 0.43 },
  },
  blurSettings = {
    blurIn: { start: 0.0, end: 0.1 },
    blurOut: { start: 0.4, end: 0.43 },
    maxBlur: 8.0,
  },
}) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  if (!mounted) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-transparent">
        <div className="text-muted-foreground">Loading gallery...</div>
      </div>
    );
  }

  return (
    <div className="w-full h-full">
      <Gallery3DContent 
        images={images}
        speed={speed}
        visibleCount={visibleCount}
        fadeSettings={fadeSettings}
        blurSettings={blurSettings}
      />
    </div>
  );
}
