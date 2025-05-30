import React, { useRef, useEffect, useState, useCallback, useMemo } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { Box, Typography, Button, Paper, TextField, CircularProgress, Alert } from '@mui/material';

// Remove worker setting entirely - let react-pdf use its fallback
// pdfjs.GlobalWorkerOptions.workerSrc = null;

export default function DirectPDFViewer({ file, onTextSelection }) {
  const iframeRef = useRef(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [manualText, setManualText] = useState('');
  const [showManualInput, setShowManualInput] = useState(false);

  const onDocumentLoadSuccess = useCallback(({ numPages }) => {
    setNumPages(numPages);
    setLoading(false);
    setError(null);
    console.log('PDF loaded successfully:', numPages, 'pages');
  }, []);

  const onDocumentLoadError = useCallback((error) => {
    console.error('PDF load error:', error);
    setError('Failed to load PDF');
    setLoading(false);
  }, []);

  const handleTextSelection = useCallback(() => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    
    if (text && text.length > 0) {
      console.log('Selected text:', text);
      onTextSelection && onTextSelection(text);
    }
  }, [onTextSelection]);

  // Options that force polyfill mode
  const documentOptions = useMemo(() => ({
    verbosity: 0,
    disableWorker: true,
    isEvalSupported: false
  }), []);

  if (!file) {
    return (
      <Box sx={{ 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        border: '1px solid #ddd',
        borderRadius: 1,
        backgroundColor: '#f5f5f5'
      }}>
        <Typography variant="h6" color="text.secondary">
          Select a PDF file to view
        </Typography>
      </Box>
    );
  }

  const pdfUrl = `http://127.0.0.1:5000/files/${file.filename}`;

  const handleManualSubmit = () => {
    if (manualText.trim()) {
      onTextSelection(manualText.trim());
      setManualText('');
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* PDF Iframe */}
      <Box sx={{ flex: 1, mb: 2 }}>
        <iframe
          ref={iframeRef}
          src={pdfUrl}
          width="100%"
          height="100%"
          style={{ border: '1px solid #ddd', borderRadius: '4px' }}
          title={`PDF Viewer - ${file.filename}`}
        />
      </Box>

      {/* Manual text input */}
      <Paper sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
          <Typography variant="subtitle2">
            Text Selection:
          </Typography>
          <Button 
            size="small" 
            variant="outlined"
            onClick={() => setShowManualInput(!showManualInput)}
          >
            {showManualInput ? 'Hide' : 'Enter Text'}
          </Button>
        </Box>

        {showManualInput && (
          <Box sx={{ mb: 2 }}>
            <TextField
              fullWidth
              multiline
              rows={3}
              placeholder="Copy text from the PDF above and paste it here..."
              value={manualText}
              onChange={(e) => setManualText(e.target.value)}
              size="small"
            />
            <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
              <Button 
                variant="contained" 
                size="small"
                onClick={handleManualSubmit}
                disabled={!manualText.trim()}
              >
                Use This Text
              </Button>
              <Button 
                variant="outlined" 
                size="small"
                onClick={() => setManualText('')}
              >
                Clear
              </Button>
            </Box>
          </Box>
        )}

        <Typography variant="body2" color="text.secondary">
          💡 Copy text from the PDF above, then click "Enter Text" to paste it for analysis
        </Typography>
      </Paper>
    </Box>
  );
}