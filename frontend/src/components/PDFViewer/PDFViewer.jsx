import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import DirectPDFViewer from './DirectPDFViewer';

// Helper functions from react-pdf-highlighter example
const getNextId = () => String(Math.random()).slice(2);

const parseIdFromHash = () =>
  document.location.hash.slice("#highlight-".length);

const resetHash = () => {
  document.location.hash = "";
};

export default function PDFViewer({ 
  file, 
  onTextSelection, 
  onHighlight,
  highlights,
  onAction, 
  isLoading 
}) {
  const [selectedText, setSelectedText] = useState('');
  // Local highlights state for this component
  const [localHighlights, setLocalHighlights] = useState([]);
  const scrollViewerTo = useRef((highlight) => {});

  // Get highlight by ID
  const getHighlightById = useCallback((id) => {
    return localHighlights.find((highlight) => highlight.id === id);
  }, [localHighlights]);

  // Scroll to highlight from hash
  const scrollToHighlightFromHash = useCallback(() => {
    const highlight = getHighlightById(parseIdFromHash());
    if (highlight) {
      scrollViewerTo.current(highlight);
    }
  }, [getHighlightById]);

  // Effect to handle hash changes
  useEffect(() => {
    window.addEventListener("hashchange", scrollToHighlightFromHash, false);
    return () => {
      window.removeEventListener("hashchange", scrollToHighlightFromHash, false);
    };
  }, [scrollToHighlightFromHash]);

  // Add highlight function
  const addHighlight = useCallback((highlight) => {
    console.log("Saving highlight", highlight);
    const newHighlight = { ...highlight, id: getNextId() };
    setLocalHighlights((prevHighlights) => [
      newHighlight,
      ...prevHighlights,
    ]);
    
    // Notify parent component
    onHighlight && onHighlight(newHighlight);
    
    // Extract text for parent's text selection handler
    if (highlight.content && highlight.content.text) {
      onTextSelection && onTextSelection(highlight.content.text);
    }
  }, [onHighlight, onTextSelection]);

  // Update highlight function
  const updateHighlight = useCallback((highlightId, position, content) => {
    console.log("Updating highlight", highlightId, position, content);
    setLocalHighlights((prevHighlights) =>
      prevHighlights.map((h) => {
        const {
          id,
          position: originalPosition,
          content: originalContent,
          ...rest
        } = h;
        return id === highlightId
          ? {
              id,
              position: { ...originalPosition, ...position },
              content: { ...originalContent, ...content },
              ...rest,
            }
          : h;
      })
    );
  }, []);

  // Reset highlights
  const resetHighlights = useCallback(() => {
    setLocalHighlights([]);
    resetHash();
  }, []);

  // Handle action from highlighting
  const handleHighlightAction = useCallback((action, text) => {
    onAction && onAction(action);
    onTextSelection && onTextSelection(text);
  }, [onAction, onTextSelection]);

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
          highlights={localHighlights}
          onAddHighlight={addHighlight}
          onUpdateHighlight={updateHighlight}
          onResetHighlights={resetHighlights}
          onAction={handleHighlightAction}
          isLoading={isLoading}
          scrollViewerTo={scrollViewerTo}
          resetHash={resetHash}
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