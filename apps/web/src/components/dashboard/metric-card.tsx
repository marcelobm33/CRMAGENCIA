"use client";

import { LucideIcon } from "lucide-react";
import { Card, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

interface MetricCardProps {
  label: string;
  value: string;
  icon: LucideIcon;
  variacao?: number;
  color?: 'blue' | 'emerald' | 'indigo' | 'slate' | 'amber';
}

export function MetricCard({ label, value, icon: Icon, variacao, color = 'blue' }: MetricCardProps) {
  const colorStyles = {
    blue: "text-blue-600 bg-blue-50",
    emerald: "text-emerald-600 bg-emerald-50",
    indigo: "text-indigo-600 bg-indigo-50",
    slate: "text-slate-600 bg-slate-50",
    amber: "text-amber-600 bg-amber-50",
  };

  return (
    <Card className="border-none shadow-premium bg-white hover:translate-y-[-4px] transition-all duration-300 group overflow-hidden">
      <CardContent className="p-8">
        <div className="flex items-start justify-between">
          <div className={cn(
            "h-12 w-12 rounded-2xl flex items-center justify-center transition-all duration-300",
            colorStyles[color]
          )}>
            <Icon className="h-6 w-6" />
          </div>
          {variacao !== undefined && (
            <span className={cn(
              "text-[10px] font-black px-2 py-1 rounded-lg uppercase tracking-widest",
              variacao >= 0 ? "text-emerald-600 bg-emerald-50" : "text-rose-600 bg-rose-50"
            )}>
              {variacao >= 0 ? "+" : ""}{variacao}%
            </span>
          )}
        </div>
        
        <div className="mt-6">
          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-[0.2em] mb-1">
            {label}
          </p>
          <h3 className="text-2xl font-black text-slate-900 tracking-tight leading-none">
            {value}
          </h3>
        </div>
      </CardContent>
      <div className={cn(
        "h-1 w-full opacity-0 group-hover:opacity-100 transition-opacity absolute bottom-0",
        color === 'blue' ? 'bg-blue-600' : 
        color === 'emerald' ? 'bg-emerald-600' :
        color === 'indigo' ? 'bg-indigo-600' :
        'bg-slate-900'
      )} />
    </Card>
  );
}
