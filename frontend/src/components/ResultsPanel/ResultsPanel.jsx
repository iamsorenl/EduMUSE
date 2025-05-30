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

export default function ResultsPanel({ results, isLoading, selectedText }) {
  const getActionColor = (action) => {
    switch (action) {
      case 'summarize': return 'primary';
      case 'quiz': return 'success';
      case 'search': return 'secondary';
      default: return 'default';
    }
  };

  const getActionIcon = (action) => {
    switch (action) {
      case 'summarize': return '📝';
      case 'quiz': return '🧠';
      case 'search': return '🔍';
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
              Results:
            </Typography>
            
            <Box sx={{ 
              backgroundColor: 'grey.50', 
              p: 2, 
              borderRadius: 1,
              maxHeight: 300,
              overflow: 'auto'
            }}>
              <Typography variant="body2">
                {typeof results.data === 'string' ? results.data : JSON.stringify(results.data, null, 2)}
              </Typography>
            </Box>
          </CardContent>
        </Card>
      )}

      {selectedText && (
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