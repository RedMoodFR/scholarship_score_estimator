# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:38:17 2022

@author: guill
"""
import numpy as np
import scipy.stats

def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h

class report :
    def Courses(self, courses) :
        self.courses = courses
    
    def SubjectiveEstimation(self, subjectiveEstimators) :
        self.subjectiveEstimators = subjectiveEstimators
    
    def CoursesWeights(self, coursesWeights) :
        self.coursesWeights = coursesWeights
        sumWeights = 0
        for i in coursesWeights :
            sumWeights += coursesWeights[i]
        self.sumWeights = sumWeights
    
    def estimations(self, display = False) :
        coursesDistributions = {}
        means = []
        reports = []
        k = []
        kmax = []
        for i in self.courses :
            k.append(0)
            a = self.subjectiveEstimators[i][0]
            b = self.subjectiveEstimators[i][1]
            coursesDistributions[i] = []
            while a < b :
                coursesDistributions[i].append(a)
                a += 1
            coursesDistributions[i].append(b)
            kmax.append(len(coursesDistributions[i])-1)
        
        while k != kmax :
            h = 1
            report = {}
            dist = []
            for i in range(len(k)) :
                report[self.courses[i]] = coursesDistributions[self.courses[i]][k[i]]
                dist.append(coursesDistributions[self.courses[i]][k[i]] * self.coursesWeights[self.courses[i]])
            mean = np.sum(dist)/self.sumWeights
            means.append(mean)
            reports.append((mean,report))
            if display == True :
                print(mean,'\n',report)
            
            if k[-1] != kmax[-1] :
                k[-1] += 1
                continue
            
            while k[-h] == kmax[-h] :
                h += 1
            k[-h] += 1
            for i in range(h-1) :
                k[-(h-1-i)] = 0
                
        report = {}
        dist = []
        for i in range(len(k)) :
            report[self.courses[i]] = coursesDistributions[self.courses[i]][k[i]]
            dist.append(coursesDistributions[self.courses[i]][k[i]] * self.coursesWeights[self.courses[i]])
        mean = np.mean(dist)
        means.append(mean)
        reports.append((mean,report))
        
        self.reports = reports
        self.means = means
        self.mean = np.mean(means)
        self.std = np.std(means)
        self.confidenceInterval =  mean_confidence_interval(means, confidence=0.95)
        
def inputCourses(report) :
    courses = []
    while True :
        a = input("Enter the name of your Course, or 'q' to quit : ")
        if a == "q" : 
            break
        else :
            courses.append(a)
    report.Courses(courses)

def inputSubjectiveEstimations(report) :
    subjectiveEstimators = {}
    for i in report.courses :
        while True :
            while True :
                a = input("Minimal score expected for the course "+i+' : ')
                try :
                    a = float(a)
                    break
                except :
                    print("You have to enter a full or float number")
            while True :
                b = input("Maximal score expected for the course "+i+' : ')
                try :
                    b = float(b)
                    break
                except :
                    print("You have to enter a full or float number")
            if a > b :
                print("Minimal score must be inferior or equal to maximum score")
                continue
            else :
                break
        subjectiveEstimators[i] = (a,b)
    report.SubjectiveEstimation(subjectiveEstimators)

def inputCoursesWeights(report) :
    coursesWeights = {}
    for i in report.courses :
        while True :
            a = input("Weight of the course "+i+' : ')
            try :
                a = float(a)
                break
            except :
                print("You have to enter a full or float number")
        coursesWeights[i] = a
    report.CoursesWeights(coursesWeights)