"use client";

import { useRouter, useSearchParams } from "next/navigation";
import { ArrowLeft, Save, LayoutDashboard, User } from "lucide-react";
import { Button } from "@/components/ui/button";

export const EditorNavbar = () => {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isFromSetup = searchParams.get("theme") || searchParams.get("storyline");

  return (
    <div className="h-12 border-b border-border bg-card flex items-center justify-between px-4 shrink-0">
      {/* Left */}
      <div className="flex items-center gap-3">
        {isFromSetup && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => router.push("/setup")}
            className="h-8 px-2 gap-1.5 text-muted-foreground hover:text-foreground"
          >
            <ArrowLeft size={14} />
            <span className="text-xs">Back</span>
          </Button>
        )}
        <span className="text-sm font-bold tracking-tight text-foreground">
          Ai<span className="text-primary">Toon</span>
        </span>
      </div>

      {/* Right */}
      <div className="flex items-center gap-1">
        <Button variant="ghost" size="sm" className="h-8 px-3 gap-1.5 text-xs text-muted-foreground hover:text-foreground">
          <Save size={13} />
          Save Draft
        </Button>
        <Button variant="ghost" size="sm" className="h-8 px-3 gap-1.5 text-xs text-muted-foreground hover:text-foreground">
          <LayoutDashboard size={13} />
          Dashboard
        </Button>
        <Button variant="ghost" size="sm" className="h-8 px-3 gap-1.5 text-xs text-muted-foreground hover:text-foreground">
          <User size={13} />
          Profile
        </Button>
      </div>
    </div>
  );
};
