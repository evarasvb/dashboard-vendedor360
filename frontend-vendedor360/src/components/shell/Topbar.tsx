"use client";
import { Menu, Bell } from "lucide-react";
import { useApp } from "@/lib/store";
import { Button } from "@/components/ui/button";

export default function Topbar() {
  const setSidebarOpen = useApp((s) => s.setSidebarOpen);
  return (
    <div className="h-14 border-b flex items-center justify-between px-3">
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(true)}>
          <Menu className="w-5 h-5" />
        </Button>
        <span className="font-semibold">{process.env.NEXT_PUBLIC_BRAND_NAME || "Vendedor 360"}</span>
      </div>
      <Button variant="ghost" size="icon">
        <Bell className="w-5 h-5" />
      </Button>
    </div>
  );
}
