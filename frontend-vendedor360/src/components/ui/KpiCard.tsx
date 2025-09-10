import { Card, CardContent } from "./card";

interface KpiCardProps {
  label: string;
  value: string | number;
  hint?: string;
}

export default function KpiCard({ label, value, hint }: KpiCardProps) {
  return (
    <Card className="rounded-2xl">
      <CardContent className="p-4">
        <div className="text-sm text-muted-foreground">{label}</div>
        <div className="text-2xl font-semibold">{value}</div>
        {hint && <div className="text-xs text-muted-foreground mt-1">{hint}</div>}
      </CardContent>
    </Card>
  );
}
