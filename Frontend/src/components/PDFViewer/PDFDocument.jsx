import React, { useMemo } from 'react';
import { Document, Page, pdfjs } from 'react-pdf';
import { Box, Typography, Alert, Button, CircularProgress } from '@mui/material';

export default function PDFDocument({
  pdfUrl,
  pageNumber,
  scale,
  onLoadSuccess,
  onLoadError,
  onTextSelection,
  error,
  loading
}) {
  const handleError = (error) => {
    console.error('PDF Load Error Details:', error);
    console.log('PDF URL:', pdfUrl);
    onLoadError(error);
  };

  // Use jsdelivr with the matching version
  const documentOptions = useMemo(() => ({
    cMapUrl: `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/cmaps/`,
    cMapPacked: true,
    standardFontDataUrl: `https://cdn.jsdelivr.net/npm/pdfjs-dist@${pdfjs.version}/standard_fonts/`,
    verbosity: 0,
  }), []);

  console.log('PDFDocument render:', {
    loading,
    pdfUrl: typeof pdfUrl === 'string' ? pdfUrl : `blob(${pdfUrl?.size} bytes)`,
    error,
    pdfVersion: pdfjs.version
  });

  // Show loading state while fetching PDF
  if (loading) {
    return (
      <Box sx={{ 
        flexGrow: 1, 
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        backgroundColor: '#f5f5f5'
      }}>
        <Box sx={{ textAlign: 'center' }}>
          <CircularProgress size={40} sx={{ mb: 2 }} />
          <Typography variant="h6">Fetching PDF...</Typography>
          <Typography variant="body2" color="text.secondary">
            Loading document from server
          </Typography>
        </Box>
      </Box>
    );
  }

  // Show error if no PDF data
  if (!pdfUrl && !loading) {
    return (
      <Box sx={{ 
        flexGrow: 1, 
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: '1px solid',
        borderColor: 'divider',
        borderRadius: 1,
        backgroundColor: '#f5f5f5'
      }}>
        <Box sx={{ textAlign: 'center' }}>
          <Typography variant="h6" color="text.secondary">
            No PDF data available
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            PDF URL: {pdfUrl ? 'Available' : 'Not available'}
          </Typography>
          <Typography variant="body2" color="text.secondary">
            Loading: {loading ? 'Yes' : 'No'}
          </Typography>
        </Box>
      </Box>
    );
  }

  return (
    <Box sx={{ 
      flexGrow: 1, 
      overflow: 'auto',
      position: 'relative',
      border: '1px solid',
      borderColor: 'divider',
      borderRadius: 1,
      backgroundColor: '#f5f5f5'
    }}>
      {error && (
        <Alert 
          severity="error" 
          sx={{ m: 2 }}
        >
          <Typography variant="body2" sx={{ mb: 1 }}>
            {error}
          </Typography>
          <Typography variant="caption">
            PDF Version: {pdfjs.version} | Using jsdelivr CDN
          </Typography>
        </Alert>
      )}

      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center',
          p: 2,
          minHeight: '100%'
        }}
        onMouseUp={onTextSelection}
      >
        <Document
          file={pdfUrl}
          onLoadSuccess={onLoadSuccess}
          onLoadError={handleError}
          options={documentOptions}
          loading={
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', p: 4 }}>
              <CircularProgress size={30} sx={{ mb: 2 }} />
              <Typography variant="h6" sx={{ mb: 2 }}>Loading PDF...</Typography>
              <Typography variant="body2" color="text.secondary">
                Rendering document...
              </Typography>
            </Box>
          }
          error={
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', p: 4 }}>
              <Typography variant="h6" color="error" sx={{ mb: 2 }}>
                Failed to load PDF
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                Worker or document loading issue
              </Typography>
              <Button 
                variant="outlined" 
                onClick={() => window.location.reload()}
              >
                Refresh Page
              </Button>
            </Box>
          }
        >
          {!error && pdfUrl && (
            <Page
              pageNumber={pageNumber}
              scale={scale}
              renderTextLayer={true}
              renderAnnotationLayer={false}
              loading={
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
                  <CircularProgress size={20} sx={{ mr: 1 }} />
                  <Typography variant="body2">Loading page {pageNumber}...</Typography>
                </Box>
              }
            />
          )}
        </Document>
      </Box>
    </Box>
  );
}