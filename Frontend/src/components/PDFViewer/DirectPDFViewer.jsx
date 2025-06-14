import React, { useCallback, useEffect } from 'react';
import {
  AreaHighlight,
  Highlight,
  PdfHighlighter,
  PdfLoader,
  Popup,
  Tip,
} from 'react-pdf-highlighter';
import { Box, Typography, Button, ButtonGroup, Paper, Chip } from '@mui/material';
import { Search, Psychology, Delete, Highlight as HighlightIcon, Sync } from '@mui/icons-material';

// CrewAI Action Tip Component (with Highlight option)
const CrewAITip = ({ onConfirm, onCancel }) => (
  <Paper sx={{ p: 2, maxWidth: 300, boxShadow: 3, borderRadius: 2 }}>
    <Typography variant="subtitle2" gutterBottom color="primary">
      Choose an action:
    </Typography>
    
    <ButtonGroup 
      variant="contained" 
      size="small" 
      orientation="vertical" 
      fullWidth
      sx={{ mb: 2 }}
    >
      <Button
        startIcon={<HighlightIcon />}
        onClick={() => onConfirm({ text: 'highlight', emoji: '💡' })}
        color="warning"
      >
        Just Highlight
      </Button>
      <Button
        startIcon={<Search />}
        onClick={() => onConfirm({ text: 'search', emoji: '🔍' })}
        color="info"
      >
        Academic Paper Web Search
      </Button>
      <Button
        startIcon={<Psychology />}
        onClick={() => onConfirm({ text: 'explain', emoji: '🧠' })}
        color="secondary"
      >
        Academic Paper LLM Result
      </Button>
      <Button
        startIcon={<Sync />}
        onClick={() => onConfirm({ text: 'analyze', emoji: '⚡' })}
        color="success"
      >
        Hybrid Academic Paper Result
      </Button>
    </ButtonGroup>

    <Button 
      variant="outlined" 
      size="small" 
      fullWidth
      onClick={onCancel}
    >
      Cancel
    </Button>
  </Paper>
);

// Highlight Popup Component (shows when clicking existing highlights)
const HighlightPopup = ({ comment, onAction, onDelete }) => (
  <Paper sx={{ p: 2, maxWidth: 250, boxShadow: 3, borderRadius: 2 }}>
    {comment?.text && (
      <>
        <Typography variant="body2" gutterBottom>
          {comment.emoji} Action: <Chip label={comment.text} size="small" />
        </Typography>
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 2 }}>
          Choose a new action for this highlight:
        </Typography>
      </>
    )}
    
    <ButtonGroup variant="outlined" size="small" orientation="vertical" fullWidth>
      <Button onClick={() => onAction('highlight')}>💡 Keep Highlighted</Button>
      <Button onClick={() => onAction('search')}>🔍 Web Search</Button>
      <Button onClick={() => onAction('explain')}>🧠 LLM Explain</Button>
      <Button onClick={() => onAction('analyze')}>⚡ Hybrid Analysis</Button>
    </ButtonGroup>
    
    {onDelete && (
      <Button 
        variant="text" 
        size="small" 
        fullWidth
        onClick={onDelete}
        startIcon={<Delete />}
        sx={{ mt: 1, color: 'error.main' }}
      >
        Delete This Highlight
      </Button>
    )}
  </Paper>
);

// Simple Spinner component
const Spinner = () => (
  <Box sx={{ 
    display: 'flex', 
    alignItems: 'center', 
    justifyContent: 'center', 
    height: '100%',
    flexDirection: 'column'
  }}>
    <Typography variant="h6" sx={{ mb: 2 }}>Loading PDF...</Typography>
    <Typography variant="body2" color="text.secondary">
      Please wait while the document loads
    </Typography>
  </Box>
);

