import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Box } from '@mui/material';
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
  // Local highlights state for this component
  const [localHighlights, setLocalHighlights] = useState([]);
  const [clearKey, setClearKey] = useState(0); // Key to force re-render only for clear all
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

  // Delete individual highlight function - NO re-render forced
  const deleteHighlight = useCallback((highlightId) => {
    console.log("Deleting highlight with ID:", highlightId);
    setLocalHighlights((prevHighlights) => 
      prevHighlights.filter(h => h.id !== highlightId)
    );
    // Clear hash if it's pointing to the deleted highlight
    if (document.location.hash === `#highlight-${highlightId}`) {
      resetHash();
    }
  }, []);

  // Reset highlights - FORCE re-render for clear all operation
  const resetHighlights = useCallback(() => {
    console.log("Clearing all highlights - forcing re-render");
    setLocalHighlights([]);
    resetHash();
    // Force re-render by incrementing the key
    setClearKey(prev => prev + 1);
  }, []);

  // Handle action from highlighting
  const handleHighlightAction = useCallback((action, text) => {
    console.log('PDFViewer handleHighlightAction:', action, text?.substring(0, 50));
    
    // Always pass the text to the parent action handler
    if (onAction) {
      onAction(action, text);
    }
    
    // Also update parent's text selection
    if (onTextSelection && text) {
      onTextSelection(text);
    }
  }, [onAction, onTextSelection]);

  return (
    <Box sx={{ height: '100%' }}>
      <DirectPDFViewer 
        key={`pdf-viewer-${clearKey}`} // Force re-render only when clearKey changes (clear all)
        file={file}
        highlights={localHighlights}
        onAddHighlight={addHighlight}
        onUpdateHighlight={updateHighlight}
        onDeleteHighlight={deleteHighlight}
        onResetHighlights={resetHighlights}
        onAction={handleHighlightAction}
        isLoading={isLoading}
        scrollViewerTo={scrollViewerTo}
        resetHash={resetHash}
      />
    </Box>
  );
}