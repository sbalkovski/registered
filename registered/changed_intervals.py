"""
CLI tool to compare the stops between two ratings.
"""

import argparse
from collections import defaultdict
from pyproj import Geod
from registered.parser import Pattern, PatternStop, PatternRevenueType
from registered.rating import Rating
from registered.db import geo_node

GEOD = Geod(ellps="WGS84")

def get_intervals_from_stops(rating, stops):
    """
    Given a Rating, return a dictionary mapping stop IDs to the intervals and routes that it's included on.
    """
    this_route = None
    from_stop = None
    from_stop_name = None
    interval_pairs = defaultdict(set)
    intervals = set()
    all_stops = {stop.stop_id: stop for stop in rating["nde"]}
    num_interval_pairs = 0
    for record in rating["pat"]:
        if isinstance(record, Pattern):
            if (record.revenue_type == PatternRevenueType.REVENUE):
                this_route = record.route_id + " " +record.direction_name
            else: this_route = None
            from_stop = None
            from_stop_name = None
            continue
        if isinstance(record, PatternStop):
            to_stop = record.stop_id
            to_stop_name = all_stops[to_stop].name
            if this_route is not None and from_stop is not None and (to_stop in stops or from_stop in stops):
                this_interval = sorted([to_stop, from_stop])
                this_interval = (this_interval[0], this_interval[1])
                num_interval_pairs += 1
                if this_interval not in intervals:
                    interval_pairs[(from_stop, to_stop, from_stop_name, to_stop_name)] = this_route
                    intervals.add(this_interval)
            from_stop = to_stop
            from_stop_name = to_stop_name
    by_route = sorted(interval_pairs.items(), key=lambda x: x[1])
    print(num_interval_pairs)
    return by_route

def main(args):
    """
    Entrypoint for the CLI tool.
    """
    current_rating = Rating(args.CURRENT)
    next_rating = Rating(args.NEXT)
    # print(by_stop)
    changed_intervals = defaultdict(set)

    current_rating_stops = {stop.stop_id: stop for stop in current_rating["nde"]}
    current_rating_stop_ids = set(current_rating_stops)

    next_rating_stops = {stop.stop_id: stop for stop in next_rating["nde"]}
    next_rating_stop_ids = set(next_rating_stops)

    new_stop_ids = next_rating_stop_ids - current_rating_stop_ids
    # output(next_rating_stops, new_stop_ids, by_stop, "newStops")

    shared_stop_ids = next_rating_stop_ids & current_rating_stop_ids
    same_names = {
        stop_id
        for stop_id in shared_stop_ids
        if current_rating_stops[stop_id].name == next_rating_stops[stop_id].name
    }
    same_locations = {
        stop_id
        for stop_id in shared_stop_ids
        if (
            current_rating_stops[stop_id].easting_ft,
            current_rating_stops[stop_id].northing_ft,
        )
        == (
            next_rating_stops[stop_id].easting_ft,
            next_rating_stops[stop_id].northing_ft,
        )
    }

    changed_stops = next_rating_stop_ids - same_locations
    by_route = get_intervals_from_stops(next_rating, changed_stops)
    for ((from_stop, to_stop, from_stop_name, to_stop_name), route_direction) in by_route:
        print(
            f"{route_direction},{from_stop},{from_stop_name},{to_stop},{to_stop_name}"
        )



parser = argparse.ArgumentParser(
    description="Compare two ratings to find new/modified stops."
)
parser.add_argument(
    "CURRENT", help="The Combine directory where the current rating files live"
)
parser.add_argument(
    "NEXT", help="The Combine directory where the next rating files live"
)

if __name__ == "__main__":
    import sys

    sys.exit(main(parser.parse_args()))
