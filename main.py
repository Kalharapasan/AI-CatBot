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