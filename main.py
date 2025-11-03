import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
import os
from datetime import datetime
import random
import re
from collections import defaultdict

class SelfLearningAI:
    def __init__(self, name):
        self.name = name
        self.knowledge_base = defaultdict(list)
        self.patterns = []
        self.context_memory = []
        self.word_associations = defaultdict(set)
        self.response_scores = defaultdict(int)
        self.conversation_count = 0
        self._initialize_basic_knowledge()
    
    def _initialize_basic_knowledge(self):
        basic_patterns = [
            ("hello|hi|hey|greetings", ["Hello! How can I help you?", "Hi there! What's on your mind?", "Hey! Nice to meet you!"]),
            ("how are you|how do you do|what's up", ["I'm doing great! How about you?", "I'm well, thanks for asking!", "Doing fantastic! How can I assist you?"]),
            ("bye|goodbye|see you|farewell", ["Goodbye! Have a great day!", "See you later!", "Take care!"]),
            ("thank|thanks|appreciate", ["You're welcome!", "Happy to help!", "Anytime!"]),
            ("your name|who are you|what are you", ["I'm a self-learning AI assistant. I learn from our conversations!", "I'm an AI that gets smarter with every chat!"]),
            ("help|assist|support", ["I'm here to help! Just ask me anything and I'll do my best to assist you.", "Sure! What do you need help with?"]),
            ("weather|temperature|climate", ["I don't have real-time weather data, but I can learn about weather patterns if you teach me!", "Tell me about the weather in your area!"]),
            ("joke|funny|humor", ["Why don't scientists trust atoms? Because they make up everything! 😄", "What do you call a bear with no teeth? A gummy bear!"]),
            ("age|old|years", ["I was just created, but I'm learning fast!", "Age is just a number. I measure my growth in conversations!"]),
            ("love|like|enjoy", ["That's great! Tell me more about what you love!", "I'd love to hear more about that!"]),
        ]
        
        for pattern, responses in basic_patterns:
            for response in responses:
                self.patterns.append({
                    'input_pattern': pattern,
                    'response': response,
                    'keywords': pattern.split('|')
                })
    def extract_keywords(self, text):
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 
                     'in', 'with', 'to', 'for', 'of', 'as', 'by', 'this', 'that', 'it'}
        words = re.findall(r'\w+', text.lower())
        keywords = [w for w in words if w not in stop_words and len(w) > 2]
        return keywords if keywords else words
    
    def generate_response(self, user_input, context=[]):
        self.conversation_count += 1
        user_input_lower = user_input.lower()
        
        for pattern_data in self.patterns:
            pattern = pattern_data['input_pattern']
            pattern_parts = pattern.split('|')
            
            if any(part in user_input_lower for part in pattern_parts):
                return random.choice([pattern_data['response']]) if isinstance(pattern_data['response'], str) else pattern_data['response']
        
        keywords = self.extract_keywords(user_input)
        
        if keywords:
            for keyword in keywords[:3]: 
                if keyword in self.knowledge_base and self.knowledge_base[keyword]:
                    responses = self.knowledge_base[keyword]
                    best_response = max(responses, key=lambda x: x.get('score', 0))
                    if best_response['score'] > 0:
                        return best_response['response']
        
        return self.generate_smart_response(user_input, keywords, context)
    
    def generate_smart_response(self, user_input, keywords, context):
        
        if '?' in user_input:
            responses = [
                f"That's an interesting question! Based on what I know, {keywords[0] if keywords else 'this topic'} is quite fascinating. What specifically would you like to know?",
                f"Good question! I'm learning about {keywords[0] if keywords else 'this'}. Can you tell me more details?",
                f"Let me think about that... Regarding {keywords[0] if keywords else 'your question'}, I'd say it depends on the context. What's your take on it?",
            ]
            return random.choice(responses)

        if keywords:
            topic = ' and '.join(keywords[:2]) if len(keywords) > 1 else keywords[0]
            responses = [
                f"Interesting! I'm noting down information about {topic}. This will help me learn.",
                f"Thanks for sharing that about {topic}! I'm learning from this conversation.",
                f"I see you're talking about {topic}. That's useful information!",
                f"Got it! I've learned something new about {topic}. Tell me more!",
                f"That's helpful information about {topic}! I'm storing this in my knowledge base.",
            ]
        else:
            responses = [
                "I understand. Can you elaborate on that?",
                "Interesting! Tell me more.",
                "I'm listening. Please continue.",
                "That's good to know! What else?",
            ]
        
        return random.choice(responses)
    
    def learn_from_conversation(self, user_input, bot_response, user_feedback=None):
        keywords = self.extract_keywords(user_input)
        
        score = 1
        if user_feedback == 'positive':
            score = 3
        elif user_feedback == 'negative':
            score = -1
        
        for keyword in keywords[:5]:  
            self.knowledge_base[keyword].append({
                'response': bot_response,
                'context': user_input,
                'timestamp': datetime.now().isoformat(),
                'score': score
            })
        
        
        words = user_input.lower().split()
        for i, word in enumerate(words):
            if i < len(words) - 1:
                self.word_associations[word].add(words[i + 1])
                
        self.patterns.append({
                'input_pattern': '|'.join(keywords[:3]) if keywords else user_input.lower(),
                'response': bot_response,
                'keywords': keywords
            })
    
    def get_stats(self):
        return {
            'total_patterns': len(self.patterns),
            'keywords_learned': len(self.knowledge_base),
            'associations': sum(len(v) for v in self.word_associations.values()),
            'total_knowledge': sum(len(v) for v in self.knowledge_base.values()),
            'conversations': self.conversation_count
        }
        
