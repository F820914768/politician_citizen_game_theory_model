# -*- coding: utf-8 -*-
"""
Created on Mon May  4 01:18:42 2020

@author: 82091
"""
import random
import numpy as np
import matplotlib.pyplot as plt

def generate_ideology():
    x = np.random.normal(0.5, 0.2)
    if x > 1:
        x = 1
    elif x < 0:
        x = 0
    return x

class Politician:
    def __init__(self, country):
        self.country = country
        self.country.add_politician(self)
        
        self.ideology = random.random()
        self.num_vote = 0
        self.poll_result = 0
        
        self.history_poll_result = []
        self.previous_action = random.choice([-1, 1])
    
    def judge(self):
        self.history_poll_result.append(self.poll_result)
        
        if len(self.history_poll_result) == 1:
            action = (random.random() - 0.5) * 1
            self.ideology += action
            self.previous_action = 1 if action >= 0 else -1
            return None
        
        if self.history_poll_result[-2] - self.history_poll_result[-1] < 0:
            action = self.previous_action * (-1) 
            self.ideology += action
            self.previous_action = 1 if action >= 0 else -1        
        else:
            self.ideology += self.previous_action
            
            
    
class Country:
    def __init__(self):
        self.politicians = []
        self.citizens = []
        
    def add_citizen(self, citizen):
        self.citizens.append(citizen)
        
    def add_politician(self, politician):
        self.politicians.append(politician)
        
    def campaign(self):
        for politician in self.politicians:
            politician.num_vote = 0
        
        for citizen in self.citizens:
            citizen.vote()
            
    def public_opinion_poll(self):
        for politician in self.politicians:
            politician.poll_result = 0        

        for citizen in self.citizens:
            citizen.opinion()
            
        for politician in self.politicians:
            politician.judge()


    def hist(self):
        h = []
        for politician in self.politicians:
            h.append(politician.ideology)
        plt.hist(h)

    def hist_citizen(self):
        h = []
        for citizen in self.citizens:
            h.append(citizen.ideology)
        plt.hist(h)       
    
class Citizen:
    def __init__(self, country):
        self.ideology = generate_ideology()
        self.country = country
        self.country.add_citizen(self)
        self.politicians = self.country.politicians
        
        
    def vote(self):
        d = []
        for politician in self.politicians:
            ideology_difference = abs(self.ideology - politician.ideology)
            d.append(ideology_difference)
        
        i = np.argmin(d)
        
        favor_poli = self.politicians[i]
        favor_poli.num_vote += 1
        
    def opinion(self):
        d = []
        for politician in self.politicians:
            ideology_difference = abs(self.ideology - politician.ideology)
            d.append(ideology_difference)
        
        i = np.argmin(d)
        
        favor_poli = self.politicians[i]
        favor_poli.poll_result += 1    
        
    
            
        
if __name__ == '__main__':
    country = Country()
    for i in range(7000):
        Citizen(country)
        
    for i in range(4):
        Politician(country)
        
    for i in range(10):
        country.public_opinion_poll()
        
    country.hist()
    plt.show()
    country.hist_citizen()
        