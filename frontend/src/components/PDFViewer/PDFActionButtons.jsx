import React from 'react';
import {
  ButtonGroup,
  Button,
  Paper,
  Fade
} from '@mui/material';
import {
  Summarize,
  Quiz,
  Search
} from '@mui/icons-material';

export default function PDFActionButtons({
  show,
  position,
  onAction,
  isLoading
}) {
  return (
    <Fade in={show}>
      <Paper
        sx={{
          position: 'fixed',
          left: position.x - 150,
          top: position.y,
          zIndex: 1000,
          p: 1,
          boxShadow: 3
        }}
      >
        <ButtonGroup variant="contained" size="small">
          <Button
            startIcon={<Summarize />}
            onClick={() => onAction('summarize')}
            disabled={isLoading}
            color="primary"
          >
            Summarize
          </Button>
          <Button
            startIcon={<Quiz />}
            onClick={() => onAction('quiz')}
            disabled={isLoading}
            color="success"
          >
            Quiz Me
          </Button>
          <Button
            startIcon={<Search />}
            onClick={() => onAction('search')}
            disabled={isLoading}
            color="secondary"
          >
            Search
          </Button>
        </ButtonGroup>
      </Paper>
    </Fade>
  );
}