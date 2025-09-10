'use client';

import AppShell from '@/components/shell/AppShell';
import { DataTable } from '@/components/ui/DataTable';

const columns = ['SKU', 'Nombre', 'Stock', 'Precio'];
const rows = [
  { SKU: 'A-001', Nombre: 'Silla ergonómica', Stock: 12, Precio: '$89.990' },
  { SKU: 'A-002', Nombre: 'Toner HP 12A', Stock: 5, Precio: '$54.990' },
];

export default function InventarioPage() {
  return (
    <AppShell>
      <h1 className="text-xl font-semibold mb-3">Inventario</h1>
      <DataTable columns={columns} rows={rows} />
    </AppShell>
  );
}
