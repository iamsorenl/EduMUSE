import React, { useState } from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import DirectPDFViewer from './DirectPDFViewer';

export default function PDFViewer({ 
  file, 
  onTextSelection, 
  onAction, 
  isLoading 
}) {
  const [selectedText, setSelectedText] = useState('');

  // Handle text selection from the PDF viewer
  const handleTextSelection = (text) => {
    setSelectedText(text);
    onTextSelection && onTextSelection(text);
  };

  const handleAction = (action) => {
    if (selectedText && onAction) {
      onAction(action);
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* PDF Viewer */}
      <Box sx={{ flex: 1, mb: 2 }}>
        <DirectPDFViewer 
          file={file} 
          onTextSelection={handleTextSelection}
        />
      </Box>

      {/* Selected Text Display */}
      {selectedText && (
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Selected Text:
          </Typography>
          <Typography variant="body2" sx={{ mb: 2 }}>
            "{selectedText}"
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 1 }}>
            <Button 
              variant="outlined" 
              size="small"
              onClick={() => handleAction('summarize')}
              disabled={isLoading}
            >
              Summarize
            </Button>
            <Button 
              variant="outlined" 
              size="small"
              onClick={() => handleAction('explain')}
              disabled={isLoading}
            >
              Explain
            </Button>
            <Button 
              variant="outlined" 
              size="small"
              onClick={() => handleAction('question')}
              disabled={isLoading}
            >
              Ask Question
            </Button>
          </Box>
        </Paper>
      )}

      {/* Instructions */}
      <Paper sx={{ p: 2, backgroundColor: '#f8f9fa' }}>
        <Typography variant="body2" color="text.secondary">
          💡 Highlight text directly in the PDF above to select it
        </Typography>
      </Paper>
    </Box>
  );
}