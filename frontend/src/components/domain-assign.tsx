import { useState } from 'react';
import { assignDomain } from '@/api';

const DomainAssign = ({ projectId }: {projectId: number}) => {
  const [domain, setDomain] = useState('');
  const [error, setError] = useState("");

  const handleDomainChange = (e: any) => {
    setDomain(e.target.value);
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    if (!domain) {
      setError("Please enter a domain");
      return;
    }

    try {
      await assignDomain(projectId, domain);
      setError("");
      alert("Domain assigned successfully!");
    } catch (err) {
      setError("Error assigning domain");
    }
  };

  return (
    <div>
      {projectId && <form onSubmit={handleSubmit}>
        <h2>Assign Domain</h2>
        <input
          type="text"
          placeholder="Enter your domain"
          value={domain}
          onChange={handleDomainChange}
        />
        <button type="submit">Assign Domain</button>
      </form> ||
      <p>Upload a project to assign the domain.</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default DomainAssign;
