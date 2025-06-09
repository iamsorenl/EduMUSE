import React from 'react';
import { Box } from '@mui/material';
import Header from './Header';

export default function Layout({ children }) {
  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        flexDirection: 'column',
        backgroundColor: '#f1f1f1',
      }}
    >
      <Header />
      {children}
    </Box>
  );
}
