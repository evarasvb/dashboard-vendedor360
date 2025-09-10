'use client';

import AppShell from '@/components/shell/AppShell';
import { DataTable } from '@/components/ui/DataTable';

const columns = ['N°', 'Cliente', 'Estado', 'Monto'];
const rows = [
  { 'N°': 'COT-001', Cliente: 'Acme Corp', Estado: 'Pendiente', Monto: '$1.500.000' },
  { 'N°': 'COT-002', Cliente: 'Beta Ltda', Estado: 'Aceptada', Monto: '$750.000' },
];

export default function CotizacionesPage() {
  return (
    <AppShell>
      <h1 className="text-xl font-semibold mb-3">Cotizaciones</h1>
      <DataTable columns={columns} rows={rows} />
    </AppShell>
  );
}
