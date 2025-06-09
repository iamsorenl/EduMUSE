import React from 'react';
import { Box, Typography } from '@mui/material';

export default function SimplePDFViewer({ file }) {
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
          Select a PDF file to view
        </Typography>
      </Box>
    );
  }

  const pdfUrl = `http://127.0.0.1:5000/files/${file.filename}`;

  return (
    <Box sx={{ height: '100%', width: '100%' }}>
      <iframe
        src={pdfUrl}
        width="100%"
        height="100%"
        style={{ border: 'none' }}
        title={`PDF Viewer - ${file.filename}`}
      />
    </Box>
  );
}