"use client";
import Topbar from "./Topbar";
import Sidebar from "./Sidebar";
import React from "react";

export default function AppShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Topbar />
      <Sidebar />
      <div className="p-4 max-w-7xl mx-auto">{children}</div>
    </div>
  );
}
