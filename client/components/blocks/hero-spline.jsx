"use client";

import { ArrowRight, Sparkles, BookOpen, Palette } from "lucide-react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import Particles from "@/components/ui/Particles";

export default function HeroSpline() {
  const router = useRouter();

  return (
    <section className="relative min-h-screen overflow-hidden flex items-center justify-center">
      <div
        className="absolute inset-0 z-0 bg-cover bg-center"
        style={{ backgroundImage: "url('/gallery/hero_spline_image.jpg')" }}
      />
      <div className="absolute inset-0 z-10 bg-black/30" />
      {/* <div className="absolute inset-0 z-20"> */}
      <div className="absolute inset-0 z-20 pointer-events-none">
        <Particles
          particleCount={300}
          particleSpread={10}
          speed={0.1}
          moveParticlesOnHover
          alphaParticles
          className="absolute inset-0"
        />
      </div>

      {/* Content */}
      <div className="relative z-30 flex flex-col items-center text-center px-6 max-w-4xl mx-auto">

      {/* Badge */}
      <div className="flex items-center gap-2 px-3 py-2 rounded-full border border-border/20 bg-card/10 backdrop-blur-sm mb-8">
        <Sparkles className="w-4 h-4 text-primary" />
        <span className="text-sm text-gray-400">Powered by AI</span>
      </div>

      {/* Glass Panel ONLY for main hero text */}
      <div className="px-6 py-8 max-w-xl rounded-2xl bg-gradient-to-b from-black/10 via-blue-975/20 to-black/20 backdrop-blur-md border border-white/10 shadow-2xl">

        <h2 className="text-5xl md:text-7xl font-bold tracking-tight text-white leading-[1.1] drop-shadow-[0_4px_20px_rgba(0,0,0,0.8)]">
          Create Comics
          <br />
          <span className="text-primary">With AI</span>
        </h2>

        <p className="mt-6 text-lg md:text-xl text-gray-300 max-w-2xl leading-relaxed">
          Turn your ideas into stunning Manga, Manhua, and Anime style comics instantly.
          Write, design, and publish ... all in one studio
        </p>

        {/* CTA */}
        <div className="mt-10 flex flex-col sm:flex-row gap-4 justify-center">
          <Button
            variant="outline"
            size="lg"
            className="text-base px-8 py-6 rounded-xl gap-2"
          >
            <BookOpen className="w-5 h-5" />
            View Gallery
          </Button>
          
          <Button
            size="lg"
            className="text-base px-8 py-6 rounded-xl gap-2"
            onClick={() => router.push("/setup")}
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </Button>

        </div>

      </div>

      {/* Feature pills */}
      <div className="mt-16 flex flex-wrap justify-center gap-3">
        {[
          { icon: Sparkles, label: "AI Generation" },
          { icon: Palette, label: "Manga Styles" },
          { icon: BookOpen, label: "Story Builder" },
        ].map(({ icon: Icon, label }) => (
          <div key={label} className="flex items-center gap-2 px-4 py-2 rounded-lg bg-card/30 border border-border/30 backdrop-blur-sm">
            <Icon className="w-4 h-4 text-primary" />
            <span className="text-sm text-gray-400">{label}</span>
          </div>
        ))}
      </div>

    </div>
      </section>
  );
}