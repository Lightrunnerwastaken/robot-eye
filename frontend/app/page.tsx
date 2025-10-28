import { Dashboard } from "../components/Dashboard";
import { GoalForm } from "../components/GoalForm";
import { GoalList } from "../components/GoalList";
import { ReviewPanel } from "../components/ReviewPanel";

export default function HomePage() {
  return (
    <div className="flex flex-col gap-8">
      <GoalForm />
      <GoalList />
      <Dashboard />
      <ReviewPanel />
    </div>
  );
}
