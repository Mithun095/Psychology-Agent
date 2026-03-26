---
description: Frontend development workflow for Thushara
---

# 🔵 Thushara's Frontend Development Workflow

Welcome to the Cycology Agent project! This is your workflow guide for frontend development.

## Your Role
You are the **Frontend Developer** responsible for building the user interface of the Cycology Agent mental health support platform.

## Your Directory
You can **ONLY** work in: `frontend/`

---

## 🚀 Getting Started

### Step 1: Clone and Setup Branch
```bash
git clone https://github.com/your-org/cycology-agent.git
cd cycology-agent
git checkout -b feature/frontend
git push -u origin feature/frontend
```

### Step 2: Start with Docker (Recommended)
```bash
# From project root
cp .env.example .env
docker-compose up --build

# Frontend will be at http://localhost:3000
# Changes in frontend/ auto-reload!
```

### Alternative: Run Frontend Only
```bash
cd frontend
npm install
npm run dev
```

---

## 📋 Your Tasks

### Phase 1: Setup & Core UI
- [ ] Initialize Next.js project with TypeScript
- [ ] Setup Tailwind CSS with calming color theme
- [ ] Create layout components (Navbar, Footer, Sidebar)
- [ ] Build the landing page with NGO messaging

### Phase 2: Chat Interface
- [ ] Build ChatContainer component
- [ ] Create MessageBubble component (user & AI messages)
- [ ] Build ChatInput component with send button
- [ ] Add typing indicator animation
- [ ] Implement message history display

### Phase 3: User Features
- [ ] Create anonymous login page
- [ ] Build user profile component
- [ ] Create mood tracking UI
- [ ] Build appointment booking interface

### Phase 4: Professional Features
- [ ] Create psychologist dashboard layout
- [ ] Build video call interface component
- [ ] Create appointment calendar view

---

## 🎨 Design Guidelines

### Color Palette (Calming & Supportive)
```css
/* Use these colors for a calming mental health theme */
--primary: #4F9D9D;      /* Teal - Trust & Calm */
--secondary: #7BC9C9;    /* Light Teal */
--accent: #E8B86D;       /* Warm Gold - Hope */
--background: #F5F9F9;   /* Soft White */
--text: #2D3436;         /* Soft Black */
--success: #6BCB77;      /* Green - Positive */
--warning: #FFD93D;      /* Yellow - Attention */
--error: #FF6B6B;        /* Soft Red - Crisis */
```

### Typography
- Headings: `Inter` or `Outfit`
- Body: `Inter` or `Open Sans`
- Keep it readable and friendly

### UI Principles
- Soft, rounded corners
- Gentle shadows
- Smooth animations
- Mobile-first approach
- Accessibility (WCAG 2.1)

---

## 🤖 Antigravity Prompt

Copy and paste this prompt into Antigravity to get started:

```
I am Thushara, the Frontend Developer for the Cycology Agent project.

This is an AI-powered mental health support platform (NGO initiative) that provides:
- Empathetic AI chatbot for people feeling lonely/depressed
- Anonymous & private conversations
- Connection to real psychologists when needed
- Video/voice call capabilities

My responsibility is building the frontend in the `frontend/` directory using:
- Next.js 14 with TypeScript
- Tailwind CSS
- Socket.io client for real-time chat

IMPORTANT: I can ONLY edit files in the `frontend/` directory. Never touch other directories.

My current priority tasks:
1. Initialize the Next.js project with TypeScript and Tailwind
2. Create a calming, supportive UI theme (teal/green colors)
3. Build the main chat interface components
4. Create the landing page explaining our NGO mission

Please help me start by setting up the project structure and creating the base components.
```

---

## 🔄 Git Workflow

```bash
# Before starting work each day:
git checkout main
git pull origin main
git checkout feature/frontend
git merge main

# After making changes:
git add .
git commit -m "feat: description"
git push origin feature/frontend

# Create PR when ready for review
```

---

## ❓ Questions?
Contact Myth (Project Lead) for any architectural decisions or questions.
