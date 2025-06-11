import React from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Divider,
  Button,
  IconButton,
  Stack,
  Collapse
} from '@mui/material';
import { Psychology, CheckCircle, Clear, Close, DeleteOutline, ExpandMore, ExpandLess, HighlightOff } from '@mui/icons-material';

// Helper function to format CrewAI results
const formatResult = (data) => {
  if (!data) {
    return (
      <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
        No result data available
      </Typography>
    );
  }

  if (typeof data === 'string') {
    return (
      <Typography variant="body2" sx={{ fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>
        {data}
      </Typography>
    );
  }

  // Handle structured data from CrewAI
  if (typeof data === 'object') {
    return (
      <>
        <Typography variant="subtitle2" color="primary" gutterBottom>
          {data.flow_type || 'AI Analysis'}
        </Typography>
        
        {data.topic && (
          <Typography variant="body2" sx={{ mb: 1 }}>
            <strong>Topic:</strong> {data.topic}
          </Typography>
        )}
        
        {data.retrieval_method && (
          <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
            Method: {data.retrieval_method}
          </Typography>
        )}
        
        {data.sources_found && (
          <Box sx={{ mt: 1 }}>
            <Typography variant="body2" sx={{ fontSize: '0.85rem', whiteSpace: 'pre-wrap' }}>
              {data.sources_found}
            </Typography>
          </Box>
        )}
        
        {/* Display metadata if available */}
        {data.metadata && (
          <Box sx={{ mt: 1, pt: 1, borderTop: '1px dashed rgba(0,0,0,0.1)' }}>
            <Typography variant="caption" color="text.secondary" sx={{ display: 'block' }}>
              <strong>Additional Info:</strong> {Object.keys(data.metadata).map(key => 
                `${key}: ${typeof data.metadata[key] === 'object' ? JSON.stringify(data.metadata[key]) : data.metadata[key]}`
              ).join(', ')}
            </Typography>
          </Box>
        )}
        
        {/* PDF Generation Success - for assessments */}
        {data.flow_type === 'assessment' && data.pdf_files && (
          <Box sx={{ mt: 2, p: 2, bgcolor: 'success.light', borderRadius: 1, border: '1px solid', borderColor: 'success.main' }}>
            <Typography variant="subtitle2" color="success.dark" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              ✅ Assessment PDFs Generated Successfully
            </Typography>
            <Typography variant="body2" color="success.dark" sx={{ fontSize: '0.85rem' }}>
              • Student Assessment: <code>{data.pdf_files.student_assessment?.split('/').pop()}</code><br/>
              • Answer Key: <code>{data.pdf_files.answer_key?.split('/').pop()}</code>
            </Typography>
            <Typography variant="caption" color="success.dark" sx={{ display: 'block', mt: 1 }}>
              📁 Files saved to uploads folder - check the file list to download
            </Typography>
          </Box>
        )}
        
        {/* General PDF success for other flows */}
        {data.pdf_generated && data.flow_type !== 'assessment' && (
          <Box sx={{ mt: 1, p: 1, bgcolor: 'info.light', borderRadius: 1 }}>
            <Typography variant="caption" color="info.dark">
              📄 PDF generated: {data.pdf_filename}
            </Typography>
          </Box>
        )}
      </>
    );
  }

  // Fallback for any other data type
  return (
    <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
      {JSON.stringify(data, null, 2)}
    </Typography>
  );
};

// Individual Result Card Component
const ResultCard = ({ result, onDelete, index }) => {
  const [expanded, setExpanded] = React.useState(index === 0); // First result expanded by default

  const getActionColor = (action) => {
    switch (action) {
      case 'search': return 'info';
      case 'explain': return 'primary';
      case 'analyze': return 'secondary';
      case 'highlight': return 'warning';
      default: return 'default';
    }
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'search': return '🔍';
      case 'explain': return '🧠';
      case 'analyze': return '⚡';
      case 'highlight': return '💡';
      default: return '🤖';
    }
  };

  return (
    <Card sx={{ mb: 1, border: '1px solid', borderColor: 'divider' }}>
      <CardContent sx={{ pb: 1 }}>
        {/* Header with action and controls */}
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
          <Typography variant="body1" sx={{ mr: 1 }}>
            {getActionIcon(result.action)}
          </Typography>
          <Chip 
            label={result.action} 
            color={getActionColor(result.action)}
            size="small"
          />
          <CheckCircle 
            sx={{ ml: 'auto', mr: 1, color: 'success.main', fontSize: 18 }} 
          />
          <IconButton 
            size="small" 
            onClick={() => setExpanded(!expanded)}
            sx={{ mr: 1 }}
          >
            {expanded ? <ExpandLess /> : <ExpandMore />}
          </IconButton>
          <IconButton 
            size="small" 
            onClick={() => onDelete(result.id)}
            color="error"
            title="Delete this result"
          >
            <DeleteOutline fontSize="small" />
          </IconButton>
        </Box>

        {/* Timestamp */}
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mb: 1 }}>
          {new Date(result.timestamp).toLocaleTimeString()}
        </Typography>

        {/* Collapsible content */}
        <Collapse in={expanded}>
          <Box>
            {/* Selected Text Preview */}
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              Selected Text:
            </Typography>
            <Box sx={{ 
              backgroundColor: 'grey.100', 
              p: 1, 
              borderRadius: 1,
              mb: 1,
              fontStyle: 'italic'
            }}>
              <Typography variant="body2" sx={{ fontSize: '0.85rem' }}>
                "{result.text}"
              </Typography>
            </Box>
            
            {/* AI Result */}
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
              AI Result:
            </Typography>
            <Box sx={{ 
              backgroundColor: 'grey.50', 
              p: 1.5, 
              borderRadius: 1,
              maxHeight: 200,
              overflow: 'auto'
            }}>
              {result.error ? (
                <Typography variant="body2" color="error" sx={{ fontSize: '0.85rem' }}>
                  Error: {result.error}
                </Typography>
              ) : (
                formatResult(result.data)
              )}
            </Box>
          </Box>
        </Collapse>
      </CardContent>
    </Card>
  );
};

