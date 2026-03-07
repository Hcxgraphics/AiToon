"use client";

import { ArrowRight, Sparkles, BookOpen, Palette } from "lucide-react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";

export default function HeroSpline() {
  const router = useRouter();

  return (
    <section className="relative w-full min-h-screen flex items-center justify-center bg-background overflow-hidden" data-section="hero-spline">
      {/* Animated background effects */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 rounded-full bg-primary/10 blur-[120px] animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 rounded-full bg-accent/10 blur-[100px] animate-pulse" style={{ animationDelay: "1s" }} />
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] rounded-full bg-primary/5 blur-[150px]" />
      </div>

      {/* Grid pattern */}
      <div className="absolute inset-0 z-0 opacity-[0.03]"
           style={{ backgroundImage: "linear-gradient(hsl(var(--foreground)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--foreground)) 1px, transparent 1px)", backgroundSize: "60px 60px" }} />

      {/* Content */}
      <div className="relative z-10 flex flex-col items-center text-center px-6 max-w-4xl mx-auto">
        {/* Badge */}
        <div className="flex items-center gap-2 px-4 py-2 rounded-full border border-border/50 bg-card/50 backdrop-blur-sm mb-8">
          <Sparkles className="w-4 h-4 text-primary" />
          <span className="text-sm text-muted-foreground">Powered by AI</span>
        </div>

        <h2 className="text-5xl md:text-7xl font-bold tracking-tight text-foreground leading-[1.1]">
          Create Comics
          <br />
          <span className="text-primary">With AI</span>
        </h2>

        <p className="mt-6 text-lg md:text-xl text-muted-foreground max-w-2xl leading-relaxed">
          Turn your ideas into stunning Manga, Manhua, and Anime style comics instantly.
          Write, design, and publish — all in one studio.
        </p>

        {/* CTA */}
        <div className="mt-10 flex flex-col sm:flex-row gap-4">
          <Button
            size="lg"
            className="text-base px-8 py-6 rounded-xl gap-2"
            onClick={() => router.push("/setup")}
          >
            Get Started
            <ArrowRight className="w-5 h-5" />
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="text-base px-8 py-6 rounded-xl gap-2"
          >
            <BookOpen className="w-5 h-5" />
            View Gallery
          </Button>
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
              <span className="text-sm text-muted-foreground">{label}</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
