# -*- coding: utf-8 -*-
import warnings


class Variation:
    """
    Class handles results provided with A/B test for a particular variation
    """
    def __init__(self, total=None, success=None, data=None, group=None):
        """
        Create Variation instance
        
        :param int total: number of total visitors
        :param int success: number of visitors who clicked the button
        :param iterable data: sequence of visitors actions (1 - clicked, 0 - didn't click)
        :param int group: size of group in data (for Wald tests) 
        """
        self.group = group

        if data is not None:
            try:
                self.data = list(data)
            except:
                raise TypeError('data must be convertible to list')
        else:
            self.data = data

        if data is not None:
            self.total = len(data)
            self.success = sum(data)
        else:
            self.total = total if total else 0.
            self.success = success if success else 0.

        if (self.data is not None) and (set(self.data) != {0, 1}):
            raise Exception('data should contain only 0\'s and 1\'s.')

        if (self.total is not None) and (self.success is not None) and (self.total < self.success):
            raise Exception('Conversion rate > 1')

    def estimate_conversion(self):
        """
        Estimate the sample conversion
        
        :return: conversion 
        """
        try:
            return self.success / self.total
        except:
            raise ZeroDivisionError()

    def copy(self):
        """
        Copy Variation instance
        
        :return: Variation
        """
        return Variation(self.total, self.success, self.data)

    def truncate(self, size):
        """
        Truncate variation data size to proposed if it is less than current one.
        
        :param int size: new size
        :return: variation
        """
        if not self.data:
            raise Exception('Variation has no data inside')
        else:
            return Variation(data=self.data[:1 + min(size, self.total)])

    def generate_sample(self):
        """
        Generate a sample based on total number and number of successes.
        
        :return numpy.array:
        """
        import numpy as np
        mask = np.random.choice(self.total, self.success, replace=False)
        sample = np.zeros(self.total)
        sample[mask] = 1
        return sample


class VariationsCollection:
    """
    Set of variations obtained within A/B test.
    Includes one control variations and several experimental ones.
    """
    def __init__(self, *args):
        """
        Create VariationsCollection instance.
        The first argument is treated as a control variation, the other - as experimental ones.
        If no arguments are provided the empty instance would be created.
        
        :param Variation args:
        """
        self.control = None
        self.treatments = list()

        if len(args):
            self.add_control(args[0])
            if len(args) > 1:
                self.add_treatments(*args[1:])

    def add_control(self, variation):
        """
        Add control variation to the collection.
        If control variation is already present it would be substituted and the warning would be printed to console.
        It's an in-place method.
        
        :param Variation variation: new control variation
        """
        if not isinstance(variation, Variation):
            raise TypeError('Variation object only suits.')
        if self.control:
            warnings.warn('Collection already has a control variation. It would be changed to proposed one.')
        self.control = variation

    def add_treatments(self, *args):
        """
        Add new treatment variations. Treatments are added to the end of experimental variations list.
        It'a an in-place method.
        
        :param Variation args: experimental variations
        """
        if not len(args):
            warnings.warn('Nothing to add')
        else:
            for arg in args:
                if not isinstance(arg, Variation):
                    raise TypeError('Objects of Variation type only suit.')
            self.treatments += list(args)

    def delete_control(self):
        """
        Delete control variation.
        """
        self.control = None

    def delete_treatment(self, n):
        """
        Delete treatment with given number (counting from 1) if it exists.
        It's an in-place method.
        
        :param int n: number of variation to be deleted.
        """
        if n > len(self.treatments):
            warnings.warn('Number of experimental variations is less then proposed number.')
        else:
            del self.treatments[n-1]

    def describe(self):
        """
        Return summary information about collection.
        If collection is empty returns None.
        
        :return pandas.DataFrame:  
        """
        import pandas as pd
        if (self.control is None) and (not len(self.treatments)):
            warnings.warn('The collection is empty.')
            return None
        info_dict = dict()
        if self.control is not None:
            info_dict['Control'] = [self.control.success,
                                    self.control.total,
                                    self.control.estimate_conversion()
                                    ]
        for i, treatment in enumerate(self.treatments, 1):
            info_dict['Treatment_{:d}'.format(i)] = [treatment.success,
                                                     treatment.total,
                                                     treatment.estimate_conversion()
                                                     ]
        info_df = pd.DataFrame(info_dict)
        info_df.index = ['Success', 'Total', 'Conversion_rate']
        return info_df.T
