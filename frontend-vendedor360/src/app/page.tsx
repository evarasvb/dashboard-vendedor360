'use client';

import AppShell from '@/components/shell/AppShell';
import { KpiCard } from '@/components/ui/KpiCard';
import ChartPanel from '@/components/ui/ChartPanel';

const demo = [
  { x: 'Lun', y: 12 },
  { x: 'Mar', y: 18 },
  { x: 'Mié', y: 10 },
  { x: 'Jue', y: 22 },
  { x: 'Vie', y: 15 },
];

export default function HomePage() {
  return (
    <AppShell>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
        <KpiCard label="Ventas hoy" value="$ 1.250.000" hint="+12% vs ayer" />
        <KpiCard label="Órdenes nuevas" value={7} hint="2 en despacho" />
        <KpiCard label="Cotizaciones activas" value={14} hint="4 vencen hoy" />
        <KpiCard label="Match Compra Ágil" value="23" hint="en revisión" />
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ChartPanel title="Ingresos últimos 7 días" data={demo} />
        <ChartPanel title="Cotizaciones vs Órdenes" data={demo} />
      </div>
    </AppShell>
  );
}
