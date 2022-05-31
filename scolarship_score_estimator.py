# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:38:17 2022

@author: guillaume cosnier
visit : 
    guillaumecosnier.psychoscope.net
    psychoscope.net
    youtube.com/c/lesingequibaille
"""
try : 
    import numpy as np
    import scipy.stats
except : 
    print("Error : Be sure to have installed numpy and scipy to use this program")
    input("Press enter to quit")
    quit()

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
    
    def exportEstimations(self) :
        with open('academicEstimations.txt','w') as f:
            line = 'Mean estimation : '+ str(self.mean)+'\n'+'Standard deviation : '+ str(self.std)+'\n'
            f.write(line)
        with open('academicEstimations.csv','w') as f:
            f.write('#;Mean')
            for i in self.courses :
                line = ';'+i
                f.write(line)
            n = 0
            for i in self.reports :
                f.write('\n')
                n += 1
                line = str(n)+';'+str(i[0])
                f.write(line)
                for u in i[1] :
                    line = ';'+str(i[1][u])
                    f.write(line)
        
def inputCourses(report) :
    courses = []
    print("Enter the name of your courses one after the other, then quit\n")
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
                    print("You have to enter a full or a float number")
            while True :
                b = input("Maximal score expected for the course "+i+' : ')
                try :
                    b = float(b)
                    break
                except :
                    print("You have to enter a full or a float number")
            if a > b :
                print("Minimal score must be inferior or equal to maximal score")
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
                print("You have to enter a full or a float number")
        coursesWeights[i] = a
    report.CoursesWeights(coursesWeights)

def textBoxProgram() :
    A = report()
    inputCourses(A)
    inputSubjectiveEstimations(A)
    inputCoursesWeights(A)
    print("\nProcessing, please wait...")
    A.estimations()
    print("\nMean estimated mean :",A.mean)
    print("Standard deviation of estimated means :",A.std)
    while True :
        a = input("""\nDo you want to export results ?
                  y - Yes
                  n - No
                  Your choice : """)
        if a == 'y' :
            print("\nProcessing, please wait...")
            A.exportEstimations()
            print("\nEstimations exported")
            break
        elif a == 'n' :
            break
        else :
            "\nJust choose between 'y' or 'n'. Easy."
    input("\nPress enter to quit")

textBoxProgram()