class ChatBot(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Self-Learning AI Chatbot")
        self.geometry("1000x700")
        self.configure(bg='#1e1e1e')
        
        self.models = {
            'Neural-1': SelfLearningAI('Neural-1'),
            'Neural-2': SelfLearningAI('Neural-2'),
            'Neural-3': SelfLearningAI('Neural-3'),
            'Adaptive': SelfLearningAI('Adaptive')
        }
        self.current_model = 'Neural-1'
        self.chat_history = []
        self.conversation_context = []
        self.last_user_message = None
        self.last_bot_response = None
        
        self.load_knowledge()
        self.create_widgets()
        self.after(60000, self.auto_save_knowledge)
    
    def create_widgets(self):
        main_frame = tk.Frame(self, bg='#1e1e1e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        control_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        tk.Label(control_frame, text="AI Brain:", bg='#2d2d2d', fg='white', 
                font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5, pady=5)
        self.model_var = tk.StringVar(value=self.current_model)
        model_menu = ttk.Combobox(control_frame, textvariable=self.model_var, 
                                 values=list(self.models.keys()), state='readonly', width=15)
        model_menu.pack(side=tk.LEFT, padx=5)
        model_menu.bind('<<ComboboxSelected>>', self.change_model)
        self.learning_label = tk.Label(control_frame, text="● Learning: ON", 
                                       bg='#2d2d2d', fg='#4CAF50', font=('Arial', 9, 'bold'))
        self.learning_label.pack(side=tk.LEFT, padx=10)
        tk.Button(control_frame, text="📊 Stats", command=self.show_stats, 
                 bg='#4CAF50', fg='white', font=('Arial', 9, 'bold'), 
                 relief=tk.FLAT, padx=8).pack(side=tk.LEFT, padx=3)
        
        tk.Button(control_frame, text="🆕 New", command=self.new_chat, 
                 bg='#FF9800', fg='white', font=('Arial', 9, 'bold'), 
                 relief=tk.FLAT, padx=8).pack(side=tk.LEFT, padx=3)
        
        tk.Button(control_frame, text="💾 Save", command=self.save_chat, 
                 bg='#9C27B0', fg='white', font=('Arial', 9, 'bold'), 
                 relief=tk.FLAT, padx=8).pack(side=tk.LEFT, padx=3)
        
        chat_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.SUNKEN, bd=2)
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, 
                                                     bg='#1e1e1e', fg='#ffffff', 
                                                     font=('Consolas', 10), 
                                                     relief=tk.FLAT, padx=10, pady=10)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        self.chat_display.tag_config('user', foreground='#4CAF50', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config('bot', foreground='#2196F3', font=('Consolas', 10, 'bold'))
        self.chat_display.tag_config('system', foreground='#FF9800', font=('Consolas', 9, 'italic'))
        self.chat_display.tag_config('learn', foreground='#9C27B0', font=('Consolas', 9, 'italic'))
        
        input_frame = tk.Frame(main_frame, bg='#2d2d2d', relief=tk.RAISED, bd=2)
        input_frame.pack(fill=tk.X)
        
        self.input_field = tk.Text(input_frame, height=3, wrap=tk.WORD, 
                                   bg='#1e1e1e', fg='white', 
                                   font=('Arial', 11), relief=tk.FLAT, padx=10, pady=10)
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0), pady=5)
        self.input_field.bind('<Return>', self.send_message)
        self.input_field.focus()
        
        btn_frame = tk.Frame(input_frame, bg='#2d2d2d')
        btn_frame.pack(side=tk.RIGHT, padx=5)
        
        tk.Button(btn_frame, text="👍", command=lambda: self.give_feedback('positive'), 
                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'), 
                 relief=tk.FLAT, width=3).pack(side=tk.TOP, pady=2)
        
        tk.Button(btn_frame, text="👎", command=lambda: self.give_feedback('negative'), 
                 bg='#f44336', fg='white', font=('Arial', 12, 'bold'), 
                 relief=tk.FLAT, width=3).pack(side=tk.TOP, pady=2)
        
        tk.Button(btn_frame, text="Send", command=self.send_message, 
                 bg='#2196F3', fg='white', font=('Arial', 9, 'bold'), 
                 relief=tk.FLAT, width=5, pady=5).pack(side=tk.TOP, pady=2)
        
        self.add_system_message("🤖 Self-Learning AI Chatbot Ready!")
        self.add_system_message("I learn from every conversation. Just start chatting!")
    
    def add_message(self, sender, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == 'user':
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", 'user')
            self.chat_display.insert(tk.END, f"{message}\n\n")
        elif sender == 'bot':
            self.chat_display.insert(tk.END, f"[{timestamp}] AI: ", 'bot')
            self.chat_display.insert(tk.END, f"{message}\n\n")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_system_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[SYSTEM] {message}\n\n", 'system')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def add_learning_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"[LEARNING] {message}\n\n", 'learn')
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def send_message(self, event=None):
        """Send user message"""
        if event and event.keysym == 'Return':
            if event.state & 0x1:
                return
            
        message = self.input_field.get("1.0", tk.END).strip()
        
        if message:
            self.add_message('user', message)
            self.last_user_message = message
            self.input_field.delete("1.0", tk.END)
            self.get_ai_response(message)
        
        if event:
            return 'break'
    
    def get_ai_response(self, user_message):
        try:
            model = self.models[self.current_model]
            response = model.generate_response(user_message, self.conversation_context[-5:])
            self.add_message('bot', response)
            self.last_bot_response = response
            self.chat_history.append({
                'role': 'user', 
                'content': user_message, 
                'timestamp': datetime.now().isoformat()
            })
            self.chat_history.append({
                'role': 'assistant', 
                'content': response, 
                'timestamp': datetime.now().isoformat()
            })
            
            self.conversation_context.append(user_message)
            self.conversation_context.append(response)
            model.learn_from_conversation(user_message, response)
            stats = model.get_stats()
            self.add_learning_message(
                f"✓ Learned! Knowledge: {stats['keywords_learned']} concepts | "
                f"{stats['total_patterns']} patterns | {stats['conversations']} chats"
            )
            
        except Exception as e:
            self.add_system_message(f"Error: {str(e)}")
            print(f"Error in get_ai_response: {e}")
    
    def give_feedback(self, feedback_type):
        if self.last_user_message and self.last_bot_response:
            model = self.models[self.current_model]
            model.learn_from_conversation(self.last_user_message, self.last_bot_response, feedback_type)
            
            if feedback_type == 'positive':
                self.add_learning_message("👍 Great! I'll remember this response works well!")
            else:
                self.add_learning_message("👎 Noted! I'll try to improve next time!")
            
            self.save_knowledge()
        else:
            self.add_system_message("No recent message to rate")
            
    def change_model(self, event=None):
        self.current_model = self.model_var.get()
        stats = self.models[self.current_model].get_stats()
        self.add_system_message(
            f"Switched to {self.current_model} | "
            f"Knowledge: {stats['keywords_learned']} concepts, {stats['conversations']} conversations"
        )
    
    def show_stats(self):
        stats_window = tk.Toplevel(self)
        stats_window.title("AI Learning Statistics")
        stats_window.geometry("600x450")
        stats_window.configure(bg='#1e1e1e')
        
        tk.Label(stats_window, text="🧠 AI Learning Statistics", bg='#1e1e1e', fg='white', 
                font=('Arial', 16, 'bold')).pack(pady=15)
        
        stats_text = scrolledtext.ScrolledText(stats_window, wrap=tk.WORD, 
                                               bg='#2d2d2d', fg='white', 
                                               font=('Consolas', 10))
        stats_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        for model_name, model in self.models.items():
            stats = model.get_stats()
            stats_text.insert(tk.END, f"\n{'='*60}\n")
            stats_text.insert(tk.END, f"  MODEL: {model_name}\n")
            stats_text.insert(tk.END, f"{'='*60}\n\n")
            stats_text.insert(tk.END, f"  📚 Learned Concepts:      {stats['keywords_learned']}\n")
            stats_text.insert(tk.END, f"  🧩 Response Patterns:     {stats['total_patterns']}\n")
            stats_text.insert(tk.END, f"  🔗 Word Associations:     {stats['associations']}\n")
            stats_text.insert(tk.END, f"  💡 Total Knowledge Items: {stats['total_knowledge']}\n")
            stats_text.insert(tk.END, f"  💬 Conversations:         {stats['conversations']}\n\n")
        
        stats_text.config(state=tk.DISABLED)
        
        tk.Button(stats_window, text="Close", command=stats_window.destroy,
                 bg='#f44336', fg='white', font=('Arial', 10, 'bold'),
                 relief=tk.FLAT, padx=20, pady=8).pack(pady=10)
    
    def new_chat(self):
        if messagebox.askyesno("New Chat", "Start new chat? Current conversation will be cleared."):
            self.chat_display.config(state=tk.NORMAL)
            self.chat_display.delete("1.0", tk.END)
            self.chat_display.config(state=tk.DISABLED)
            self.chat_history = []
            self.conversation_context = []
            self.add_system_message("✨ New chat started! I still remember everything I learned.")
    
    def save_chat(self):
        if self.chat_history:
            filename = f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.chat_history, f, indent=2)
            self.add_system_message(f"💾 Chat saved to {filename}")
        else:
            messagebox.showinfo("Save Chat", "No chat history to save")