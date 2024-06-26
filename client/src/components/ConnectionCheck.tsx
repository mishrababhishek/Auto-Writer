import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner, faCheckCircle, faTimesCircle } from '@fortawesome/free-solid-svg-icons';

interface ConnectionCheckProps {
  onConnect: (ip: string) => void;
}

export const ConnectionCheck: React.FC<ConnectionCheckProps> = ({ onConnect }) => {
  const [serverAddress, setServerAddress] = useState('');
  const [status, setStatus] = useState<'idle' | 'checking' | 'success' | 'error'>('idle');

  const checkConnection = async () => {
    setStatus('checking');
    try {
      const response = await fetch(`http://${serverAddress}:8000/health/connection`);
      if (response.ok) {
        setStatus('success');
        setTimeout(() => onConnect(serverAddress), 1500);
      } else {
        setStatus('error');
      }
    } catch (error) {
      setStatus('error');
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Connect to Server</h2>
      <div className="mb-4">
        <label htmlFor="serverAddress" className="block text-sm font-medium text-gray-700">
          Server Address
        </label>
        <input
          type="text"
          id="serverAddress"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
          value={serverAddress}
          onChange={(e) => setServerAddress(e.target.value)}
          placeholder="e.g. 192.168.1.100"
        />
      </div>
      <button
        onClick={checkConnection}
        disabled={status === 'checking'}
        className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 disabled:opacity-50"
      >
        {status === 'checking' ? (
          <FontAwesomeIcon icon={faSpinner} spin />
        ) : (
          'Check Connection'
        )}
      </button>
      {status === 'success' && (
        <p className="mt-2 text-green-600">
          <FontAwesomeIcon icon={faCheckCircle} /> Connected successfully!
        </p>
      )}
      {status === 'error' && (
        <p className="mt-2 text-red-600">
          <FontAwesomeIcon icon={faTimesCircle} /> Connection failed. Please check the server address and try again.
        </p>
      )}
    </div>
  );
};