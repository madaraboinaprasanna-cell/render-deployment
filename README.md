# AstraLearn - AI-Powered Student Collaboration Platform

## Overview
AstraLearn is a future-ready, dark-themed collaborative platform designed to help students connect, study together, and track their progress using AI-enhanced matching and personalized learning paths.

Built with **Django**, **HTML**, **CSS**, **JavaScript**, and **SQLite3**.

## Features

### 1. **Modern Dark UI**
- Space-inspired background with stars and twinkling effects.
- Glassmorphism design for panels and cards.
- Glowing interactive elements and responsive layout.

### 2. **Authentication & Profiles**
- Secure SignUp/Login using Django Auth.
- Customizable profiles with avatars, bio, and learning styles (Visual, Auditory, etc.).
- Interests tagging for better group matching.

### 3. **Study Groups & AI Matching**
- Create and join study groups based on subjects.
- **Smart Recommendations**: The system suggests groups that match your interests.
- View group details and members.

### 4. **Live Collaboration Rooms**
- Each group has a dedicated virtual room.
- **Real-time Chat**: Polling-based chat system for seamless communication.
- **Video/Screen Share Integration**: Placeholder UI for future WebRTC integration (simulated actions).

### 5. **Prepared Notes & Resource Sharing**
- Share and download prepared notes for different subjects.
- Support for text-based notes and file uploads.
- Community-driven knowledge sharing.

### 6. **AI-Powered Weekly Tests**
- Generate comprehensive 25-question MCQ tests for any group subject.
- **AI Tutoring**: The platform uses Gemini AI to craft specific questions to assess your learning.
- Grading system (50 marks) with instant performance feedback.

### 7. **Doubt AI Chat**
- Dedicated AI tutor to solve subject-specific doubts instantly using Gemini.

### 8. **Dashboard**
- Overview of joined groups and learning progress.
- Quick access to active study rooms.

## Installation & Setup

1. **Install Dependencies** (Pillow for image handling, requests for API):
   ```bash
   pip install Pillow requests
   ```

2. **Run Migrations**:
   ```bash
   python manage.py makemigrations accounts groups collaborate doubt_ai notes exams
   python manage.py migrate
   ```

3. **Create Superuser (Optional)**:
   ```bash
   python manage.py createsuperuser
   ```

4. **Run Server**:
   ```bash
   python manage.py runserver
   ```
   Or simply run `run_platform.bat` on Windows.

## Usage Guide

1. **Sign Up**: Create an account via the Sign Up button.
2. **Setup Profile**: Add your interests (comma-separated, e.g., "Math, Physics") to get better recommendations.
3. **Join Group**: Browse groups or create one.
4. **Collaborate**: click "Enter Room" on a group to chat.
5. **Learn**: Go to "Learning" tab to start a path and track progress.

Enjoy collaborating with AstraLearn!
