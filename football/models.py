from django.db import models
from collections import defaultdict

class Team(models.Model):
    # Model Fields
    team_id = models.CharField(primary_key=True, max_length=3)
    city = models.CharField(max_length=50)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = [ "team_id" ]
        db_table = "team"

    def __str__(self):
        return '%s %s' % (self.city, self.name)

    def get_qbs(self):
        return self.player_set.filter(position__exact='QB')

    def get_players(self):
        players = []
        players.append(self.player_set.filter(position__exact='QB'))
        players.append(self.player_set.filter(position__exact='RB'))
        players.append(self.player_set.filter(position__exact='WR'))
        players.append(self.player_set.filter(position__exact='TE'))
        players.append(self.player_set.filter(position__exact='K'))
        players.append(self.player_set.filter(position__exact='C'))
        players.append(self.player_set.filter(position__exact='CB'))
        players.append(self.player_set.filter(position__exact='DB'))
        players.append(self.player_set.filter(position__exact='DE'))
        players.append(self.player_set.filter(position__exact='DL'))
        players.append(self.player_set.filter(position__exact='FB'))
        players.append(self.player_set.filter(position__exact='FS'))
        players.append(self.player_set.filter(position__exact='G'))
        players.append(self.player_set.filter(position__exact='ILB'))
        players.append(self.player_set.filter(position__exact='LB'))
        players.append(self.player_set.filter(position__exact='LS'))
        players.append(self.player_set.filter(position__exact='MLB'))
        players.append(self.player_set.filter(position__exact='NT'))
        players.append(self.player_set.filter(position__exact='OG'))
        players.append(self.player_set.filter(position__exact='OL'))
        players.append(self.player_set.filter(position__exact='OLB'))
        players.append(self.player_set.filter(position__exact='OT'))
        players.append(self.player_set.filter(position__exact='P'))
        players.append(self.player_set.filter(position__exact='SAF'))
        players.append(self.player_set.filter(position__exact='SS'))
        players.append(self.player_set.filter(position__exact='T'))
        players.append(self.player_set.filter(position__exact='UNK'))

        return players

class Player(models.Model):

    # Define Enums
    PlayerPos = (
            ('C', 'Center'),
            ('CB', 'Cornerback'),
            ('DB', 'Defensive Back'),
            ('DE', 'Defensive End'),
            ('DL', 'Defensive Lineman'),
            ('FB', 'Fullback'),
            ('FS', 'Free Safety'),
            ('G', 'Guard'),
            ('ILB', 'Inside Linebacker'),
            ('K', 'Kicker'),
            ('LB', 'Linebacker'),
            ('LS', 'Long Snapper'),
            ('MLB', 'MIddle Linebacker'),
            ('NT', 'Nose Tackle'),
            ('OG', 'Outside Guard'),
            ('OL', 'Offensive Lineman'),
            ('OLB', 'Outside Linebacker'),
            ('OT', 'Offensive Tackle'),
            ('P', 'Punter'),
            ('QB', 'Quarterback'),
            ('RB', 'Runningback'),
            ('SAF', 'SAF'),
            ('SS', 'Strong Safety'),
            ('T', 'Tackle'),
            ('TE', 'Tight End'),
            ('WR', 'Wide Receiver'),
            ('UNK', 'Unknown'),
    )

    PlayerStatus = (
            ('Active', 'Active'),
            ('InjuredReserve', 'Injured Reserve'),
            ('NonFootballInjury', 'Non-football Injury'),
            ('Suspended', 'Suspended'),
            ('PUP', 'PUP'),
            ('UnsignedDraftPick', 'Unsigned Draft Pick'),
            ('Exempt', 'Exempt'),
            ('Unknown', 'Unknown'),
    )

    # Model Fields
    player_id = models.CharField(primary_key=True, max_length=10)
    gsis_name = models.CharField(max_length=75, null=True, db_index=True)
    full_name = models.CharField(max_length=100, null=True, db_index=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    team = models.ForeignKey(Team, on_delete=models.PROTECT, db_column="team")
    position = models.CharField(max_length=3, choices=PlayerPos)
    profile_id = models.IntegerField(null=True)
    profile_url = models.CharField(max_length=255, null=True)
    uniform_number = models.SmallIntegerField(null=True)
    birthdate = models.CharField(max_length=75, null=True)
    college = models.CharField(max_length=255, null=True)
    height = models.SmallIntegerField(null=True)
    weight = models.SmallIntegerField(null=True)
    years_pro = models.SmallIntegerField(null=True)
    status = models.CharField(max_length=18, choices=PlayerStatus)

    class Meta:
        ordering = [ "position", "last_name", "first_name" ]
        db_table = "player"

    def __str__(self):
        return '%s, %s' % (self.last_name, self.first_name)


