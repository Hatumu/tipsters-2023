import React, { useState, useEffect } from 'react';
import './Rules.css'

const RulesComponent = () => {
  const [textContent, setTextContent] = useState('');

  useEffect(() => {
    // Fetch the text content from the file
    fetch('/data/Rules.txt')
        .then(response => response.text())
        .then(data => {
            console.log('Fetched text content:', data);
            setTextContent(data);
        })
      .catch(error => console.error('Error fetching text content:', error));
  }, []);

  return (
    <div className="rules-container">
      {/* Render the text content */}
      <pre>{textContent}</pre>
    </div>
  );
};

export default RulesComponent;
