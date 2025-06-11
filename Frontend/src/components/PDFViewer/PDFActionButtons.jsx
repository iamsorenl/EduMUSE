import React from 'react';
import {
  ButtonGroup,
  Button,
  Paper,
  Fade,
  Tooltip
} from '@mui/material';
import {
  Highlight,
  Search,
  Psychology,
  Sync
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
          <Tooltip title="Just highlight this text without AI processing">
            <Button
              startIcon={<Highlight />}
              onClick={() => onAction('highlight')}
              disabled={isLoading}
              color="warning"
            >
              Just Highlight
            </Button>
          </Tooltip>
          
          <Tooltip title="Search the web for information about this text">
            <Button
              startIcon={<Search />}
              onClick={() => onAction('search')}
              disabled={isLoading}
              color="info"
            >
              Academic Paper Web Search
            </Button>
          </Tooltip>
          
          <Tooltip title="Use LLM to explain this concept">
            <Button
              startIcon={<Psychology />}
              onClick={() => onAction('explain')}
              disabled={isLoading}
              color="secondary"
            >
              Academic Paper LLM Result
            </Button>
          </Tooltip>
          
          <Tooltip title="Use hybrid approach combining web search and LLM">
            <Button
              startIcon={<Sync />}
              onClick={() => onAction('analyze')}
              disabled={isLoading}
              color="success"
            >
              Hybrid Academic Paper Result
            </Button>
          </Tooltip>
        </ButtonGroup>
      </Paper>
    </Fade>
  );
}
