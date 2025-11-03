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