export default function DirectPDFViewer({
  file,
  highlights,
  onAddHighlight,
  onUpdateHighlight,
  onResetHighlights,
  onDeleteHighlight,
  onAction,
  isLoading,
  scrollViewerTo,
  resetHash
}) {

  // Handle action confirmation from tip
  const handleActionConfirm = useCallback((comment, highlight) => {
    // Always add the highlight (visual highlighting)
    onAddHighlight({
      content: highlight.content,
      position: highlight.position,
      comment
    });

    // Only trigger CrewAI processing for non-highlight actions
    if (comment.text !== 'highlight') {
      onAction(comment.text, highlight.content.text);
    } else {
      // For highlight action, just update the selected text in parent
      onAction('highlight', highlight.content.text);
    }
  }, [onAddHighlight, onAction]);

  // Handle actions from existing highlights
  const handleExistingHighlightAction = useCallback((action, highlight) => {
    // Update the highlight's comment to reflect the new action
    const updatedComment = {
      text: action,
      emoji: getActionEmoji(action)
    };
    
    // Update the highlight
    onUpdateHighlight(highlight.id, {}, { comment: updatedComment });
    
    // Trigger action if not just highlighting
    if (action !== 'highlight') {
      onAction(action, highlight.content.text);
    }
  }, [onAction, onUpdateHighlight]);

  // Handle clear all highlights - Enhanced feedback
  const handleClearAll = useCallback(() => {
    console.log("Clear All clicked - clearing", highlights.length, "highlights");
    resetHash();
    onResetHighlights();
  }, [onResetHighlights, resetHash, highlights.length]);

  // Handle individual highlight deletion - FIXED
  const handleDeleteHighlight = useCallback((highlightToDelete) => {
    console.log('Deleting individual highlight:', highlightToDelete.id);
    
    // Use the new onDeleteHighlight prop if available, otherwise filter manually
    if (onDeleteHighlight) {
      onDeleteHighlight(highlightToDelete.id);
    } else {
      // Fallback: let the parent component handle it by notifying about the deletion
      console.warn('onDeleteHighlight not provided, using fallback method');
      // You could also emit an event or use a callback here
    }
  }, [onDeleteHighlight]);

  // Helper function to get emoji for actions
  const getActionEmoji = (action) => {
    switch (action) {
      case 'highlight': return '💡';
      case 'search': return '🔍';
      case 'explain': return '🧠';
      case 'analyze': return '⚡';
      default: return '🎯';
    }
  };

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
          Select a file to view
        </Typography>
      </Box>
    );
  }
  
  // Handle non-PDF files (like podcasts)
  if (file.type === 'podcast') {
    return (
      <Box sx={{ 
        height: '100%', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center',
        flexDirection: 'column',
        border: '1px solid #ddd',
        borderRadius: 1,
        backgroundColor: '#f5f5f5',
        p: 3
      }}>
        <Typography variant="h5" color="primary" gutterBottom>
          🎧 Podcast Audio File
        </Typography>
        <Typography variant="body1" sx={{ mb: 3, textAlign: 'center' }}>
          {file.filename.split('/').pop().replace('.mp3', '').replace(/_/g, ' ')}
        </Typography>
        
        <Box sx={{ width: '100%', maxWidth: 500, mb: 3 }}>
          <audio controls style={{ width: '100%' }}>
            <source src={`http://127.0.0.1:5000/files/${file.filename}`} type="audio/mpeg" />
            Your browser does not support the audio element.
          </audio>
        </Box>
        
        <Typography variant="body2" color="text.secondary" sx={{ textAlign: 'center' }}>
          This is a podcast generated from a PDF document. You can listen to it directly in the browser.
        </Typography>
      </Box>
    );
  }

  const pdfUrl = `http://127.0.0.1:5000/files/${file.filename}`;

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Highlights summary */}
      {highlights.length > 0 && (
        <Paper sx={{ p: 1, mb: 1, backgroundColor: 'action.hover' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Typography variant="caption">
              {highlights.length} highlight{highlights.length !== 1 ? 's' : ''} 
              ({highlights.filter(h => h.comment?.text === 'highlight').length} saved, {highlights.filter(h => h.comment?.text !== 'highlight').length} processed)
            </Typography>
            <Button 
              size="small" 
              variant="outlined" 
              onClick={handleClearAll}
              startIcon={<Delete />}
              color="error" // Make it more obvious it's a destructive action
            >
              Clear All
            </Button>
          </Box>
          
          <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mt: 0.5 }}>
            {highlights.slice(0, 4).map((h, index) => (
              <Chip 
                key={h.id || index} 
                label={`${h.comment?.emoji || '🎯'} "${h.content?.text?.substring(0, 15) || 'Highlight'}..."`}
                size="small"
                variant="outlined"
                clickable
                color={h.comment?.text === 'highlight' ? 'warning' : 'primary'}
                onClick={() => {
                  document.location.hash = `highlight-${h.id}`;
                }}
              />
            ))}
            {highlights.length > 4 && (
              <Chip 
                label={`+${highlights.length - 4} more`}
                size="small"
                variant="outlined"
              />
            )}
          </Box>
        </Paper>
      )}

      {/* PDF Highlighter - NO key prop here since it's handled by parent */}
      <Box sx={{ flex: 1, position: 'relative' }}>
        <PdfLoader url={pdfUrl} beforeLoad={<Spinner />}>
          {(pdfDocument) => (
            <PdfHighlighter
              pdfDocument={pdfDocument}
              enableAreaSelection={(event) => event.altKey}
              onScrollChange={resetHash}
              scrollRef={(scrollTo) => {
                scrollViewerTo.current = scrollTo;
                // Auto-scroll to hash on load
                const highlightId = document.location.hash.slice("#highlight-".length);
                if (highlightId) {
                  const highlight = highlights.find(h => h.id === highlightId);
                  if (highlight) {
                    scrollTo(highlight);
                  }
                }
              }}
              onSelectionFinished={(
                position,
                content,
                hideTipAndSelection,
                transformSelection
              ) => (
                <CrewAITip
                  onConfirm={(comment) => {
                    handleActionConfirm(comment, { content, position });
                    hideTipAndSelection();
                  }}
                  onCancel={hideTipAndSelection}
                />
              )}
              highlightTransform={(
                highlight,
                index,
                setTip,
                hideTip,
                viewportToScaled,
                screenshot,
                isScrolledTo
              ) => {
                const isTextHighlight = !highlight.content?.image;

                const component = isTextHighlight ? (
                  <Highlight
                    isScrolledTo={isScrolledTo}
                    position={highlight.position}
                    comment={highlight.comment}
                  />
                ) : (
                  <AreaHighlight
                    isScrolledTo={isScrolledTo}
                    highlight={highlight}
                    onChange={(boundingRect) => {
                      onUpdateHighlight(
                        highlight.id,
                        { boundingRect: viewportToScaled(boundingRect) },
                        { image: screenshot(boundingRect) }
                      );
                    }}
                  />
                );

                return (
                  <Popup
                    popupContent={
                      <HighlightPopup 
                        comment={highlight.comment}
                        onAction={(action) => {
                          handleExistingHighlightAction(action, highlight);
                          hideTip();
                        }}
                        onDelete={() => {
                          handleDeleteHighlight(highlight);
                          hideTip();
                        }}
                      />
                    }
                    onMouseOver={(popupContent) =>
                      setTip(highlight, () => popupContent)
                    }
                    onMouseOut={hideTip}
                    key={index}
                  >
                    {component}
                  </Popup>
                );
              }}
              highlights={highlights}
            />
          )}
        </PdfLoader>
      </Box>

      {/* Instructions */}
      <Paper sx={{ p: 1, mt: 1, backgroundColor: '#e3f2fd' }}>
        <Typography variant="caption" color="text.secondary">
          💡 <strong>Select text</strong> to highlight or trigger AI actions • <strong>Alt+drag</strong> for areas • <strong>Click highlights</strong> for options
          {isLoading && ' • Processing...'}
        </Typography>
      </Paper>
    </Box>
  );
}
