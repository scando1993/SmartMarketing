class Person(object):
    def __init__(self, name=None, job=None, greeting=None, last_seen=None, gender=None):
        self.name = name
        self.job = job
        self.greeting = greeting
        self.lastSeen = last_seen
        self.gender = gender
        print(self)
