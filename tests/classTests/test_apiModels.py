from extra_life.donordrive.apiModels import *
import pytest
import aiohttp
from aioresponses import aioresponses


# ### 
# fetch_donorDrive Test Cases
# ###

@pytest.mark.asyncio
async def test_fetch_donorDrive_200():  #Fix
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testEndPoint = f'teams/{testTeamID}'
        testStatus = 200
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=testStatus, 
                   payload={"numParticipants":6, "fundraisingGoal":10000.00, "eventName":"OMIT",
                            "links":"OMIT","hasActivityTracking":False, "captainDisplayName":"Gary Mayden",
                            "hasTeamOnlyDonations":False, "isCustomAvatarImage":True,"eventID":553,
                            "sumDonations":1834.89, "createdDateUTC":"2023-01-02T16:25:33.560+0000",
                            "sourceTeamID":63399, "name":"Paper HandGrenades","avatarImageURL":"OMIT",
                            "teamID":63399,"sumPledges":0.00,"numDonations":79}, 
                   headers={"ETag": '"newMockFetchETag"'})
        
        eTag, jsonData, message = await fetch_donorDrive(testEndPoint, testETag)

        assert message == 'Success - 200'
        assert eTag == '"newMockFetchETag"'
        assert jsonData == {"numParticipants":6, "fundraisingGoal":10000.00, "eventName":"OMIT",
                            "links":"OMIT","hasActivityTracking":False, "captainDisplayName":"Gary Mayden",
                            "hasTeamOnlyDonations":False, "isCustomAvatarImage":True,"eventID":553,
                            "sumDonations":1834.89, "createdDateUTC":"2023-01-02T16:25:33.560+0000",
                            "sourceTeamID":63399, "name":"Paper HandGrenades","avatarImageURL":"OMIT",
                            "teamID":63399,"sumPledges":0.00,"numDonations":79}


@pytest.mark.asyncio
async def test_fetch_donorDrive_304():
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testEndPoint = f'teams/{testTeamID}'
        testStatus = 304
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=testStatus, payload={"mock": "mootData"}, 
                   headers={"ETag": '"newMockFetchETag"'})
        
        eTag, jsonData, message = await fetch_donorDrive(testEndPoint, testETag)
        
        assert message == 'Success - 304, nothing to do'
        assert eTag == None
        assert jsonData == None


@pytest.mark.asyncio
async def test_fetch_donorDrive_other():
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testEndPoint = f'teams/{testTeamID}'
        testStatus = 429
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=testStatus, payload={"mock": "mootData"}, 
                   headers={"ETag": '"mootETag"'})
        
        eTag, jsonData, message = await fetch_donorDrive(testEndPoint, testETag)
        
        assert message == 'Error - 429, too many requests'
        assert eTag == None
        assert jsonData == None


@pytest.mark.asyncio
async def test_fetch_donorDrive_other():
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testEndPoint = f'teams/{testTeamID}'
        testStatus = 504
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=testStatus, payload={"mock": "mootData"}, 
                   headers={"ETag": '"mootETag"'})
        
        eTag, jsonData, message = await fetch_donorDrive(testEndPoint, testETag)
        
        assert message == 'Error - 504 received. Please be advised.'
        assert eTag == None
        assert jsonData == None


# ### 
# fetch_teamInfo Test Cases
# ###

