import json
import numpy
import time

from . import defaults


class Range:

    def __init__(self, weight, distance):
        self.weight = weight
        self.distance = distance

    @staticmethod
    def from_dict(data):
        return Range(data['weight'], data['distance'])


class EdirpLevelRanges:
    DEFAULT_START_DISTANCE = 0.0
    DEFAULT_MAX_DISTANCE = 300.0
    DEFAULT_STEP_SIZE = 5.0

    def __init__(self, name, ranges):
        self.name = name
        self.ranges = ranges

    # First attempt will replaced by tree search.
    # Could add optional weighting and normalization.
    def create_histogram(self, distances):
        histogram = {}
        for distance in distances:
            for (index, start_distance) in enumerate(self.ranges):
                stop_distance = None
                if index < len(self.ranges) - 1:
                    stop_distance = self.ranges[index + 1]

                if start_distance.distance < distance:
                    if stop_distance is not None and stop_distance.distance < distance:
                        continue
                    histogram[index] = histogram.get(index, 0) + 1
                    break

        sum_of_values = 0.0
        weighted_histogram = {}
        for key, value in histogram.iteritems():
            weighted_value = self.ranges[key].weight * value
            weighted_histogram[key] = weighted_value
            sum_of_values += weighted_value

        normalized_histogram = {key: weighted_value/sum_of_values for key, weighted_value in weighted_histogram.iteritems()}
        return normalized_histogram

    @classmethod
    def create_edirp_level_ranges_interactively(cls):
        edirp_level_ranges_file_path = raw_input('Please enter the path to the json config file containing the EDIRP\n'
                                                 'level ranges. DEFAULT: {path}\n'
                                                 .format(path=defaults.DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH))

        if edirp_level_ranges_file_path == '':
            print '-Using default file path'
            edirp_level_ranges_file_path = defaults.DEFAULT_EDIRP_LEVEL_RANGES_FILE_PATH

        default_name = time.strftime("%Y%m%d-%H%M%S")
        edirp_level_ranges_name = raw_input('Please enter the name of the edirp level range file. DEFAULT: {def_name}\n'
                                            .format(def_name=default_name))

        if edirp_level_ranges_name == '':
            print '-Using default name'
            edirp_level_ranges_name = default_name

        uniform_distances_answer = ''
        while uniform_distances_answer.lower() not in ['y', 'n']:
            uniform_distances_answer = raw_input('Would you like the distances to be uniform? (y/n)\n')

        uniform_distances = uniform_distances_answer == 'y'
        if uniform_distances:
            print 'Generating uniform distances'

            start_dist_input = raw_input('What is the start distance? DEFAULT: {default_start_distance}'
                                         .format(default_start_distance=cls.DEFAULT_START_DISTANCE))

            try:
                start_dist = float(start_dist_input)
            except:
                print 'Could not convert start dist into float, using default'
                start_dist = cls.DEFAULT_START_DISTANCE

            max_dist_input = raw_input('What is the max distance? DEFAULT: {default_max_distance}'
                                       .format(default_max_distance=cls.DEFAULT_MAX_DISTANCE))

            try:
                max_dist = float(max_dist_input)
            except:
                print 'Could not convert max dist into float, using default'
                max_dist = cls.DEFAULT_MAX_DISTANCE

            step_size_input = raw_input('What is the step size? DEFAULT: {default_step_size}'
                                        .format(default_step_size=cls.DEFAULT_STEP_SIZE))
            try:
                step_size = float(step_size_input)
            except:
                print 'Could not convert step size into float, using default'
                step_size = cls.DEFAULT_STEP_SIZE

            number_of_steps = int((max_dist - start_dist) / step_size)
            steps = []
            for step in numpy.linspace(start_dist, max_dist, num=number_of_steps, endpoint=True):
                steps.append({
                    'distance': step,
                    'weight': 1.0,
                })

            with open(edirp_level_ranges_file_path, 'w') as edirp_level_ranges_file:
                json.dump({
                    'name': edirp_level_ranges_name,
                    'ranges': steps
                }, edirp_level_ranges_file)

    @staticmethod
    def from_json(filename):
        with open(filename, 'r') as json_file:
            data = json.load(json_file)
            return EdirpLevelRanges(data['name'], [Range.from_dict(range_dict) for range_dict in data['ranges']])
