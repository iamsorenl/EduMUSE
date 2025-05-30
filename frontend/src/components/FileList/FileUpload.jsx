import React, { useState } from 'react';
import {
  Box,
  Button,
  CircularProgress,
  Typography,
  Alert,
  styled
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

const HiddenInput = styled('input')({
  display: 'none',
});

export default function FileUpload({ onUploadSuccess, onUploadError }) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Check if it's a PDF
    if (file.type !== 'application/pdf') {
      const errorMsg = 'Please select a PDF file';
      setError(errorMsg);
      onUploadError?.(errorMsg);
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Upload successful:', result);
        
        // Clear the input
        event.target.value = '';
        
        // Clear any previous errors
        setError(null);
        
        // Notify parent component
        onUploadSuccess?.(result);
      } else {
        const errorData = await response.json();
        const errorMsg = errorData.error || 'Upload failed';
        setError(errorMsg);
        onUploadError?.(errorMsg);
      }
    } catch (err) {
      const errorMsg = 'Error uploading file';
      setError(errorMsg);
      onUploadError?.(errorMsg);
      console.error('Upload error:', err);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box>
      <Button
        component="label"
        variant="contained"
        startIcon={<CloudUpload />}
        size="small"
        disabled={uploading}
        sx={{ mb: 1 }}
      >
        {uploading ? 'Uploading...' : 'Upload PDF'}
        <HiddenInput
          type="file"
          accept=".pdf"
          onChange={handleFileUpload}
        />
      </Button>

      {uploading && (
        <Box sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1, 
          mb: 1, 
          p: 1, 
          backgroundColor: 'action.hover', 
          borderRadius: 1 
        }}>
          <CircularProgress size={16} />
          <Typography variant="body2">Uploading PDF...</Typography>
        </Box>
      )}

      {error && (
        <Alert severity="error" sx={{ mb: 1 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
    </Box>
  );
}