@pytest.mark.asyncio
async def test_fetch_teamInfo():
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testEndPoint = f'teams/{testTeamID}'
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=200, 
                   payload={"numParticipants":6, "fundraisingGoal":10000.00, "eventName":"OMIT",
                            "links":"OMIT","hasActivityTracking":False, "captainDisplayName":"Gary Mayden",
                            "hasTeamOnlyDonations":False, "isCustomAvatarImage":True,"eventID":553,
                            "sumDonations":1834.89, "createdDateUTC":"2023-01-02T16:25:33.560+0000",
                            "sourceTeamID":63399, "name":"Paper HandGrenades","avatarImageURL":"OMIT",
                            "teamID":63399,"sumPledges":0.00,"numDonations":79}, 
                   headers={"ETag": '"newMockFetchETag"'})
        
        eTag, jsonData, message = await fetch_teamInfo(testTeamID, testETag)
        
        assert message == 'Success - 200'
        assert eTag == '"newMockFetchETag"'
        assert jsonData == {"numParticipants":6, "fundraisingGoal":10000.00, "eventName":"OMIT",
                            "links":"OMIT","hasActivityTracking":False, "captainDisplayName":"Gary Mayden",
                            "hasTeamOnlyDonations":False, "isCustomAvatarImage":True,"eventID":553,
                            "sumDonations":1834.89, "createdDateUTC":"2023-01-02T16:25:33.560+0000",
                            "sourceTeamID":63399, "name":"Paper HandGrenades","avatarImageURL":"OMIT",
                            "teamID":63399,"sumPledges":0.00,"numDonations":79}


# ### 
# fetch_participants Test Cases
# ###

@pytest.mark.asyncio
async def test_fetch_participants():
    with aioresponses() as mocked:
        testETag = '"origMockFetchETag"'
        testTeamID = 1234
        testQueryString = "orderBy=displayName%20ASC"
        testEndPoint = f'teams/{testTeamID}/participants?{testQueryString}'
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=200, 
                   payload=[{"fundraisingGoal":1500.00,"eventName":"Extra Life 2023","links":{"donate":"OMIT",
                            "stream":"OMIT","page":"OMIT","facebookFundraiser":"OMIT"},"hasActivityTracking":False,
                            "role":"T","isTeamCoCaptain":False,"participantID":510212,"teamName":"Paper HandGrenades",
                            "streamIsLive":False,"numIncentives":0,"streamingPlatform":"Twitch",
                            "isCustomAvatarImage":True,"displayName":"Donnie Mayden","sumDonations":579.49,
                            "eventID":553,"createdDateUTC":"2023-01-10T20:29:48.387+0000","numMilestones":4,
                            "participantTypeCode":"P","avatarImageURL":"OMIT","teamID":63399,"isTeamCaptain":False,
                            "streamIsEnabled":True,"sumPledges":0.00,"streamingChannel":"Warhaven51","numDonations":28},
                            {"fundraisingGoal":2500.00,"eventName":"Extra Life 2023","links":{"donate":"OMIT",
                            "stream":"OMIT","page":"OMIT"},"hasActivityTracking":False,"role":"C",
                            "isTeamCoCaptain":False,"participantID":508967,"teamName":"Paper HandGrenades",
                            "streamIsLive":False,"numIncentives":0,"streamingPlatform":"Twitch",
                            "isCustomAvatarImage":True,"displayName":"Gary Mayden","sumDonations":285.00,
                            "eventID":553,"createdDateUTC":"2023-01-02T16:25:33.560+0000","numMilestones":4,
                            "participantTypeCode":"P","avatarImageURL":"OMIT","teamID":63399,
                            "isTeamCaptain":True,"streamIsEnabled":True,"sumPledges":0.00,
                            "streamingChannel":"gizzzary","numDonations":16}], 
                   headers={"ETag": '"newMockFetchETag"'})
        
        eTag, jsonData, message = await fetch_participants(testTeamID, testETag)
        
        assert message == 'Success - 200'
        assert eTag == '"newMockFetchETag"'
        assert jsonData == [{"fundraisingGoal":1500.00,"eventName":"Extra Life 2023","links":{"donate":"OMIT",
                            "stream":"OMIT","page":"OMIT","facebookFundraiser":"OMIT"},"hasActivityTracking":False,
                            "role":"T","isTeamCoCaptain":False,"participantID":510212,"teamName":"Paper HandGrenades",
                            "streamIsLive":False,"numIncentives":0,"streamingPlatform":"Twitch",
                            "isCustomAvatarImage":True,"displayName":"Donnie Mayden","sumDonations":579.49,
                            "eventID":553,"createdDateUTC":"2023-01-10T20:29:48.387+0000","numMilestones":4,
                            "participantTypeCode":"P","avatarImageURL":"OMIT","teamID":63399,"isTeamCaptain":False,
                            "streamIsEnabled":True,"sumPledges":0.00,"streamingChannel":"Warhaven51","numDonations":28},
                            {"fundraisingGoal":2500.00,"eventName":"Extra Life 2023","links":{"donate":"OMIT",
                            "stream":"OMIT","page":"OMIT"},"hasActivityTracking":False,"role":"C",
                            "isTeamCoCaptain":False,"participantID":508967,"teamName":"Paper HandGrenades",
                            "streamIsLive":False,"numIncentives":0,"streamingPlatform":"Twitch",
                            "isCustomAvatarImage":True,"displayName":"Gary Mayden","sumDonations":285.00,
                            "eventID":553,"createdDateUTC":"2023-01-02T16:25:33.560+0000","numMilestones":4,
                            "participantTypeCode":"P","avatarImageURL":"OMIT","teamID":63399,
                            "isTeamCaptain":True,"streamIsEnabled":True,"sumPledges":0.00,
                            "streamingChannel":"gizzzary","numDonations":16}]


