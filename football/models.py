from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
import nfldb

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

    def stats(self, year, phase, week, sort='receiving_yds'):
        db = nfldb.connect()
        query = nfldb.Query(db)

        query.game(season_year=year)
        if phase != 'All':
            query.game(season_type=phase)

            if week != 'All':
                query.game(week=week)

        query.player(player_id=self.player_id)

        return query.sort(sort).as_aggregate()


class UserTeam(models.Model):
    """ User-created fantasy teams """

    team_name = models.CharField(max_length=250, help_text="Enter a name for your team")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = [ "team_name" ]

    def __str__(self):
        return self.team_name

class UserPlayer(models.Model):
    """
    Model to map a player (from nfldb) to a user
    created fantasy team (UserTeam)
    """

    fantasy_team = models.ForeignKey(UserTeam, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    class Meta:
        ordering = [ "fantasy_team", "player" ]

    def __str__(self):
        return '%s (%s)' % (self.player, self.fantasy_team)

class NflDbHelper:
    @staticmethod
    def weeks(phase):
        weeks = []
        if phase != 'All':
            if phase == 'Preseason':
                weeks += ["All", "1", "2", "3", "4"]
            elif phase == 'Regular':
                weeks += ["All", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
            elif phase == 'Postseason':
                weeks += ["All", "1", "2", "3"]
            else:
                raise Http404("Page not found!")

        return weeks

    @staticmethod
    def computePoints(player):
        passing_pts = player.passing_yds / 25.0
        rushing_pts = player.rushing_yds / 10.0
        receive_pts = player.receiving_yds / 10.0

        passing_pts += 4 * player.passing_tds
        rushing_pts += 6 * player.rushing_tds
        receive_pts += 6 * player.receiving_tds

        total_pts = passing_pts + rushing_pts + receive_pts
        ppr_pts = total_pts + player.passing_att + player.rushing_att + player.receiving_rec

        return (total_pts, ppr_pts)

    @staticmethod
    def query(year, phase, week, position, sort):
        db = nfldb.connect()
        query = nfldb.Query(db)

        query.game(season_year=year)

        # Filter on season/week info
        if phase != 'All':
            query.game(season_type=phase)

            if week != 'All':
                query.game(week=week)

        # Filter on position
        query.player(position=position)

        # Get the players and sorting method
        if sort !='fantasy' and sort != 'ppr':
            aggregate_players = query.sort(sort).as_aggregate()
        else:
            aggregate_players = query.as_aggregate()

        # Compute fantasy points
        fantasy = []
        for aggpp in aggregate_players:
            (total_pts, ppr_pts) = NflDbHelper.computePoints(aggpp)
            fantasy.append((aggpp, total_pts, ppr_pts))

        # if fantasy points or ppr points sort request, do that now
        if sort == 'fantasy':
            fantasy.sort(key=lambda tup: tup[1], reverse=True) # Sort on regular rankings
        elif sort == 'ppr':
            fantasy.sort(key=lambda tup: tup[2], reverse=True) # Sort on ppr rankings

        return fantasy

    @staticmethod
    def players(year, players):
        db = nfldb.connect()

        qbs = []
        rbs = []
        wrs = []
        tes = []
        oth = []
        for player in players:
            query = nfldb.Query(db)
            query.game(season_year=year)
            query.player(player_id=player.player_id)
            for aggpp in query.as_aggregate():
                (total_pts, ppr_pts) = NflDbHelper.computePoints(aggpp)

                if aggpp.player.position == nfldb.Enums.player_pos['QB']:
                    qbs.append((aggpp, total_pts, ppr_pts))
                elif aggpp.player.position == nfldb.Enums.player_pos['RB']:
                    rbs.append((aggpp, total_pts, ppr_pts))
                elif aggpp.player.position == nfldb.Enums.player_pos['WR']:
                    wrs.append((aggpp, total_pts, ppr_pts))
                elif aggpp.player.position == nfldb.Enums.player_pos['TE']:
                    tes.append((aggpp, total_pts, ppr_pts))
                else:
                    oth.append((aggpp, total_pts, ppr_pts))

        return (qbs, rbs, wrs, tes, oth)

