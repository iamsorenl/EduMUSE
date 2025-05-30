import React from 'react';
import {
  Box,
  Typography,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Divider
} from '@mui/material';
import { Psychology, CheckCircle } from '@mui/icons-material';

export default function ResultsPanel({ results, isLoading, selectedText, highlights }) {
  const getActionColor = (action) => {
    switch (action) {
      case 'summarize': return 'primary';
      case 'explain': return 'success';
      case 'quiz': return 'secondary';
      case 'analyze': return 'info';
      case 'highlight': return 'warning';
      default: return 'default';
    }
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'summarize': return '📝';
      case 'explain': return '🧠';
      case 'quiz': return '❓';
      case 'analyze': return '🔍';
      case 'highlight': return '💡';
      default: return '🤖';
    }
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
        <Psychology sx={{ mr: 1, color: 'primary.main' }} />
        <Typography variant="h6">
          AI Results
        </Typography>
      </Box>
      
      <Divider sx={{ mb: 2 }} />
      
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
      
      {results && !isLoading && (
        <Card sx={{ mb: 2 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <Typography variant="body1" sx={{ mr: 1 }}>
                {getActionIcon(results.action)}
              </Typography>
              <Chip 
                label={results.action} 
                color={getActionColor(results.action)}
                size="small"
              />
              <CheckCircle 
                sx={{ ml: 'auto', color: 'success.main', fontSize: 20 }} 
              />
            </Box>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Selected Text:
            </Typography>
            <Box sx={{ 
              backgroundColor: 'grey.100', 
              p: 1, 
              borderRadius: 1,
              mb: 2,
              fontStyle: 'italic'
            }}>
              <Typography variant="body2">
                "{results.text || selectedText}"
              </Typography>
            </Box>
            
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              AI Result:
            </Typography>
            
            <Box sx={{ 
              backgroundColor: 'grey.50', 
              p: 2, 
              borderRadius: 1,
              maxHeight: 300,
              overflow: 'auto'
            }}>
              <Typography variant="body2">
                {results.error ? 
                  `Error: ${results.error}` : 
                  (typeof results.data === 'string' ? results.data : JSON.stringify(results.data, null, 2))
                }
              </Typography>
            </Box>
            
            {results.timestamp && (
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                Processed at: {new Date(results.timestamp).toLocaleTimeString()}
              </Typography>
            )}
          </CardContent>
        </Card>
      )}

      {/* Show highlight summary */}
      {highlights && highlights.length > 0 && (
        <Box sx={{ mt: 1 }}>
          <Typography variant="subtitle2" sx={{ mb: 1 }}>
            Document Highlights ({highlights.length})
          </Typography>
          <Box sx={{ maxHeight: 200, overflow: 'auto' }}>
            {highlights.slice(0, 5).map((highlight, index) => (
              <Box key={highlight.id || index} sx={{ mb: 1, p: 1, backgroundColor: 'action.hover', borderRadius: 1 }}>
                <Typography variant="caption">
                  {highlight.comment?.emoji || '🎯'} {highlight.comment?.text || 'highlight'}
                </Typography>
                <Typography variant="body2" sx={{ fontSize: '0.75rem' }}>
                  "{highlight.content?.text?.substring(0, 60) || 'No text'}..."
                </Typography>
              </Box>
            ))}
            {highlights.length > 5 && (
              <Typography variant="caption" color="text.secondary">
                +{highlights.length - 5} more highlights
              </Typography>
            )}
          </Box>
        </Box>
      )}

      {selectedText && !results && !isLoading && (
        <Box sx={{ mt: 'auto', p: 2, backgroundColor: 'action.hover', borderRadius: 1 }}>
          <Typography variant="caption" color="text.secondary">
            Currently selected:
          </Typography>
          <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
            "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
          </Typography>
        </Box>
      )}
      
      {!results && !isLoading && !selectedText && (
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