# ### 
# fetch_recentDonations Test Cases
# ###

@pytest.mark.asyncio
async def test_fetch_recentDonations():
    with aioresponses() as mocked:
        testTeamID = 1234
        testDonationCount = 2
        testQueryString = f"orderBy=createdDateUTC%20DESC&limit={testDonationCount}"
        testEndPoint = f'teams/{testTeamID}/donations?{testQueryString}'
        mocked.get('https://www.extra-life.org/api/'+testEndPoint, 
                   status=200, 
                   payload=[{"displayName":"Gary Mayden","donorID":"A16F82F3FFDF0C64","links":{"recipient":"OMIT",
                            "donate":"OMIT"},"eventID":553,"isRegFee":False,
                            "createdDateUTC":"2023-08-22T11:21:33.640+0000","recipientName":"Donnie Mayden",
                            "recipientImageURL":"OMIT","message":"This is your new Twitch sub - for the kids",
                            "participantID":510212,"amount":5.00,"avatarImageURL":"OMIT","teamID":63399,
                            "donationID":"A4056C34E9B9F7ED"},{"displayName":"Gary Mayden","donorID":"A16F82F3FFDF0C64",
                            "links":{"recipient":"OMIT","donate":"OMIT"},"eventID":553,"isRegFee":False,
                            "createdDateUTC":"2023-08-22T11:21:29.837+0000","recipientName":"Nick North",
                            "recipientImageURL":"OMIT","message":"This is your new Twitch sub - for the kids",
                            "participantID":512196,"amount":5.00,"avatarImageURL":"OMIT","teamID":63399,
                            "donationID":"99147262E89D4F69"}], 
                   headers={"ETag": '"newMockFetchETag"'})
        
        eTag, jsonData, message = await fetch_recentDonations(testTeamID, testDonationCount)
        
        assert message == 'Success - 200'
        assert eTag == '"newMockFetchETag"'
        assert jsonData == [{"displayName":"Gary Mayden","donorID":"A16F82F3FFDF0C64","links":{"recipient":"OMIT",
                            "donate":"OMIT"},"eventID":553,"isRegFee":False,
                            "createdDateUTC":"2023-08-22T11:21:33.640+0000","recipientName":"Donnie Mayden",
                            "recipientImageURL":"OMIT","message":"This is your new Twitch sub - for the kids",
                            "participantID":510212,"amount":5.00,"avatarImageURL":"OMIT","teamID":63399,
                            "donationID":"A4056C34E9B9F7ED"},{"displayName":"Gary Mayden","donorID":"A16F82F3FFDF0C64",
                            "links":{"recipient":"OMIT","donate":"OMIT"},"eventID":553,"isRegFee":False,
                            "createdDateUTC":"2023-08-22T11:21:29.837+0000","recipientName":"Nick North",
                            "recipientImageURL":"OMIT","message":"This is your new Twitch sub - for the kids",
                            "participantID":512196,"amount":5.00,"avatarImageURL":"OMIT","teamID":63399,
                            "donationID":"99147262E89D4F69"}]