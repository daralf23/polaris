from extra_life.database.tables import Teams

def test_newTeam():
    foo = Teams(team_id=56690, 
                discord_guild_id=122333444455555666666,
                reporting_channel=1223334444,
                name= 'The Stunt Team',
                num_participants=4,
                num_donations=12,
                sum_donations=36.00,
                fundraising_goal=50000.00,
                event_id=33333)
    
    assert foo.team_id == 56690
    assert foo.reporting_channel == 1223334444
    assert foo.name == 'The Stunt Team'
    assert foo.num_participants == 4
    assert foo.num_donations == 12
    assert foo.sum_donations == 36.00
    assert foo.fundraising_goal == 50000.00
    assert foo.event_id == 33333

def test_fulTeam():
    foo = Teams(id=1, 
                            team_id=56690, 
                            discord_guild_id=122333444455555666666,
                            reporting_channel=1223334444,
                            name= 'The Stunt Team',
                            num_participants=4,
                            num_donations=12,
                            sum_donations=36.00,
                            fundraising_goal=50000.00,
                            event_id=33333,
                            team_etag='"EC326662160CB68AE7360293FAB1FE00"',
                            participants_etag='"FC326662160CB68AE7360293FAB1FE00"',
                            donations_etag='"GC326662160CB68AE7360293FAB1FE00"')

    assert foo.team_id == 56690
    assert foo.reporting_channel == 1223334444
    assert foo.name == 'The Stunt Team'
    assert foo.num_participants == 4
    assert foo.num_donations == 12
    assert foo.sum_donations == 36.00
    assert foo.fundraising_goal == 50000.00
    assert foo.event_id == 33333
    assert foo.team_etag == '"EC326662160CB68AE7360293FAB1FE00"'
    assert foo.participants_etag == '"FC326662160CB68AE7360293FAB1FE00"'
    assert foo.donations_etag == '"GC326662160CB68AE7360293FAB1FE00"'


