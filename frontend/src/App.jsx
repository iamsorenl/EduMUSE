import React, { useState } from 'react';
import { 
  Box, 
  Grid,
  Paper,
  ThemeProvider,
  createTheme,
  CssBaseline 
} from '@mui/material';
import Layout from './components/Layout/Layout';
import PDFViewer from './components/PDFViewer/PDFViewer';
import FileList from './components/FileList/FileList';
import ResultsPanel from './components/ResultsPanel/ResultsPanel';

// Create MUI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedText, setSelectedText] = useState('');
  const [highlights, setHighlights] = useState([]);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setHighlights([]);
  };

  const handleTextSelection = (text, position) => {
    setSelectedText(text);
    console.log('Selected text:', text);
  };

  const handleHighlight = (highlight) => {
    setHighlights(prev => [...prev, highlight]);
  };

  const handleAction = async (action) => {
    if (!selectedText) return;

    setIsLoading(true);
    try {
      // Mock results for now since CrewAI backend isn't ready
      setTimeout(() => {
        setResults({ 
          action, 
          data: `Mock ${action} result for: "${selectedText.substring(0, 50)}..."` 
        });
        setIsLoading(false);
      }, 2000);
    } catch (error) {
      console.error('Error calling API:', error);
      setIsLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Layout>
        <Box sx={{ flex: 1, p: 2 }}>
          <Grid container spacing={2} sx={{ height: 'calc(100vh - 100px)' }}>
            {/* Left sidebar - File list */}
            <Grid size={2}>
              <Paper sx={{ height: '100%', p: 2 }}>
                <FileList 
                  onFileSelect={handleFileSelect}
                  selectedFile={selectedFile}
                />
              </Paper>
            </Grid>

            {/* Center - PDF Viewer */}
            <Grid size={7}>
              <Paper sx={{ height: '100%', p: 2 }}>
                <PDFViewer
                  file={selectedFile}
                  onTextSelection={handleTextSelection}
                  onHighlight={handleHighlight}
                  highlights={highlights}
                  onAction={handleAction}
                  isLoading={isLoading}
                />
              </Paper>
            </Grid>

            {/* Right sidebar - Results */}
            <Grid size={3}>
              <Paper sx={{ height: '100%', p: 2 }}>
                <ResultsPanel 
                  results={results} 
                  isLoading={isLoading}
                  selectedText={selectedText}
                />
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Layout>
    </ThemeProvider>
  );
}

export default App;
