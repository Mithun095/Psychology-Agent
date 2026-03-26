import { useState, useRef, useEffect } from 'react';

interface Message {
    id: string;
    content: string;
    sender: 'user' | 'agent';
    mood?: string;
    crisisLevel?: string;
    timestamp: Date;
}

export default function Home() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [sessionId, setSessionId] = useState<string | null>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    // Add welcome message on mount
    useEffect(() => {
        setMessages([
            {
                id: 'welcome',
                content: "Hello! 👋 I'm your Psychology Agent, here to listen and support you. Feel free to share what's on your mind. Everything you say here is private and confidential.",
                sender: 'agent',
                timestamp: new Date(),
            },
        ]);
    }, []);

    const sendMessage = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            content: input,
            sender: 'user',
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await fetch('http://localhost:8001/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: input,
                    session_id: sessionId,
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to get response');
            }

            const data = await response.json();

            if (data.session_id && !sessionId) {
                setSessionId(data.session_id);
            }

            const agentMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: data.response,
                sender: 'agent',
                mood: data.mood,
                crisisLevel: data.crisis_level,
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, agentMessage]);
        } catch (error) {
            console.error('Error:', error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: "I'm sorry, I'm having trouble connecting right now. Please try again in a moment.",
                sender: 'agent',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    };

    const getMoodColor = (mood?: string) => {
        switch (mood) {
            case 'happy': return 'bg-green-500';
            case 'sad': return 'bg-blue-500';
            case 'anxious': return 'bg-yellow-500';
            case 'angry': return 'bg-red-500';
            case 'neutral': return 'bg-gray-500';
            default: return 'bg-purple-500';
        }
    };

    return (
        <div className="min-h-screen flex flex-col bg-gradient-to-br from-slate-900 via-purple-900/20 to-slate-900">
            {/* Header */}
            <header className="glass border-b border-white/10 px-6 py-4">
                <div className="max-w-4xl mx-auto flex items-center justify-between">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                            <span className="text-xl">🧠</span>
                        </div>
                        <div>
                            <h1 className="text-xl font-bold gradient-text">Psychology Agent</h1>
                            <p className="text-xs text-slate-400">Your mental health companion</p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2">
                        <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span>
                        <span className="text-sm text-slate-400">Online</span>
                    </div>
                </div>
            </header>

            {/* Chat Container */}
            <main className="flex-1 overflow-hidden flex flex-col max-w-4xl mx-auto w-full">
                {/* Messages */}
                <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
                        >
                            <div
                                className={`max-w-[80%] rounded-2xl px-4 py-3 ${message.sender === 'user'
                                        ? 'bg-gradient-to-br from-indigo-500 to-purple-600 text-white'
                                        : 'glass text-slate-200'
                                    }`}
                            >
                                <p className="text-sm leading-relaxed whitespace-pre-wrap">{message.content}</p>
                                {message.mood && message.sender === 'agent' && (
                                    <div className="mt-2 flex items-center gap-2 text-xs text-slate-400">
                                        <span className={`w-2 h-2 rounded-full ${getMoodColor(message.mood)}`}></span>
                                        <span>Detected mood: {message.mood}</span>
                                    </div>
                                )}
                                <p className="text-xs mt-1 opacity-50">
                                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </p>
                            </div>
                        </div>
                    ))}

                    {/* Typing indicator */}
                    {isLoading && (
                        <div className="flex justify-start animate-fade-in">
                            <div className="glass rounded-2xl px-4 py-3">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                    <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                    <span className="w-2 h-2 rounded-full bg-slate-400 animate-bounce" style={{ animationDelay: '300ms' }}></span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="glass border-t border-white/10 p-4">
                    <div className="flex gap-3 items-end">
                        <div className="flex-1 relative">
                            <textarea
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                onKeyPress={handleKeyPress}
                                placeholder="Share what's on your mind..."
                                className="w-full bg-slate-800/50 border border-slate-700 rounded-xl px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 resize-none"
                                rows={1}
                                disabled={isLoading}
                            />
                        </div>
                        <button
                            onClick={sendMessage}
                            disabled={!input.trim() || isLoading}
                            className="bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed text-white rounded-xl px-6 py-3 font-medium transition-all duration-200 flex items-center gap-2"
                        >
                            <span>Send</span>
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </div>
                    <p className="text-xs text-slate-500 mt-2 text-center">
                        🔒 Your conversation is private and confidential
                    </p>
                </div>
            </main>

            {/* Footer */}
            <footer className="text-center py-3 text-xs text-slate-500">
                <p>💚 Remember: You are not alone. We're here to help.</p>
            </footer>
        </div>
    );
}
