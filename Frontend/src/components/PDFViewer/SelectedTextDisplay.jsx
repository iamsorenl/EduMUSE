import React from 'react';
import { Box, Typography } from '@mui/material';

export default function SelectedTextDisplay({ selectedText }) {
  if (!selectedText) return null;

  return (
    <Box sx={{ mt: 2, p: 1, backgroundColor: 'action.hover', borderRadius: 1 }}>
      <Typography variant="caption" color="text.secondary">
        Selected text:
      </Typography>
      <Typography variant="body2" sx={{ fontStyle: 'italic' }}>
        "{selectedText.substring(0, 200)}{selectedText.length > 200 ? '...' : ''}"
      </Typography>
    </Box>
  );
}