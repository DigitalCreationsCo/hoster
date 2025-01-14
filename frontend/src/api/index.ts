import { Project } from '@/types';
import axios from 'axios';

const apiUrl = import.meta.env.VITE_BACKEND_URL + 'api/';

export const uploadFile = async (file: any) => {
  const formData = new FormData();
  formData.append('file', file);
  
  try {
    const response = await axios.post(`${apiUrl}projects/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading file", error);
    throw error;
  }
};

export const assignDomain = async (projectId: number, domain: string) => {
  try {
    const response = await axios.post(`${apiUrl}projecs/${projectId}/domain`, { domain });
    return response.data;
  } catch (error) {
    console.error("Error assigning domain", error);
    throw error;
  }
};

export const deleteProject = async (projectId: number) => {
  try {
    const response = await axios.delete(`${apiUrl}projects/${projectId}/`);
    return response.data;
  } catch (error) {
    console.error("Error deleting project", error);
    throw error;
  }
};

export const getProjects = async () => {
  try {
    const response = await axios.get(`${apiUrl}projects/`);
    let projects:Project[] = response.data;

    console.info('get projects')
    projects = projects.map((project) => {
      const fileUrl = project.file;

      console.info('file url', fileUrl)
      return project;
    })
    console.info(JSON.stringify(projects))
    return projects

  } catch (error) {
    console.error("Error fetching projects", error);
    throw error;
  }
};
