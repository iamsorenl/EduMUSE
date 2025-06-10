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
  // State to manage results from actions - CHANGED to array for multiple results
  const [results, setResults] = useState([]);
  // State to manage loading status
  const [isLoading, setIsLoading] = useState(false);

  // Handler for selecting a file from the file list
  const handleFileSelect = (file) => {
    setSelectedFile(file); // Update the selected file
    setHighlights([]); // Clear highlights when a new file is selected
    setResults([]); // Clear all results
    setSelectedText(''); // Clear selected text
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

  // Handler for clearing ALL AI results
  const handleClearAllResults = () => {
    setResults([]);
    console.log('All AI results cleared');
  };

  // Handler for clearing ALL highlights - NEW
  const handleClearHighlights = () => {
    setHighlights([]);
    console.log('All highlights cleared');
  };

  // Handler for deleting individual AI result
  const handleDeleteResult = (resultId) => {
    setResults(prev => prev.filter(result => result.id !== resultId));
    console.log('Individual AI result deleted:', resultId);
  };

  // Updated handler for performing an action - now accepts text parameter
  const handleAction = async (action, text = selectedText) => {
    // Make sure we have text to work with
    const textToProcess = text || selectedText;
    
    if (!textToProcess) {
      console.warn('No text available for action:', action);
      return; // Do nothing if no text is available
    }

    // If it's just a highlight action, don't process with AI
    if (action === 'highlight') {
      console.log('Text highlighted:', textToProcess);
      setSelectedText(textToProcess); // Update selected text for display
      return; // Just keep the highlight, no AI processing
    }

    setIsLoading(true); // Set loading state to true
    
    try {
      console.log(`Performing ${action} on text:`, textToProcess.substring(0, 100));
      
      // Generate unique ID for this result
      const resultId = `result-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
      
      // Make API call to the Flask server
      const response = await fetch('http://127.0.0.1:5000/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          action,
          text: textToProcess
        }),
      });
      
      if (!response.ok) {
        throw new Error(`API call failed with status: ${response.status}`);
      }
      
      const data = await response.json();
      
      // Format the result for display
      const formattedResult = {
        id: resultId,
        action,
        text: textToProcess.substring(0, 100) + (textToProcess.length > 100 ? '...' : ''),
        data: data.result.educational_content[data.result.metadata.flows_executed[0]],
        timestamp: data.timestamp,
        fullText: textToProcess // Keep the full text for reference
      };

      // Add to results array instead of replacing
      setResults(prev => [formattedResult, ...prev]); // Add newest first
      setSelectedText(textToProcess); // Update selected text to show what was processed
      
    } catch (error) {
      console.error('Error calling API:', error); // Log any errors
      const errorResult = {
        id: `error-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
        action,
        text: textToProcess.substring(0, 100) + (textToProcess.length > 100 ? '...' : ''),
        error: `Failed to process request: ${error.message}`,
        timestamp: new Date().toISOString(),
      };
      setResults(prev => [errorResult, ...prev]);
    } finally {
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
                  onAction={handleAction} // Pass action handler (now accepts text parameter)
                  isLoading={isLoading} // Pass loading state
                />
              </Paper>
            </Grid>

            {/* Right sidebar - Results */}
            <Grid size={3}>
              <Paper sx={{ height: '100%', p: 2 }}> {/* Paper component for styling */}
                <ResultsPanel 
                  results={results} // Pass results array
                  isLoading={isLoading} // Pass loading state
                  selectedText={selectedText} // Pass currently selected text
                  highlights={highlights} // Pass highlights for display
                  onClearAllResults={handleClearAllResults} // Pass clear all results handler
                  onDeleteResult={handleDeleteResult} // Pass delete individual result handler
                  onClearHighlights={handleClearHighlights} // Pass clear highlights handler - NEW
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
