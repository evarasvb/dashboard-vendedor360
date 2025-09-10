'use client';
import AppShell from '@/components/shell/AppShell';
import ChartPanel from '@/components/ui/ChartPanel';

const ingresos = [
  { x: 'Ene', y: 1250000 },
  { x: 'Feb', y: 1520000 },
  { x: 'Mar', y: 980000 },
  { x: 'Abr', y: 1870000 },
];

const ordenes = [
  { x: 'Ene', y: 45 },
  { x: 'Feb', y: 52 },
  { x: 'Mar', y: 38 },
  { x: 'Abr', y: 60 },
];

export default function ReportesPage() {
  return (
    <AppShell>
      <h1 className="text-xl font-semibold mb-3">Reportes</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <ChartPanel title="Ingresos mensuales" data={ingresos} />
        <ChartPanel title="Órdenes mensuales" data={ordenes} />
      </div>
    </AppShell>
  );
}
