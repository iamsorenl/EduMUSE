import React from 'react';
import { Box, Typography } from '@mui/material';
import { PictureAsPdf } from '@mui/icons-material';

export default function EmptyState() {
  return (
    <Box sx={{ 
      display: 'flex', 
      flexDirection: 'column',
      alignItems: 'center', 
      justifyContent: 'center', 
      height: '100%',
      color: 'text.secondary'
    }}>
      <PictureAsPdf sx={{ fontSize: 64, mb: 2, opacity: 0.3 }} />
      <Typography variant="h6" color="text.secondary">
        Select a PDF document to view
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
        Choose a file from the list to get started
      </Typography>
    </Box>
  );
}