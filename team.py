class Team:
    def __init__(self, name, wins, ties, losses, GF, GA):
        self.name = name
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.GA = GA
        self.GF = GF
        self.games = wins + losses + ties
        self.points = wins*3 + ties
        self.position = 0
        self.UCL = 0
        self.rel = 0
        self.best = 40
        self.worst = 0
        self.tWins = 0
        self.tLoss = 0
        
    #need to worry about divisions and leagues for US sports
    def __init__(self, name, wins, ties, losses, GF, GA, league, division):
        self.name = name
        self.wins = wins
        self.ties = ties
        self.losses = losses
        self.GA = GA
        self.GF = GF
        self.games = wins + losses + ties
        self.points = wins*3 + ties
        self.position = 0
        self.best = 40
        self.worst = 0
        self.tWins = 0
        self.tLoss = 0  
        self.league = league
        self.division = division
        self.winDiv = 0
        self.WC = 0
        
    def __str__(self):                                          #for printing purposes
        return self.name + " " + str(self.points)
    
    def update(self):                                           #consolidates various cumulative things that need to be updated into one callable thing
        self.games = self.wins + self.losses + self.ties
        self.points = self.wins*3 + self.ties                   #relevant for soccer only
    
    
    
    