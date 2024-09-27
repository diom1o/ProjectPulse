import os
from dotenv import load_dotenv
import datetime
load_dotenv()

class ProjectHealthTracker:
    def __init__(self, total_task_count, completed_task_count, project_start_date, project_end_date, project_risk_factors):
        self.total_task_count = total_task_count
        self.completed_task_count = completed_task_count
        self.project_start_date = datetime.datetime.strptime(project_start_date, '%Y-%m-%d').date()
        self.project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d').date()
        self.project_risk_factors = project_risk_factors

    def compute_project_progress_percentage(self):
        try:
            progress_percentage = (self.completed_task_count / self.total_task_count) * 100
            return progress_percentage
        except ZeroDivisionError:
            return 0

    def compute_daily_task_completion_rate(self):
        try:
            elapsed_days = (datetime.date.today() - self.project_start_date).days
            daily_completion_rate = self.completed_task_count / elapsed_days
            return daily_completion_rate
        except ZeroDivisionError:
            return 0

    def evaluate_project_risk_level(self):
        risk_level = "Low"
        if len(self.project_risk_factors) > 5:
            risk_level = "High"
        elif 0 < len(self.project_risk_factors) <= 5:
            risk_level = "Medium"
        return risk_level

    def refresh_project_metrics(self, updated_completed_tasks=None, updated_risk_factors=None):
        if updated_completed_tasks is not None:
            self.completed_task_count = updated_completed_tasks
        if updated_risk_factors is not None:
            self.project_risk_factors = updated_risk_factors

if __name__ == "__main__":
    task_total_count = 100
    task_completed_count = 45
    project_start_date_env = os.getenv('PROJECT_START_DATE', '2023-01-01')
    project_end_date_env = os.getenv('PROJECT_END_DATE', '2023-12-31')
    identified_risk_factors = ['New technology', 'Tight schedule']

    project_tracker = ProjectHealthTracker(task_total_count, task_completed_count, project_start_date_env, project_end_date_env, identified_risk_factors)

    print(f"Project Progress: {project_tracker.compute_project_progress_percentage()}%")
    print(f"Task Completion Rate: {project_tracker.compute_daily_task_completion_rate()} tasks/day")
    print(f"Potential Risk Level: {project_tracker.evaluate_project_risk_level()}")