import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { CircularProgressbar } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';
import { Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

interface Project {
  id: string;
  name: string;
  healthMetrics: {
    progress: number;
    risks: number;
  };
}

const ProjectHealthDashboard: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([]);

  const logDataToConsole = (data: Project[]) => {
    console.log('Fetched Project Health Data:', data);
  };

  const fetchProjectsHealth = async () => {
    const { REACT_APP_API_URL } = process.env;
    try {
      const response = await axios.get(`${REACT_APP_API_URL}/project-health`);
      const fetchedProjects = response.data;
      setProjects(fetchedProjects);
      logDataToConsole(fetchedProjects);
    } catch (error) {
      console.error('Error fetching project health data:', error);
    }
  };

  useEffect(() => {
    fetchProjectsHealth();
  }, []);

  const renderProgressBars = (project: Project) => (
    <div style={{ width: 100, height: 100, margin: '0 auto' }}>
      <CircularProgressbar value={project.healthMetrics.progress} text={`${project.healthMetrics.progress}%`} />
    </div>
  );

  const renderRiskIndicators = (riskLevel: number) => {
    let color = riskLevel < 3 ? 'green' : riskLevel <= 5 ? 'orange' : 'red';
    return <span style={{ color }}>{riskLevel}/10</span>;
  };

  const chartData = {
    labels: projects.map(project => project.name),
    datasets: [
      {
        label: 'Progress',
        data: projects.map(project => project.healthMetrics.progress),
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderColor: 'rgba(75, 192, 192, 1)',
        borderWidth: 1,
      },
      {
        label: 'Risks',
        data: projects.map(project => project.healthMetrics.risks),
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgba(255, 99, 132, 1)',
        borderWidth: 1,
      },
    ],
  };

  return (
    <div>
      <h2>Project Health Dashboard</h2>
      <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}>
        {projects.map(project => (
          <div key={project.id} style={{ margin: 20, textAlign: 'center' }}>
            <h3>{project.name}</h3>
            {renderProgressBars(project)}
            <h4>Risk Level: {renderRiskIndicators(project.healthMetrics.risks)}</h4>
          </div>
        ))}
      </div>
      <div>
        <h2>Progress and Risks Overview</h2>
        <Bar data={chartData} />
      </div>
    </div>
  );
};

export default ProjectHealthDashboard;