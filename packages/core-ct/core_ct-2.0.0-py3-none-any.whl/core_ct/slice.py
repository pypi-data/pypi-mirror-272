"""A class that abstracts a 2D slice of a `Core`."""
from __future__ import annotations
import numpy as np
from typing import Callable, Tuple


class Slice:
    """
    Abstracts properties of a core slice and contains methods for manipulating it.

    Attributes
    ----------
    data : np.ndarray
        2D numpy array of pixel data that make up the slice

    pixel_dimensions : tuple[float, float]
        Tuple containing the dimensions of each pixel as (width, height) in mm

    thickness : float
        Thickness of the slice in mm
    """

    def __init__(self, data: np.ndarray, 
                 pixel_dimensions: tuple[float, float],
                 thickness: float = 0.0):
        """
        Construct necessary attributes of a core slice.

        Arguments
        ---------
        data : np.ndarray
            2D numpy array of pixel data that make up the slice

        pixel_dimensions : tuple[float, float]
            Tuple containing the dimensions of each pixel as (width, height) in mm

        thickness : float
            Thickness of the slice in mm
        """
        self.data: np.ndarray = data
        self.pixel_dimensions: tuple[float, float] = pixel_dimensions
        self.thickness = thickness

    def __getitem__(self, index: slice | int | Tuple[slice | int, ...]) -> Slice:
        """
        Overloads the bracket operator (`[]`) to support numpy-like indexing behavior.

        Arguments
        ---------
        index : `slice`, `int`, or `tuple` of `slice` and/or `int`
            Index to use for the slicing operation. Can be a single slice, integer, or a
            tuple containing a combination of slices and integers (up to 2 items total).

        Returns
        -------
        Slice
            a new Slice containing the data specified via the index

        Raises
        ------
        IndexError
            If any provided indices are out of range or the end index comes before the
            start index on an axis.
        ValueError
            If the provided index would result in a data shape other than 2D.
            If the provided index specifies more than 2 axes.
            If a step other than 1 is defined on any axis.

        Examples
        --------
            Trim 25 pixels off both ends of the x-axis::

                trimmed = slice[25:-25]
        
            Get a Slice containing only 100th-500th pixels along the x-axis::
            
                trimmed = slice[100:500]
        
            Trim 50 pixels off the start of the y-axis::

                trimmed = slice[:, 50:]
        
            Trim 50 pixels off the end of the y-axis::
            
                trimmed = slice[:, :-50]
        
            Trim 30 pixels from all sides::
            
                trimmed = slice[30:-30, 30:-30]
        """
        # standardize inputs to a tuple, this reduces duplicated code
        if type(index).__name__ != "tuple":
            # trailing comma is necessary to correctly convert to tuple
            index = (index,)

        # make sure no more than 2 dimensions are indexed
        if len(index) > 2:
            raise ValueError(
                f"No more than 2 axes can be specified, found {len(index)}."
            )

        # replace None values with empty slice
        new_index = list(index)
        for i, idx in enumerate(new_index):
            if idx is None:
                new_index[i] = slice(None)
        index = tuple(new_index)

        # validate inputs
        for i, idx in enumerate(index):
            axis_size = self.data.shape[i]

            if isinstance(idx, int):
                if idx >= axis_size:
                    raise IndexError(
                        f"Index ({idx}) out of range on axis {i}. Axis size is "
                        f"{axis_size}."
                    )
                if idx < 0 and idx + axis_size >= axis_size:
                    raise IndexError(
                        f"Index ({idx + axis_size}, calculated from provided "
                        f"index {idx}) out of range on axis {i}. Axis size is "
                        f"{axis_size}."
                    )
                # no further processing needed for integers, skip to next iteration
                continue

            # if we reach this point, idx must be a slice
            start = idx.start
            stop = idx.stop
            
            # make sure there's no step in the slice
            if idx.step is not None and idx.step != 1:
                raise ValueError(
                    f"Error on axis {i}: using a step in the index is not supported."
                )

            # empty slices are always valid (happens when the user provides only `:`)
            # None values mean that the user didn't specify them
            if start is None and stop is None:
                continue
            
            # make sure indices are in range
            if start is not None and start >= axis_size:
                raise IndexError(
                    f"Start index ({start}) out of range on axis {i}. Axis size is "
                    f"{axis_size}. Start index can be at most {axis_size-1}."
                )
            elif start is not None and start < 0 and start + axis_size >= axis_size:
                raise IndexError(
                    f"Start index ({start + axis_size}, calculated from provided index "
                    f"{start}) out of range on axis {i}. Axis size is {axis_size}. "
                     f"Start index can be at most {axis_size-1}."
                )
            elif stop is not None and stop > axis_size:
                raise IndexError(
                    f"End index ({stop}) out of range on axis {i}. Axis size is "
                    f"{axis_size}. End index can be at most {axis_size}."
                )
            elif stop is not None and stop < 0 and stop + axis_size > axis_size:
                raise IndexError(
                    f"End index ({stop + axis_size}, calculated from provided index "
                    f"{stop}) out of range on axis {i}. Axis size is {axis_size}. End "
                    f"index can be at most {axis_size}."
                )
            
            # if start or stop is None (not provided), there's no chance of a conflict
            if start is None or stop is None:
                continue
            
            # make sure end comes after start
            if stop >= 0 and start >= 0 and stop <= start:
                raise IndexError(
                    f"End index ({stop}) must be greater than start index ({start}) on "
                    f"axis {i}."
                )
            elif stop < 0 and start < 0 and stop + axis_size <= start + axis_size:
                raise IndexError(
                    f"End index ({stop + axis_size}, calculated from provided index "
                    f"{stop}) must be greater than start index ({start + axis_size}, "
                    f"calculated from provided index {start}) on axis {i}."
                )
            # at this point, we know one is positive and one is negative
            elif start < 0 and stop <= start + axis_size:
                raise IndexError(
                    f"End index ({stop}) must be greater than start index "
                    f"({start + axis_size}, calculated from provided index {start}) on "
                    f"axis {i}."
                )
            elif stop < 0 and stop + axis_size <= start:
                raise IndexError(
                    f"End index ({stop + axis_size}, calculated from provided index "
                    f"{stop}) must be greater than start index ({start}) on axis {i}."
                )

        new_data = self.data[index]

        # create new Slice object
        if len(new_data.shape) == 2:
            return Slice(data=new_data, 
                         pixel_dimensions=tuple(self.pixel_dimensions), 
                         thickness=self.thickness) 
        else:
            raise ValueError(
                "Invalid index, unexpected shape. Shape must be 2D. This error "
                "occurs when using an index like `my_slice[1, 3:5]` or "
                "`my_slice[1, 3]`."
            )

    def shape(self) -> tuple[int, int]:
        """
        Get the dimensions of the `data` array of the core slice.

        Returns
        -------
        tuple[int, int]
            The shape of the data array of the core slice.
        """
        return self.data.shape

    def filter(self, brightness_filter: Callable[[float], bool]) -> Slice:
        """
        Get section of the slice that only contains the specified brightness values.

        Arguments
        ---------
        brightness_filter : Callable[[float], bool]
            Lambda function that defines what will be filtered out. Function must either
            return false if the value should not be included or true if the value should
            be included.

        Returns
        -------
        Slice
            New `Slice` object with only the specified brightness values left,
            everything else is set to nan.
        """
        filter_lambda = np.vectorize(lambda x: x if brightness_filter(x) else np.nan)
        filtered = filter_lambda(self.data)

        return Slice(data=filtered, pixel_dimensions=self.pixel_dimensions)
