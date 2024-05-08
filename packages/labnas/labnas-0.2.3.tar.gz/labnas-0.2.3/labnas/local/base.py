"""Basic local functions."""

import re
from pathlib import Path

import numpy as np


def assert_single_stack(tif_files: list[Path]) -> str:
    """Check that there is only one stack in list of tifs"""
    tif_origin = identify_tif_origin(tif_files[0])
    if tif_origin == "leica":
        stack_names = get_leica_stack_names(tif_files)
    elif tif_origin == "basler":
        stack_names = get_basler_stack_names(tif_files)
    else:
        raise NotImplementedError(f"{tif_origin=} not implemented.")
    assert len(stack_names) == 1, f"More than 1 stack in {tif_files[0].parent}: {stack_names}"
    print(f"Only one stack: {stack_names[0]}")
    return stack_names[0]


def identify_tif_origin(tif: Path) -> str:
    """
    Identify where tif comes from.
    Relies on file name components added by recording software.
    """
    if "ch00" in tif.name:
        origin = "leica"
    elif "LUT" in tif.name:
        origin = "leica_metadata"
    elif "Basler" in tif.name:
        origin = "basler"
    else:
        raise ValueError(f"Cannot identify origin of tif {tif}")
    return origin


def get_leica_stack_names(tif_files: list[Path]) -> list:
    """Get stack names in leica tifs"""
    stack_names = []
    for file in tif_files:
        stack_name = re.findall(r".+(?=_[tz][0-9]+)", file.name)[0]
        if stack_name not in stack_names:
            stack_names.append(stack_name)
    return stack_names


def get_basler_stack_names(tif_files: list[Path]) -> list:
    stack_names = []
    for file in tif_files:
        file_name = file.name
        stack_name = re.findall(r"(?<=__)[0-9]+_[0-9]+", file_name)[0]
        if stack_name not in stack_names:
            stack_names.append(stack_name)
    return stack_names


def list_tif_files(folder: Path) -> list:
    """List all tif files in a local folder."""
    tif_files = []
    for element in folder.iterdir():
        if element.is_file():
            if element.suffix in [".tif", ".tiff"]:
                tif_files.append(element)
    return tif_files


def sort_tif_files(tif_files: list[Path]) -> np.ndarray:
    """Sort tif files by frame index."""
    tif_origin = identify_tif_origin(tif_files[0])
    if tif_origin == "leica":
        frame_numbers = [get_leica_frame_number(x) for x in tif_files]
    elif tif_origin == "basler":
        frame_numbers = [get_basler_frame_number(x) for x in tif_files]
    else:
        raise ValueError(f"{tif_origin=} not implemented.")
    check_completeness(frame_numbers)
    sort_vector = np.argsort(frame_numbers)
    tif_files = np.asarray(tif_files)
    tif_files = tif_files[sort_vector]
    return tif_files


def get_leica_frame_number(leica_file: Path) -> int:
    """Extract frame number from leica file name"""
    frame_number = re.findall(r"(?<=[tz])[0-9]+", leica_file.name)[0]
    # print(leica_file.name, frame_number)
    frame_number = int(frame_number)
    return frame_number


def get_basler_frame_number(basler_file: Path) -> int:
    """Extract frame number from basler file name"""
    frame_number = re.findall(r"[0-9]+(?=.tif)", basler_file.name)[0]
    frame_number = int(frame_number)
    return frame_number


def check_completeness(frame_numbers: list, verbose: bool = True) -> None:
    """Check that all frame numbers are present."""
    lowest = np.min(frame_numbers)
    highest = np.max(frame_numbers)
    all_possible = np.arange(lowest, highest)
    if not np.all(np.isin(all_possible, frame_numbers)):
        is_missing = np.logical_not(np.isin(all_possible, frame_numbers))
        missing_numbers = all_possible[is_missing]
        n_missing = np.sum(is_missing)
        n_total = all_possible.size
        fraction_missing = n_missing / n_total
        print(f"The following frame numbers are missing:")
        print(missing_numbers)
        raise TifFileMissingException(f"{n_missing}/{n_total} ({fraction_missing:.2%}) frame numbers are missing")
    if verbose:
        print(f"Frame numbers: {lowest} -> {highest} (count: {len(frame_numbers)})")


class TifFileMissingException(Exception):
    pass
