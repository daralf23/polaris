from extra_life.database.tables  import Donations

def test_fullDonation():
    foo = Donations(donation_id=12345, 
                   participant_id=67890, 
                   team_id=56690, 
                   amount=25.00, 
                   display_name='Rod Kimble', 
                   message='Cool Beans')
    
    assert foo.donation_id == 12345
    assert foo.participant_id == 67890
    assert foo.team_id == 56690
    assert foo.amount == 25.00
    assert foo.display_name == 'Rod Kimble'
    assert foo.message == 'Cool Beans'

def test_minimalDonation():
    foo = Donations(donation_id=12345, 
                   participant_id=67890, 
                   team_id=56690)
    
    assert foo.donation_id == 12345
    assert foo.participant_id == 67890
    assert foo.team_id == 56690
    assert foo.amount == 0.00
    assert foo.display_name == 'Anonymous'
    assert foo.message == ''


