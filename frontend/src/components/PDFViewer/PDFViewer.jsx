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

  // Handle text selection from the PDF viewer - simplified to avoid duplication
  const handleTextSelection = (text) => {
    setSelectedText(text);
    // Pass directly to parent without additional processing
    onTextSelection && onTextSelection(text);
  };

  const handleAction = (action) => {
    if (selectedText && onAction) {
      onAction(action);
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* PDF Viewer - this handles the actual text selection */}
      <Box sx={{ flex: 1 }}>
        <DirectPDFViewer 
          file={file} 
          onTextSelection={handleTextSelection}
        />
      </Box>

      {/* Action buttons - only show when text is selected */}
      {selectedText && (
        <Paper sx={{ p: 2, mt: 2 }}>
          <Typography variant="subtitle2" gutterBottom>
            Selected Text:
          </Typography>
          <Typography variant="body2" sx={{ mb: 2, fontStyle: 'italic' }}>
            "{selectedText.length > 100 ? selectedText.substring(0, 100) + '...' : selectedText}"
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
            <Button 
              variant="text" 
              size="small"
              onClick={() => setSelectedText('')}
              color="secondary"
            >
              Clear
            </Button>
          </Box>
        </Paper>
      )}
    </Box>
  );
}