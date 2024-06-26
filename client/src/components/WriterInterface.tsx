import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlay, faPause, faStop } from '@fortawesome/free-solid-svg-icons';

interface WriterInterfaceProps {
  serverIP: string;
}

export const WriterInterface: React.FC<WriterInterfaceProps> = ({ serverIP }) => {
  const [text, setText] = useState('');
  const [minDelay, setMinDelay] = useState(0.05);
  const [maxDelay, setMaxDelay] = useState(0.2);
  const [status, setStatus] = useState<'idle' | 'writing' | 'paused'>('idle');

  const handleWrite = async () => {
    setStatus('writing');
    try {
      const response = await fetch(`http://${serverIP}:8000/execute/write`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, min_delay: minDelay, max_delay: maxDelay }),
      });
      if (response.ok) {
        await response.json();
        setStatus('idle');
      } else {
        throw new Error('Failed to start writing');
      }
    } catch (error) {
      setStatus('idle');
    }
  };

  const handlePause = async () => {
    try {
      const response = await fetch(`http://${serverIP}:8000/execute/pause`, { method: 'POST' });
      if (response.ok) {
        setStatus('paused');
      } else {
        throw new Error('Failed to pause');
      }
    } catch (error) {
      // Handle error
    }
  };

  const handleResume = async () => {
    try {
      const response = await fetch(`http://${serverIP}:8000/execute/resume`, { method: 'POST' });
      if (response.ok) {
        setStatus('writing');
      } else {
        throw new Error('Failed to resume');
      }
    } catch (error) {
      // Handle error
    }
  };

  const handleStop = async () => {
    try {
      const response = await fetch(`http://${serverIP}:8000/execute/stop`, { method: 'POST' });
      if (response.ok) {
        setStatus('idle');
      } else {
        throw new Error('Failed to stop');
      }
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div className="bg-white shadow-md rounded-lg p-6">
      <h2 className="text-xl font-semibold mb-4">Auto Writer</h2>
      <div className="mb-4">
        <label htmlFor="text" className="block text-sm font-medium text-gray-700">
          Text to Write
        </label>
        <textarea
          id="text"
          className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
          rows={5}
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div>
          <label htmlFor="minDelay" className="block text-sm font-medium text-gray-700">
            Min Delay (seconds)
          </label>
          <input
            type="number"
            id="minDelay"
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            value={minDelay}
            onChange={(e) => setMinDelay(parseFloat(e.target.value))}
            step={0.01}
            min={0}
          />
        </div>
        <div>
          <label htmlFor="maxDelay" className="block text-sm font-medium text-gray-700">
            Max Delay (seconds)
          </label>
          <input
            type="number"
            id="maxDelay"
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            value={maxDelay}
            onChange={(e) => setMaxDelay(parseFloat(e.target.value))}
            step={0.01}
            min={0}
          />
        </div>
      </div>
      <div className="flex space-x-2">
        <button
          onClick={handleWrite}
          disabled={status !== 'idle'}
          className="flex-1 bg-green-500 text-white py-2 px-4 rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 disabled:opacity-50"
        >
          <FontAwesomeIcon icon={faPlay} /> Start
        </button>
        <button
          onClick={status === 'paused' ? handleResume : handlePause}
          disabled={status === 'idle'}
          className="flex-1 bg-yellow-500 text-white py-2 px-4 rounded-md hover:bg-yellow-600 focus:outline-none focus:ring-2 focus:ring-yellow-500 focus:ring-opacity-50 disabled:opacity-50"
        >
          <FontAwesomeIcon icon={status === 'paused' ? faPlay : faPause} />{' '}
          {status === 'paused' ? 'Resume' : 'Pause'}
        </button>
        <button
          onClick={handleStop}
          disabled={status === 'idle'}
          className="flex-1 bg-red-500 text-white py-2 px-4 rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 disabled:opacity-50"
        >
          <FontAwesomeIcon icon={faStop} /> Stop
        </button>
      </div>
    </div>
  );
};