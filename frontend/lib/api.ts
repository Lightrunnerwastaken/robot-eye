import axios from "axios";

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"
});

export type Difficulty = "easy" | "medium" | "hard";

export interface GoalPayload {
  subject: string;
  topic: string;
  exam_date: string;
  difficulty: Difficulty;
  notes?: string;
}

export const fetchDashboard = async () => {
  const { data } = await api.get("/dashboard/");
  return data;
};

export const fetchGoals = async () => {
  const { data } = await api.get("/goals/");
  return data;
};
