import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Typography,
  TextField,
  Button,
  Paper,
  Avatar,
  CircularProgress,
  Divider,
  IconButton
} from '@mui/material';
import { Send, Psychology, Person, Clear } from '@mui/icons-material';

// Message component for individual chat messages
const ChatMessage = ({ message, isUser }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        mb: 2,
        flexDirection: isUser ? 'row-reverse' : 'row',
      }}
    >
      <Avatar
        sx={{
          bgcolor: isUser ? 'primary.main' : 'secondary.main',
          width: 32,
          height: 32,
          mr: isUser ? 0 : 1,
          ml: isUser ? 1 : 0,
        }}
      >
        {isUser ? <Person fontSize="small" /> : <Psychology fontSize="small" />}
      </Avatar>
      <Paper
        elevation={1}
        sx={{
          p: 1.5,
          maxWidth: '80%',
          borderRadius: 2,
          bgcolor: isUser ? 'primary.light' : 'grey.100',
          color: isUser ? 'white' : 'text.primary',
        }}
      >
        <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
          {message.content}
        </Typography>
        <Typography variant="caption" color={isUser ? 'rgba(255,255,255,0.7)' : 'text.secondary'} sx={{ display: 'block', mt: 0.5 }}>
          {new Date(message.timestamp).toLocaleTimeString()}
        </Typography>
      </Paper>
    </Box>
  );
};

const QAChat = ({ onSendMessage, messages = [], isLoading, onClearChat }) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef(null);
  
  // Scroll to bottom whenever messages change
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <Box sx={{ 
      height: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      maxHeight: '100%', // ← KEEP: Enforce maximum height
      minHeight: 0, // ← KEEP: Allow flex items to shrink
      overflow: 'hidden' // ← ADD: Prevent this container from expanding
    }}>
      {/* Header - Fixed at top */}
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between', 
        mb: 2,
        flexShrink: 0 // Prevent header from shrinking
      }}>
        <Box sx={{ display: 'flex', alignItems: 'center' }}>
          <Psychology sx={{ mr: 1, color: 'secondary.main' }} />
          <Typography variant="h6">
            QA Chat
          </Typography>
        </Box>
        
        {messages.length > 0 && (
          <IconButton 
            onClick={onClearChat}
            size="small"
            color="error"
            title="Clear chat history"
          >
            <Clear />
          </IconButton>
        )}
      </Box>
      
      <Divider sx={{ mb: 2, flexShrink: 0 }} />
      
      {/* Messages area - CRITICAL: Must not expand beyond container */}
      <Box sx={{ 
        flex: 1, // Take remaining space
        minHeight: 0, // Allow shrinking below content size
        maxHeight: '100%', // ← ADD: Don't exceed container height
        overflow: 'auto', // Allow scrolling
        mb: 2,
        display: 'flex',
        flexDirection: 'column',
        pb: 1
      }}>
        {messages.length === 0 ? (
          <Box sx={{ 
            textAlign: 'center', 
            py: 4,
            color: 'text.secondary',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            flex: 1 // ← ADD: Take available space
          }}>
            <Psychology sx={{ fontSize: 48, mb: 2, opacity: 0.3 }} />
            <Typography variant="body2">
              Ask a question to start a conversation with the QA system.
            </Typography>
          </Box>
        ) : (
          <>
            {messages.map((message, index) => (
              <ChatMessage 
                key={index} 
                message={message} 
                isUser={message.sender === 'user'} 
              />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
        
        {isLoading && (
          <Box sx={{ display: 'flex', justifyContent: 'center', my: 2 }}>
            <CircularProgress size={24} />
          </Box>
        )}
      </Box>
      
      {/* Input area - Fixed at bottom */}
      <Box sx={{ 
        display: 'flex', 
        alignItems: 'flex-end',
        flexShrink: 0, // Don't shrink input area
        pt: 1,
        pb: 1,
        borderTop: '1px solid rgba(0,0,0,0.1)'
      }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          size="small"
          multiline
          maxRows={3}
          sx={{ mr: 1 }}
        />
        <Button
          variant="contained"
          color="secondary"
          endIcon={<Send />}
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          sx={{ flexShrink: 0 }} // ← ADD: Don't shrink button
        >
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default QAChat;
