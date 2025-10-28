"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { api } from "../lib/api";

const easeLabels: Record<number, string> = {
  1: "Zu schwer",
  2: "Schwer",
  3: "Okay",
  4: "Leicht",
  5: "Sehr leicht"
};

interface ReviewFeedback {
  review: {
    id: number;
    next_due: string;
  };
  expanded_content?: {
    answer: string;
  } | null;
  micro_drill?: {
    id: number;
    answer: string;
  } | null;
}

export function ReviewPanel() {
  const queryClient = useQueryClient();
  const { data, isLoading } = useQuery({
    queryKey: ["due"],
    queryFn: async () => {
      const { data } = await api.get("/review/due", { params: { limit: 5 } });
      return data;
    },
    refetchInterval: 30_000
  });
  const [feedback, setFeedback] = useState<ReviewFeedback | null>(null);

  const mutation = useMutation({
    mutationFn: async ({ reviewId, ease }: { reviewId: number; ease: number }) => {
      const { data } = await api.put(`/review/${reviewId}`, { ease });
      return data as ReviewFeedback;
    },
    onSuccess: (result) => {
      setFeedback(result);
      queryClient.invalidateQueries({ queryKey: ["due"] });
      queryClient.invalidateQueries({ queryKey: ["dashboard"] });
    }
  });

  return (
    <section className="rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-lg">
      <h2 className="text-xl font-semibold text-primary-light">Spaced Repetition</h2>
      {isLoading && <p className="mt-4 text-slate-300">Lade Wiederholungen...</p>}
      {!isLoading && !data?.length && <p className="mt-4 text-slate-300">Keine Wiederholungen fällig.</p>}
      <ul className="mt-4 space-y-3">
        {data?.map((review: any) => (
          <li key={review.id} className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
            <p className="text-sm text-slate-300">Content #{review.content_id}</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {Object.entries(easeLabels).map(([ease, label]) => (
                <button
                  key={ease}
                  onClick={() => mutation.mutate({ reviewId: review.id, ease: Number(ease) })}
                  className="rounded-md bg-slate-800 px-3 py-1 text-sm transition hover:bg-primary-light"
                >
                  {label}
                </button>
              ))}
            </div>
          </li>
        ))}
      </ul>
      {feedback?.expanded_content && (
        <div className="mt-6 rounded-lg border border-accent/40 bg-slate-950/70 p-4">
          <h3 className="text-lg font-semibold text-accent">Vertiefende Erklärung</h3>
          <p className="mt-2 whitespace-pre-wrap text-sm text-slate-200">{feedback.expanded_content.answer}</p>
          {feedback.micro_drill && (
            <div className="mt-4 rounded-md border border-primary/40 bg-slate-900/80 p-3 text-sm text-slate-100">
              <h4 className="font-semibold text-primary-light">Micro-Drill #{feedback.micro_drill.id}</h4>
              <p className="mt-2 whitespace-pre-wrap">{feedback.micro_drill.answer}</p>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
