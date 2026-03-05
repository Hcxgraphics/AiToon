'use client';

import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import "./globals.css";

export default function RootLayout({ children }) {
  return (
    <html lang="en" className="dark">
      <head>
        <title>AiToon</title>
        <meta name="description" content="A professional AI-powered comic creation studio. Chat with AI, design panels, write dialogue, and build your story." />
        <meta property="og:title" content="AI Comic Studio" />
        <meta property="og:description" content="Create comics with AI assistance" />
        <meta property="og:type" content="website" />
        <link rel="icon" href="/favicon.ico" />
      </head>
      <body>
        <TooltipProvider>
          <Toaster />
          <Sonner />
          {children}
        </TooltipProvider>
      </body>
    </html>
  );
}
