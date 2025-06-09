import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  CircularProgress,
  Alert,
  Button
} from '@mui/material';
import { PictureAsPdf, Refresh } from '@mui/icons-material';
import FileUpload from './FileUpload';

export default function FileList({ onFileSelect, selectedFile }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchFiles = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://127.0.0.1:5000/files');
      
      if (response.ok) {
        const data = await response.json();
        setFiles(data.files);
        setError(null);
      } else {
        setError('Failed to load files');
      }
    } catch (err) {
      setError('Error connecting to server');
      console.error('Error fetching files:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = (result) => {
    // Refresh the file list when upload succeeds
    fetchFiles();
  };

  const handleUploadError = (errorMsg) => {
    // You could set a global error here if needed
    console.error('Upload failed:', errorMsg);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 2 }}>
        <CircularProgress size={24} />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
        <Button
          variant="outlined"
          startIcon={<Refresh />}
          onClick={fetchFiles}
          fullWidth
        >
          Retry
        </Button>
      </Box>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
        <Typography variant="h6">
          Documents
        </Typography>
      </Box>
      
      {/* File Upload Component */}
      <FileUpload 
        onUploadSuccess={handleUploadSuccess}
        onUploadError={handleUploadError}
      />
      
      <Divider sx={{ mb: 1 }} />
      
      <List dense>
        {files.map((file) => (
          <ListItem key={file.filename} disablePadding>
            <ListItemButton
              selected={selectedFile?.filename === file.filename}
              onClick={() => onFileSelect(file)}
            >
              <ListItemIcon>
                <PictureAsPdf color="error" />
              </ListItemIcon>
              <ListItemText 
                primary={file.filename}
                primaryTypographyProps={{
                  variant: 'body2',
                  noWrap: true
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
      </List>

      {files.length === 0 && (
        <Typography variant="body2" color="text.secondary" sx={{ p: 2, textAlign: 'center' }}>
          No PDF files found. Upload a PDF to get started.
        </Typography>
      )}

      <Button
        variant="text"
        startIcon={<Refresh />}
        onClick={fetchFiles}
        size="small"
        sx={{ mt: 1, width: '100%' }}
        disabled={loading}
      >
        Refresh List
      </Button>
    </Box>
  );
}