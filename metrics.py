import os
from dotenv import load_dotenv
import datetime
load_dotenv()

class ProjectHealthTracker:
    def __init__(self, total_task_count, completed_task_count, project_start_date, project_end_date, project_risk_factors):
        try:
            self.total_task_count = int(total_task_count)
            self.completed_task_count = int(completed_task_count)
            self.project_start_date = datetime.datetime.strptime(project_start_date, '%Y-%m-%d').date()
            self.project_end_date = datetime.datetime.strptime(project_end_date, '%Y-%m-%d').date()
            if not isinstance(project_risk_factors, list):
                raise ValueError("project_risk_factors must be a list")
            self.project_risk_factors = project_risk_factors
        except ValueError as e:
            print(f"Initialization error: {e}")
        except TypeError as e:
            print(f"Type error during initialization: {e}")
        except Exception as e:
            print(f"Unexpected error occurred during initialization: {e}")

    def compute_project_progress_percentage(self):
        if self.total_task_count <= 0:
            return 0
        progress_percentage = (self.completed_task_count / self.total_task_count) * 100
        return progress_percentage

    def compute_daily_task_completion_rate(self):
        elapsed_days = (datetime.date.today() - self.project_start_date).days
        if elapsed_days <= 0:
            return 0
        daily_completion_rate = self.completed_task_count / elapsed_days
        return daily_completion_rate

    def evaluate_project_risk_level(self):
        risk_factor_count = len(self.project_risk_factors)
        if risk_factor_count > 5:
            return "High"
        elif 0 < risk_factor_count <= 5:
            return "Medium"
        else:
            return "Low"

    def refresh_project_metrics(self, updated_completed_tasks=None, updated_risk_factors=None):
        try:
            if updated_completed_tasks is not None:
                if isinstance(updated_completed_tasks, int) and updated_completed_tasks >= 0:
                    self.completed_task_count = updated_completed_tasks
                else:
                    raise ValueError("Updated completed tasks must be a non-negative integer")
            if updated_risk_factors is not None:
                if isinstance(updated_risk_factors, list) and all(isinstance(item, str) for item in updated_risk_factors):
                    self.project_risk_factors = updated_risk_factors
                else:
                    raise ValueError("Updated risk factors must be a list of strings")
        except ValueError as e:
            print(f"Value error during metrics refresh: {e}")
        except Exception as e:
            print(f"Unexpected error occurred while refreshing metrics: {e}")

if __name__ == "__main__":
    task_total_count = 100
    task_completed_count = 45
    project_start_date_env = os.getenv('PROJECT_START_DATE', '2023-01-01')
    project_end_date_env = os.getenv('PROJECT_END_DATE', '2023-12-31')
    identified_risk_factors = ['New technology', 'Tight schedule']

    project_tracker = ProjectHealthTracker(
        task_total_count,
        task_completed_count,
        project_start_date_env,
        project_end_date_env,
        identified_risk_factors
    )

    print(f"Project Progress: {project_tracker.compute_project_progress_percentage()}%")
    print(f"Task Completion Rate: {project_tracker.compute_daily_task_completion_rate()} tasks/day")
    print(f"Potential Risk Level: {project_tracker.evaluate_project_risk_level()}")