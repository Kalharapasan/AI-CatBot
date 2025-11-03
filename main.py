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
        