export default function ResultsPanel({ 
  results, 
  isLoading, 
  selectedText, 
  highlights, 
  onClearAllResults, 
  onDeleteResult,
  onClearHighlights // NEW: Add prop for clearing highlights
}) {

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Psychology sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6">
            AI Results
            {results && results.length > 0 && (
              <Typography component="span" variant="body2" color="text.secondary" sx={{ ml: 1 }}>
                ({results.length})
              </Typography>
            )}
          </Typography>
        </Box>
        
        {/* Clear AI Results Button - only show when there are results */}
        {results && results.length > 0 && !isLoading && onClearAllResults && (
          <IconButton 
            onClick={onClearAllResults}
            size="small"
            color="error"
            title="Clear AI Results Only"
            sx={{ ml: 1 }}
          >
            <Clear />
          </IconButton>
        )}
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
      {/* Loading state */}
      {isLoading && (
        <Box sx={{ 
          display: 'flex', 
          flexDirection: 'column',
          alignItems: 'center', 
          justifyContent: 'center', 
          py: 4 
        }}>
          <CircularProgress size={40} sx={{ mb: 2 }} />
          <Typography variant="body2" color="text.secondary">
            AI is processing your request...
          </Typography>
          {selectedText && (
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1, textAlign: 'center' }}>
              Processing: "{selectedText.substring(0, 50)}..."
            </Typography>
          )}
        </Box>
      )}
      
      {/* Results list */}
      {results && results.length > 0 && (
        <Box sx={{ flex: 1, overflow: 'auto', mb: 2 }}>
          <Stack spacing={1}>
            {results.map((result, index) => (
              <ResultCard 
                key={result.id} 
                result={result} 
                onDelete={onDeleteResult}
                index={index}
              />
            ))}
          </Stack>
          
          {/* Clear AI Results button at bottom */}
          {onClearAllResults && (
            <Button 
              variant="outlined" 
              startIcon={<Clear />}
              onClick={onClearAllResults}
              sx={{ mt: 2, width: '100%' }}
              color="error"
              size="small"
            >
              Clear AI Results ({results.length})
            </Button>
          )}
        </Box>
      )}

      {/* Divider between AI Results and Document Highlights */}
      {((results && results.length > 0) || (highlights && highlights.length > 0)) && (
        <Divider sx={{ my: 1 }} />
      )}

      {/* Document Highlights section - UPDATED with separate clear */}
      {highlights && highlights.length > 0 && (
        <Box sx={{ mt: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 1 }}>
            <Typography variant="subtitle2" sx={{ color: 'text.primary' }}>
              📄 Document Highlights ({highlights.length})
            </Typography>
            {/* Clear Highlights Button - NEW */}
            {onClearHighlights && (
              <IconButton 
                onClick={onClearHighlights}
                size="small"
                color="warning"
                title="Clear All Highlights"
                sx={{ ml: 1 }}
              >
                <HighlightOff fontSize="small" />
              </IconButton>
            )}
          </Box>
          
          <Box sx={{ maxHeight: 150, overflow: 'auto' }}>
            {highlights.slice(0, 3).map((highlight, index) => (
              <Box key={highlight.id || index} sx={{ mb: 1, p: 1, backgroundColor: 'action.hover', borderRadius: 1 }}>
                <Typography variant="caption">
                  {highlight.comment?.emoji || '🎯'} {highlight.comment?.text || 'highlight'}
                </Typography>
                <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                  "{highlight.content?.text?.substring(0, 40) || 'No text'}..."
                </Typography>
              </Box>
            ))}
            {highlights.length > 3 && (
              <Typography variant="caption" color="text.secondary">
                +{highlights.length - 3} more highlights
              </Typography>
            )}
          </Box>
          
          {/* Clear Highlights button at bottom - Alternative placement */}
          {onClearHighlights && (
            <Button 
              variant="text" 
              startIcon={<HighlightOff />}
              onClick={onClearHighlights}
              sx={{ mt: 1, width: '100%' }}
              color="warning"
              size="small"
            >
              Clear Document Highlights ({highlights.length})
            </Button>
          )}
          
          <Typography variant="caption" color="text.secondary" sx={{ fontStyle: 'italic', display: 'block', mt: 1 }}>
            * Highlights are managed separately from AI results
          </Typography>
        </Box>
      )}

      {/* Currently selected text */}
      {selectedText && results.length === 0 && !isLoading && (
        <Box sx={{ mt: 'auto', p: 2, backgroundColor: 'action.hover', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Currently selected:
          </Typography>
          <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
            "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
          </Typography>
        </Box>
      )}
      
      {/* Empty state */}
      {results.length === 0 && !isLoading && !selectedText && (
        <Box sx={{ 
          textAlign: 'center', 
          py: 4,
          color: 'text.secondary'
        }}>
          <Psychology sx={{ fontSize: 48, mb: 2, opacity: 0.3 }} />
          <Typography variant="body2">
            Select text in the PDF to see AI-powered analysis here.
          </Typography>
        </Box>
      )}
    </Box>
  );
}
