import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faInfoCircle } from '@fortawesome/free-solid-svg-icons';

export const Instructions: React.FC = () => {
  return (
    <div className="bg-white shadow-md rounded-lg p-6 mt-8">
      <h2 className="text-xl font-semibold mb-4">
        <FontAwesomeIcon icon={faInfoCircle} className="mr-2" />
        Instructions
      </h2>
      <ol className="list-decimal list-inside space-y-2">
        <li>Ensure that the Auto Writer Server is running on your local network.</li>
        <li>Enter the server's IP address in the "Server Address" field and click "Check Connection".</li>
        <li>Once connected, you'll see the Auto Writer interface.</li>
        <li>Enter the text you want to auto-write in the text area.</li>
        <li>Set the minimum and maximum delay between keystrokes (in seconds).</li>
        <li>Click "Start" to begin writing. The text will be typed automatically.</li>
        <li>Use the "Pause" button to temporarily stop writing, and "Resume" to continue.</li>
        <li>Click "Stop" to end the writing process at any time.</li>
        <li>Make sure to click on the desired text input area on your computer before starting the auto-writer.</li>
      </ol>
    </div>
  );
};