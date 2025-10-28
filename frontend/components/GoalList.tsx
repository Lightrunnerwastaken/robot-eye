"use client";

import { useQuery } from "@tanstack/react-query";

import { fetchGoals } from "../lib/api";

export function GoalList() {
  const { data, isLoading } = useQuery({ queryKey: ["goals"], queryFn: fetchGoals });

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
      <h2 className="text-xl font-semibold text-primary-light">Aktive Lernziele</h2>
      {isLoading && <p className="mt-4 text-slate-300">Lade Lernziele...</p>}
      <ul className="mt-4 space-y-3">
        {data?.map((goal: any) => (
          <li key={goal.id} className="rounded-lg border border-slate-800 bg-slate-950/50 p-4">
            <p className="text-lg font-semibold text-slate-100">{goal.subject}</p>
            <p className="text-sm text-slate-300">{goal.topic}</p>
            <p className="text-xs text-slate-400">
              Prüfung am {new Date(goal.exam_date).toLocaleDateString("de-DE")}
            </p>
          </li>
        ))}
      </ul>
      {!isLoading && !data?.length && <p className="mt-4 text-slate-300">Noch keine Lernziele erfasst.</p>}
    </section>
  );
}
