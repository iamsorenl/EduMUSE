import React from 'react';
import { Box } from '@mui/material';
import Layout from './components/Layout/Layout';

function App() {
  return (
    <Layout>
      <Box sx={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        hello
      </Box>
    </Layout>
  );
}

export default App;
