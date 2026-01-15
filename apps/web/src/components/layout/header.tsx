"use client";

import { Bell, Search, User, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

interface HeaderProps {
  title: string;
  description?: string;
}

export function Header({ title, description }: HeaderProps) {
  return (
    <header className="sticky top-0 z-40 flex h-28 items-center justify-between border-b border-slate-200/30 bg-white/80 backdrop-blur-xl px-12">
      <div className="animate-fade-in">
        <h1 className="text-2xl font-black tracking-tight text-slate-900">{title}</h1>
        {description && (
          <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.25em] mt-1">{description}</p>
        )}
      </div>

      <div className="flex items-center gap-8">
        <div className="hidden lg:flex items-center relative group">
          <Search className="absolute left-4 h-4 w-4 text-slate-400 group-focus-within:text-blue-600 transition-colors" />
          <input 
            type="text" 
            placeholder="Buscar informações..." 
            className="h-12 w-80 rounded-2xl bg-slate-100/50 border-transparent pl-12 text-xs font-bold focus:bg-white focus:ring-1 focus:ring-blue-100 focus:border-blue-200 transition-all placeholder:text-slate-400"
          />
        </div>

        <div className="flex items-center gap-3">
          <Button variant="ghost" size="icon" className="h-12 w-12 rounded-2xl relative hover:bg-slate-100 transition-all group">
            <Bell className="h-5 w-5 text-slate-500 group-hover:text-slate-900" />
            <span className="absolute top-4 right-4 h-2 w-2 rounded-full bg-blue-600 ring-4 ring-white" />
          </Button>
          
          <div className="h-8 w-px bg-slate-200/50 mx-2" />
          
          <Button className="h-12 px-6 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white gap-3 transition-all shadow-lg shadow-slate-100">
            <div className="h-6 w-6 rounded-lg bg-blue-600 flex items-center justify-center">
              <Zap className="h-3 w-3 text-white fill-white" />
            </div>
            <span className="text-[11px] font-black uppercase tracking-widest">Live View</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
