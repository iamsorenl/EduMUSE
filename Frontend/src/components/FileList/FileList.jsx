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
  Button,
  IconButton,
  Tooltip,
  Menu,
  MenuItem,
  ListItemSecondaryAction
} from '@mui/material';
import { PictureAsPdf, Refresh, MoreVert, Summarize, Quiz } from '@mui/icons-material';
import FileUpload from './FileUpload';

export default function FileList({ onFileSelect, selectedFile, onAction, isLoading }) {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [processingFile, setProcessingFile] = useState(null);
  const [anchorEl, setAnchorEl] = useState(null);
  const [selectedActionFile, setSelectedActionFile] = useState(null);

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

  const handleActionMenuOpen = (event, file) => {
    setAnchorEl(event.currentTarget);
    setSelectedActionFile(file);
  };

  const handleActionMenuClose = () => {
    setAnchorEl(null);
    setSelectedActionFile(null);
  };

  const handleActionSelect = (action) => {
    if (selectedActionFile && onAction) {
      // Set the processing file to show loading indicator
      setProcessingFile(selectedActionFile.filename);
      
      // Call the action handler with isPdf=true since we're processing a whole file
      onAction(action, selectedActionFile.filename, true);
      
      // Close the menu
      handleActionMenuClose();
    }
  };

  // Reset processingFile when isLoading becomes false
  useEffect(() => {
    if (!isLoading && processingFile) {
      setProcessingFile(null);
    }
  }, [isLoading]);

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
          <ListItem 
            key={file.filename} 
            disablePadding
            secondaryAction={
              <Tooltip title="Generate AI Content">
                <IconButton 
                  edge="end" 
                  size="small"
                  onClick={(e) => handleActionMenuOpen(e, file)}
                  disabled={isLoading}
                >
                  <MoreVert fontSize="small" />
                </IconButton>
              </Tooltip>
            }
          >
            <ListItemButton
              selected={selectedFile?.filename === file.filename}
              onClick={() => onFileSelect(file)}
              disabled={isLoading && processingFile === file.filename}
            >
              <ListItemIcon>
                {isLoading && processingFile === file.filename ? (
                  <CircularProgress size={20} color="primary" />
                ) : (
                  <PictureAsPdf color="error" />
                )}
              </ListItemIcon>
              <ListItemText 
                primary={file.filename}
                primaryTypographyProps={{
                  variant: 'body2',
                  noWrap: true
                }}
                secondary={isLoading && processingFile === file.filename ? "Processing..." : null}
                secondaryTypographyProps={{
                  variant: 'caption',
                  color: 'primary'
                }}
              />
            </ListItemButton>
          </ListItem>
        ))}
        
        {/* Action Menu */}
        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleActionMenuClose}
        >
          <MenuItem onClick={() => handleActionSelect('summarize')}>
            <ListItemIcon>
              <Summarize fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Generate Summary" />
          </MenuItem>
          <MenuItem onClick={() => handleActionSelect('assess')}>
            <ListItemIcon>
              <Quiz fontSize="small" />
            </ListItemIcon>
            <ListItemText primary="Generate Assessment" />
          </MenuItem>
        </Menu>
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
