import React, { useState } from 'react';
import { ConnectionCheck } from './components/ConnectionCheck';
import { WriterInterface } from './components/WriterInterface';

const App: React.FC = () => {
  const [isConnected, setIsConnected] = useState(false);
  const [serverIP, setServerIP] = useState('');

  const handleConnect = (ip: string) => {
    setIsConnected(true);
    setServerIP(ip);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">Auto Writer Client</h1>
        {!isConnected ? (
          <ConnectionCheck onConnect={handleConnect} />
        ) : (
          <WriterInterface serverIP={serverIP} />
        )}
      </div>
    </div>
  );
};

export default App;