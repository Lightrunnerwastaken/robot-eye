"use client";

import { useQuery } from "@tanstack/react-query";
import { format } from "date-fns";
import { de } from "date-fns/locale";

import { fetchDashboard } from "../lib/api";

export function Dashboard() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard"],
    queryFn: fetchDashboard,
    refetchInterval: 60_000
  });

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
      <h2 className="text-xl font-semibold text-primary-light">Dashboard</h2>
      {isLoading && <p className="mt-4 text-slate-300">Lade heutige Aufgaben...</p>}
      {error && <p className="mt-4 text-red-400">{(error as Error).message}</p>}
      {data && (
        <div className="mt-6 grid gap-6 md:grid-cols-3">
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="text-sm text-slate-400">Aktive Lernziele</h3>
            <p className="mt-2 text-3xl font-bold">{data.goals}</p>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="text-sm text-slate-400">Fällige Wiederholungen</h3>
            <p className="mt-2 text-3xl font-bold">{data.due_reviews}</p>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950/70 p-4">
            <h3 className="text-sm text-slate-400">Fortschritt heute</h3>
            <p className="mt-2 text-3xl font-bold">{data.completion_rate}%</p>
          </div>
        </div>
      )}
      {data?.today_blocks?.length ? (
        <div className="mt-8 space-y-4">
          {data.today_blocks.map((block: any) => (
            <article key={`${block.goal_id}-${block.date}`} className="rounded-lg border border-slate-800 bg-slate-950/50 p-4">
              <header className="flex items-center justify-between">
                <h3 className="text-lg font-semibold text-accent">
                  {format(new Date(block.date), "EEEE, dd.MM.", { locale: de })}
                </h3>
                <span className="text-xs uppercase tracking-wide text-slate-400">Goal #{block.goal_id}</span>
              </header>
              <ul className="mt-3 space-y-2">
                {block.tasks.map((task: any) => (
                  <li key={task.id} className="rounded-md border border-slate-800/70 bg-slate-900/70 px-4 py-3">
                    <p className="font-medium text-slate-100">{task.description.title}</p>
                    <p className="text-xs text-slate-400">Bloom: {task.description.bloom}</p>
                    <p className="mt-1 text-sm text-slate-300">{task.description.details}</p>
                  </li>
                ))}
              </ul>
            </article>
          ))}
        </div>
      ) : (
        <p className="mt-8 text-slate-300">Noch keine Aufgaben für heute. Lege ein Lernziel an!</p>
      )}
    </section>
  );
}
