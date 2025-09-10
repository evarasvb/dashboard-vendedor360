"use client";
import Link from "next/link";
import { useApp } from "@/lib/store";

const links = [
  { href: "/", label: "Inicio" },
  { href: "/inventario", label: "Inventario" },
  { href: "/cotizaciones", label: "Cotizaciones" },
  { href: "/ordenes", label: "Órdenes" },
  { href: "/reportes", label: "Reportes" },
  { href: "/settings", label: "Ajustes" },
];

export default function Sidebar() {
  const sidebarOpen = useApp((s) => s.sidebarOpen);
  const setSidebarOpen = useApp((s) => s.setSidebarOpen);

  return (
    <div
      className={`fixed inset-y-0 left-0 z-40 w-64 bg-white border-r transform ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      } transition-transform duration-300 ease-in-out`}
    >
      <div className="p-3 font-semibold border-b">Menú</div>
      <nav className="p-2">
        <ul className="space-y-1">
          {links.map((l) => (
            <li key={l.href}>
              <Link
                className="block px-3 py-2 hover:bg-gray-100 rounded-md"
                href={l.href}
                onClick={() => setSidebarOpen(false)}
              >
                {l.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
}
