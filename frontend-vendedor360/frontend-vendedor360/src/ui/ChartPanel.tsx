import { Card } from "./card";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

interface ChartPanelProps {
  title: string;
  data: { x: string; y: number }[];
}

export default function ChartPanel({ title, data }: ChartPanelProps) {
  return (
    <Card>
      <div className="p-4">
        <div className="text-sm text-muted-foreground mb-2">{title}</div>
        <div className="h-60">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={data}>
              <XAxis dataKey="x" />
              <YAxis />
              <Tooltip />
              <Line type="monotone" dataKey="y" strokeWidth={2} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </Card>
  );
}
