"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { FormEvent, useState } from "react";

import { GoalPayload, api } from "../lib/api";

const difficulties: GoalPayload["difficulty"][] = ["easy", "medium", "hard"];

export function GoalForm() {
  const queryClient = useQueryClient();
  const [pending, setPending] = useState(false);

  const mutation = useMutation({
    mutationFn: async (payload: GoalPayload) => {
      const { data } = await api.post("/goals/", payload);
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["goals"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    }
  });

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form = event.currentTarget;
    const payload: GoalPayload = {
      subject: (form.subject as HTMLInputElement).value,
      topic: (form.topic as HTMLInputElement).value,
      exam_date: (form.exam_date as HTMLInputElement).value,
      difficulty: (form.difficulty as HTMLSelectElement).value as GoalPayload["difficulty"],
      notes: (form.notes as HTMLTextAreaElement).value || undefined
    };
    setPending(true);
    mutation.mutate(payload, {
      onSettled: () => {
        setPending(false);
        form.reset();
      }
    });
  };

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg">
      <h2 className="text-xl font-semibold text-primary-light">Lernziel erfassen</h2>
      <form onSubmit={handleSubmit} className="mt-4 grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-2 text-sm text-slate-200">
          Fach
          <input
            name="subject"
            required
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-base"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-200">
          Thema
          <input
            name="topic"
            required
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-base"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-200">
          Prüfungstermin
          <input
            type="date"
            name="exam_date"
            required
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-base"
          />
        </label>
        <label className="flex flex-col gap-2 text-sm text-slate-200">
          Schwierigkeit
          <select
            name="difficulty"
            defaultValue="medium"
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-base"
          >
            {difficulties.map((option) => (
              <option key={option} value={option}>
                {option}
              </option>
            ))}
          </select>
        </label>
        <label className="md:col-span-2 flex flex-col gap-2 text-sm text-slate-200">
          Notizen
          <textarea
            name="notes"
            rows={3}
            className="rounded-md border border-slate-700 bg-slate-800 px-3 py-2 text-base"
          />
        </label>
        <button
          type="submit"
          disabled={pending}
          className="md:col-span-2 inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 font-semibold text-white shadow-md transition hover:bg-primary-light disabled:opacity-50"
        >
          {pending ? "Speichern..." : "Ziel hinzufügen"}
        </button>
      </form>
    </section>
  );
}
