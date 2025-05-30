// Import necessary React and Material-UI components
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

// Create a custom Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2', // Primary color
    },
    secondary: {
      main: '#dc004e', // Secondary color
    },
  },
});

function App() {
  // State to manage the currently selected file
  const [selectedFile, setSelectedFile] = useState(null);
  // State to manage the currently selected text
  const [selectedText, setSelectedText] = useState('');
  // State to manage highlights in the PDF viewer
  const [highlights, setHighlights] = useState([]);
  // State to manage results from actions
  const [results, setResults] = useState(null);
  // State to manage loading status
  const [isLoading, setIsLoading] = useState(false);

  // Handler for selecting a file from the file list
  const handleFileSelect = (file) => {
    setSelectedFile(file); // Update the selected file
    setHighlights([]); // Clear highlights when a new file is selected
  };

  // Handler for selecting text in the PDF viewer
  const handleTextSelection = (text, position) => {
    setSelectedText(text); // Update the selected text
    console.log('Selected text:', text); // Log the selected text
  };

  // Handler for adding a highlight in the PDF viewer
  const handleHighlight = (highlight) => {
    setHighlights(prev => [...prev, highlight]); // Add the new highlight to the list
  };

  // Handler for performing an action based on the selected text
  const handleAction = async (action) => {
    if (!selectedText) return; // Do nothing if no text is selected

    // If it's just a highlight action, don't process with AI
    if (action === 'highlight') {
      console.log('Text highlighted:', selectedText);
      return; // Just keep the highlight, no AI processing
    }

    setIsLoading(true); // Set loading state to true
    try {
      console.log(`Performing ${action} on text:`, selectedText.substring(0, 100));
      
      // Simulate an API call with a timeout (mock results for now)
      setTimeout(() => {
        setResults({ 
          action, 
          data: `Mock ${action} result for: "${selectedText.substring(0, 50)}..."` // Mock result data
        });
        setIsLoading(false); // Set loading state to false
      }, 2000);
    } catch (error) {
      console.error('Error calling API:', error); // Log any errors
      setIsLoading(false); // Set loading state to false
    }
  };

  return (
    // Apply the custom Material-UI theme
    <ThemeProvider theme={theme}>
      <CssBaseline /> {/* Normalize CSS across browsers */}
      <Layout> {/* Main layout component */}
        <Box sx={{ flex: 1, p: 2 }}> {/* Main container */}
          <Grid container spacing={2} sx={{ height: 'calc(100vh - 100px)' }}> {/* Grid layout */}
            
            {/* Left sidebar - File list */}
            <Grid size={2}>
              <Paper sx={{ height: '100%', p: 2 }}> {/* Paper component for styling */}
                <FileList 
                  onFileSelect={handleFileSelect} // Pass file selection handler
                  selectedFile={selectedFile} // Pass currently selected file
                />
              </Paper>
            </Grid>

            {/* Center - PDF Viewer */}
            <Grid size={7}>
              <Paper sx={{ height: '100%', p: 2 }}> {/* Paper component for styling */}
                <PDFViewer
                  file={selectedFile} // Pass the selected file to the viewer
                  onTextSelection={handleTextSelection} // Pass text selection handler
                  onHighlight={handleHighlight} // Pass highlight handler
                  highlights={highlights} // Pass current highlights
                  onAction={handleAction} // Pass action handler
                  isLoading={isLoading} // Pass loading state
                />
              </Paper>
            </Grid>

            {/* Right sidebar - Results */}
            <Grid size={3}>
              <Paper sx={{ height: '100%', p: 2 }}> {/* Paper component for styling */}
                <ResultsPanel 
                  results={results} // Pass results data
                  isLoading={isLoading} // Pass loading state
                  selectedText={selectedText} // Pass currently selected text
                />
              </Paper>
            </Grid>
          </Grid>
        </Box>
      </Layout>
    </ThemeProvider>
  );
}

// Export the App component as the default export
export default App;