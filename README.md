# IWNF02-chatbot

A modern, responsive chat interface powered by Google's Gemini AI. Built with Flask, HTMX, and Tailwind CSS.

## Features

- 🤖 Real-time AI responses using Google's Gemini-Pro model
- 💨 Fast and responsive UI with HTMX
- 🎨 Modern dark mode design using Tailwind CSS
- 📱 Fully responsive layout
- ⚡ Minimal JavaScript usage
- 🔄 Dynamic message loading with loading indicators

## Environment Variables

The following environment variables are required:

| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Google Gemini API key for AI functionality | Yes |
| FLASK_ENV | Flask environment (development/production) | No |
| FLASK_DEBUG | Enable Flask debug mode (1/0) | No |

### Setup Instructions

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your-api-key-here
   ```

## Tech Stack

- **Backend**: Python/Flask
- **Frontend**: HTMX, Tailwind CSS
- **AI Model**: Google Gemini-Pro
- **Dependencies**: See `requirements.txt`

## Setup

1. Clone the repository
