import pytest
from registered import stop_intervals
from registered.rating import Rating

next_rating = next_rating = Rating(r"D:\Ratings\Winter12142025\Combine")

def test_one_stop_multiple_routes():
    different_stop_locations = {'522'}
    expected_intervals = set([('520', '522'),
                          ('522', '10522')]) 

    by_route = stop_intervals.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()
    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 2
    assert intervals == expected_intervals

def test_multiple_stops_one_route():
    different_stop_locations = {'5642', '5640'}
    expected_intervals = set([('5640', '5642'),
                        ('5638', '5640'),
                        ('5642', '5643'),
                        ('5640', '5566')])
    
    by_route = stop_intervals.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()

    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 4
    assert intervals == expected_intervals

def test_stop_intervals():
    different_stop_locations = {'522', '5642', '5640', '5887', '1049'}
    expected_intervals = set([('5640', '5642'),
                        ('5638', '5640'),
                        ('5642', '5643'),
                        ('5640', '5566'),
                        ('520', '522'),
                        ('522', '10522'),
                        ('5886', '5887'),
                        ('5887', '5888'),
                        ('1046', '1049'),
                        ('1049', '1589')])
    
    by_route = stop_intervals.get_intervals_from_stops(next_rating, different_stop_locations)
    intervals = set()

    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        intervals.add((from_stop, to_stop))

    assert len(by_route) == 10
    assert intervals == expected_intervals

