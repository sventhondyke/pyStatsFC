pyStatsFC
=========

Light-weight python wrapper around the StatsFC API. 

Follows conventions from [StatsFC API v2.0 Developer page](https://statsfc.com/developers/ "With a Title") with following exceptions:

*Fixtures* and *Results*
------------------------
These are grouped in the **Matches** class. You pass a _type_ argument which can be 'fixtures' or 'results'.
Date arguments are called *date_from* and *date_to* ('from' being reserved in python) and can be passed as python datetime.date objects or strings in yyyy-mm-dd form.

Quick examples
--------------

#### Fixtures

    >>> from pyStatsFC import *
    >>> for reds in Matches('premier-league', 'fixtures', team='Liverpool'):
    ...     print reds
    ...
    status : u'Not started'
    away_id : 8650
    date : u'2013-01-30 20:45:00'
    home : u'Arsenal'
    away : u'Liverpool'
    id : 1229350
    home_id : 9825
    ------ *** ------
    .
    .
    ...

#### Table

    >>> table = Table('premier-league')
    >>> for row in table:
    ...     print row
    info : u'championsleague'
    drawn : 2
    lost : 3
    for : 57
    played : 23
    against : 30
    team_id : 10260
    won : 18
    team : u'Manchester United'
    position : 1
    difference : 27
    points : 56
    ------ *** ------
    info : u'championsleague'
    drawn : 6
    lost : 2
    for : 45
    played : 23
    against : 19
    team_id : 8456
    won : 15
    team : u'Manchester City'
    position : 2
    difference : 26
    points : 51
    ------ *** ------
    info : u'championsleague'
    drawn : 6
    lost : 4
    for : 47
    played : 23
    against : 22
    team_id : 8455
    won : 13
    team : u'Chelsea'
    position : 3
    difference : 25
    points : 45
    ------ *** ------
    .
    .
    ...
    
##### Table position method

    >>> print "In tenth position are", Table('premier-league').position(7).team
    ... In tenth position are Stoke City