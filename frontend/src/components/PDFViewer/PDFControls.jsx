import React from 'react';
import {
  Box,
  Typography,
  IconButton,
  TextField
} from '@mui/material';
import {
  ZoomIn,
  ZoomOut,
  NavigateBefore,
  NavigateNext
} from '@mui/icons-material';

export default function PDFControls({
  filename,
  pageNumber,
  numPages,
  scale,
  onPageChange,
  onPrevPage,
  onNextPage,
  onZoomIn,
  onZoomOut
}) {
  return (
    <Box sx={{ 
      display: 'flex', 
      alignItems: 'center', 
      gap: 2, 
      mb: 2,
      flexWrap: 'wrap'
    }}>
      <Typography variant="h6" sx={{ flexGrow: 1 }}>
        {filename}
      </Typography>
      
      {/* Navigation Controls */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <IconButton onClick={onPrevPage} disabled={pageNumber <= 1}>
          <NavigateBefore />
        </IconButton>
        
        <TextField
          size="small"
          value={pageNumber}
          onChange={(e) => {
            const page = parseInt(e.target.value);
            if (page >= 1 && page <= numPages) {
              onPageChange(page);
            }
          }}
          sx={{ width: 60 }}
        />
        
        <Typography variant="body2">
          of {numPages || '?'}
        </Typography>
        
        <IconButton onClick={onNextPage} disabled={pageNumber >= numPages}>
          <NavigateNext />
        </IconButton>
      </Box>

      {/* Zoom Controls */}
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <IconButton onClick={onZoomOut} disabled={scale <= 0.5}>
          <ZoomOut />
        </IconButton>
        
        <Typography variant="body2" sx={{ minWidth: 40, textAlign: 'center' }}>
          {Math.round(scale * 100)}%
        </Typography>
        
        <IconButton onClick={onZoomIn} disabled={scale >= 3.0}>
          <ZoomIn />
        </IconButton>
      </Box>
    </Box>
  );
}