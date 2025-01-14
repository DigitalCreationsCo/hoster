import { useState } from 'react';
import { uploadFile } from '@/api';
import DomainAssign from './domain-assign';

const FileUpload = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [projectId, setProjectId] = useState(0)

  const handleFileChange = (e: any) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (!file) {
      setError("Please select a file");
      return;
    }

    try {
      const {id: projectId} = await uploadFile(file);
      setError("");
      setProjectId(projectId);
      alert("File uploaded successfully!");
      window.location.replace("/")
    } catch (err) {
      setError("Error uploading file");
    }
  };

  return (
    <>
      <h2>Upload Project Files</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" onChange={handleFileChange} />
        <button type="submit">Upload</button>
      </form>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <DomainAssign projectId={projectId} />
    </>
  );
};

export default FileUpload;
