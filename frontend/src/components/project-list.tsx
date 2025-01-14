import { useEffect, useState } from 'react';
import { getProjects, deleteProject } from '@/api';
import { Project } from '@/types';

const ProjectList = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [reallyDelete, setReallyDelete] = useState<number>(0); 
  
  let timeout:NodeJS.Timeout
  useEffect(() => {
    if (reallyDelete) {
      timeout = setTimeout(() => {
        setReallyDelete(0);
      }, 3000);
    }
  
    return () => {
      // Clear the timeout if `reallyDelete` changes or the component unmounts
      clearTimeout(timeout);
    };
  }, [reallyDelete, setReallyDelete]);

  const apiUrl = import.meta.env.VITE_BACKEND_URL;
  console.info('import.meta.env')
  console.info(import.meta.env)
  console.info(import.meta.env.VITE_BACKEND_URL)
  if (!apiUrl) {
    throw new Error('Backend URL is not defined');
  }
  
  const fetchProjects = async () => {
    try {
      const data = await getProjects();
      setProjects(data);
    } catch (err) {
      throw new Error("Error fetching projects");
    }
  };
  
  useEffect(() => {
    fetchProjects();
  }, []);

  const handleDelete = async (projectId: number) => {
    try {
      await deleteProject(projectId);
      setProjects(projects.filter(project => project.id !== projectId));
      alert("Project deleted successfully!");
    } catch (err) {
      throw new Error("Error deleting project");
    }
  };

  console.info('projects')
  console.info(JSON.stringify(projects))
  return (
      <div>
        <h2>Your Projects</h2>
        {projects.length > 0 && (
        <ul>
          {projects.map((project) => (
            <li key={project.id} style={{ listStyle: 'number', display: 'flex', flexDirection: 'column' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                <span>
                  {project.name} - {project.domain}{' '}
                  </span>
                <a href={project.file} target="_blank">Link</a>
                </div>
                <button onClick={() => reallyDelete===project.id ? handleDelete(project.id) : setReallyDelete(project.id)}>{reallyDelete===project.id ? 'Really delete?' : "Delete"}</button>
              </div>
              {/* <div style={{ display: 'flex', justifyContent: 'space-between'}}>
                {project.description}
              </div> */}
            </li>
          ))}
        </ul>) ||
        <p>You have not uploaded a project.</p>}
      </div>
  );
};

export default ProjectList;
