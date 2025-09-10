import AppShell from "@/components/shell/AppShell";
import { DataTable } from "@/components/ui/DataTable";

const columns = ["N°", "Cliente", "Estado", "Total"];
const rows = [
  { "N°": "ORD-001", Cliente: "Cliente A", Estado: "En proceso", Total: "$120.000" },
  { "N°": "ORD-002", Cliente: "Cliente B", Estado: "Despachado", Total: "$75.000" },
];

export default function OrdenesPage() {
  return (
    <AppShell>
      <h1 className="text-xl font-semibold mb-3">Órdenes</h1>
      <DataTable columns={columns} rows={rows} />
    </AppShell>
  );
}
