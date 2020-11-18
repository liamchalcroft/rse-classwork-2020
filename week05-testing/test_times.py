import times

def test_given_input():
    large = times.time_range("2010-01-12 10:00:00", "2010-01-12 12:00:00")
    short = times.time_range("2010-01-12 10:30:00", "2010-01-12 10:45:00", 2, 60)
    result = times.compute_overlap_time(large, short)
    expected = [('2010-01-12 10:30:00', '2010-01-12 10:37:00'),
                 ('2010-01-12 10:38:00', '2010-01-12 10:45:00')]
    assert result == expected

class ISS_response:
    '''
    This class provides "hardcoded" return values to mock the calls to the online API.
    '''
    @property
    def status_code(self):
        return 200

    def json(self):
        '''
        mocks the bit from the json output we need from querying the API.
        '''
        now = datetime.datetime.now().timestamp()
        return {'message': 'success',
                'request': {'altitude': 10.0, 'datetime': now, 'latitude': 51.5074, 'longitude': -0.1278, 'passes': 5},
                'response': [{'duration': 446, 'risetime': now + 88433},
                             {'duration': 628, 'risetime': now + 94095},
                             {'duration': 656, 'risetime': now + 99871},
                             {'duration': 655, 'risetime': now + 105676},
                             {'duration': 632, 'risetime': now + 111480}]}

def test_iss_passes():
    with mock.patch("requests.get", new=mock.MagicMock(return_value=ISS_response())) as mymock:
        iss_over_London = iss_passes(51.5074, -0.1278)
        mymock.assert_called_with("http://api.open-notify.org/iss-pass.json",
                                  params={
                                      "lat": 51.5074,
                                      "lon": -0.1278,
                                      "n": 5})
        assert len(iss_over_London) == 5
        # Create a range from yesterday to next week whether the overlap ranges are still 5
        yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
        next_week = datetime.datetime.now() + datetime.timedelta(days=7)
        large = time_range(f"{yesterday:%Y-%m-%d %H:%M:%S}", f"{next_week:%Y-%m-%d %H:%M:%S}")
        assert compute_overlap_time(large, iss_over_London) == iss_over_London