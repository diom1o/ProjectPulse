import os
from dotenv import load_dotenv
import datetime
load_dotenv()

class ProjectHealthMetrics:
    def __init__(self, total_tasks, completed_tasks, start_date, end_date, risk_factors):
        self.total_tasks = total_tasks
        self.completed_tasks = completed_tasks
        self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        self.end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
        self.risk_factors = risk_factors

    def calculate_progress(self):
        try:
            progress = (self.completed_tasks / self.total_tasks) * 100
            return progress
        except ZeroDivisionError:
            return 0

    def calculate_task_completion_rate(self):
        try:
            days_passed = (datetime.date.today() - self.start_date).days
            rate = self.completed_tasks / days_passed
            return rate
        except ZeroDivisionError:
            return 0

    def assess_risks(self):
        risk_level = "Low"
        if len(self.risk_factors) > 5:
            risk_level = "High"
        elif 0 < len(self.risk_factors) <= 5:
            risk_level = "Medium"
        return risk_level

    def update_metrics(self, completed_tasks=None, risk_factors=None):
        if completed_tasks is not None:
            self.completed_tasks = completed_tasks
        if risk_factors is not None:
            self.risk_factors = risk_factors

if __name__ == "__main__":
    total_tasks = 100
    completed_tasks = 45
    start_date = os.getenv('PROJECT_START_DATE', '2023-01-01')
    end_date = os.getenv('PROJECT_END_DATE', '2023-12-31')
    risk_factors = ['New technology', 'Tight schedule']

    project = ProjectHealthMetrics(total_tasks, completed_tasks, start_date, end_date, risk_factors)

    print(f"Project Progress: {project.calculate_progress()}%")
    print(f"Task Completion Rate: {project.calculate_task_completion_rate()} tasks/day")
    print(f"Potential Risk Level: {project.assess_risks()}")