from extra_life.database.tables import Participants

def test_teamCaptainParticipant():
    foo = Participants( participant_id=67890, 
                        display_name='Rod Kimble', 
                        team_id=56690, 
                        team_name='The Stunt Team',
                        is_team_captain= True, 
                        event_id=33333,
                        sum_donations=123.45,
                        fundraising_goal=500.00)
    
    assert foo.participant_id == 67890
    assert foo.display_name == 'Rod Kimble'
    assert foo.team_id == 56690
    assert foo.team_name == 'The Stunt Team'
    assert foo.is_team_captain == True
    assert foo.event_id == 33333
    assert foo.sum_donations == 123.45
    assert foo.fundraising_goal == 500.00

def test_nonCaptainParticipant():
    foo = Participants( participant_id=67890, 
                        display_name='Rod Kimble', 
                        team_id=56690, 
                        team_name='The Stunt Team',
                        event_id=33333,
                        sum_donations=123.45,
                        fundraising_goal=500.00)
    
    assert foo.participant_id == 67890
    assert foo.display_name == 'Rod Kimble'
    assert foo.team_id == 56690
    assert foo.team_name == 'The Stunt Team'
    assert foo.is_team_captain == False
    assert foo.event_id == 33333
    assert foo.sum_donations == 123.45
    assert foo.fundraising_goal == 500.00


