import React, { useState } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import 'react-pdf/dist/Page/AnnotationLayer.css';
import 'react-pdf/dist/Page/TextLayer.css';

// Configure worker using the official method
pdfjs.GlobalWorkerOptions.workerSrc = new URL(
  'pdfjs-dist/build/pdf.worker.min.mjs',
  import.meta.url,
).toString();

function MyApp() {
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [selectedText, setSelectedText] = useState('');

  function onDocumentLoadSuccess({ numPages }) {
    setNumPages(numPages);
  }

  // Handle text selection
  function handleTextSelection() {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text && text.length > 0) {
      setSelectedText(text);
      console.log('Selected text:', text);
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>React PDF Test</h1>
      
      {/* PDF Viewer */}
      <div 
        style={{ 
          border: '1px solid #ccc', 
          padding: '20px',
          backgroundColor: '#f9f9f9',
          marginBottom: '20px'
        }}
        onMouseUp={handleTextSelection}
      >
        <Document
          file="./uploads/AttentionIsAllYouNeed.pdf"
          onLoadSuccess={onDocumentLoadSuccess}
          onLoadError={(error) => console.error('Error loading PDF:', error)}
        >
          <Page 
            pageNumber={pageNumber} 
            renderTextLayer={true}
            renderAnnotationLayer={false}
            scale={1.0}
          />
        </Document>
      </div>

      {/* Controls */}
      {numPages && (
        <div style={{ marginBottom: '20px' }}>
          <p>
            Page {pageNumber} of {numPages}
          </p>
          <button 
            type="button" 
            disabled={pageNumber <= 1} 
            onClick={() => setPageNumber(pageNumber - 1)}
            style={{ marginRight: '10px', padding: '5px 10px' }}
          >
            Previous
          </button>
          <button 
            type="button" 
            disabled={pageNumber >= numPages} 
            onClick={() => setPageNumber(pageNumber + 1)}
            style={{ padding: '5px 10px' }}
          >
            Next
          </button>
        </div>
      )}

      {/* Selected text display */}
      {selectedText && (
        <div style={{ 
          backgroundColor: '#e3f2fd', 
          padding: '15px', 
          borderRadius: '5px',
          border: '1px solid #2196f3' 
        }}>
          <h3>Selected Text:</h3>
          <p style={{ 
            backgroundColor: 'white', 
            padding: '10px', 
            borderRadius: '3px',
            fontFamily: 'monospace',
            fontSize: '14px',
            border: '1px solid #ddd'
          }}>
            "{selectedText}"
          </p>
          <button 
            onClick={() => setSelectedText('')}
            style={{ 
              padding: '5px 10px', 
              backgroundColor: '#2196f3', 
              color: 'white', 
              border: 'none', 
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            Clear Selection
          </button>
        </div>
      )}

      {/* Instructions */}
      <div style={{ 
        backgroundColor: '#f0f0f0', 
        padding: '15px', 
        borderRadius: '5px',
        marginTop: '20px'
      }}>
        <h3>Instructions:</h3>
        <p>1. The PDF should load above</p>
        <p>2. Try selecting text in the PDF by clicking and dragging</p>
        <p>3. Selected text should appear in the blue box below</p>
        <p>4. Use Previous/Next buttons to navigate pages</p>
      </div>
    </div>
  );
}

export default MyApp;

