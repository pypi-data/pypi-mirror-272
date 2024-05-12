import subprocess
from pathlib import Path, PosixPath
from typing import Optional, Iterable, List

import numpy as np
import rasterio as rio
from logger import logger


def merge(
        input_files: Iterable[PosixPath],
        output_folder: Optional[str] = None,
        output_name: Optional[PosixPath] = None,
        output_nodata_value: int = 0,
        keep_separate: bool = False,
        output_format: str = "COG",
        output_datatype: str = "uint16",
        output_crs: str = None,
        output_pixel_size: tuple[int, int] = None,
        creation_option: str = None,
) -> Path:
    """
    Function to merge different raster files.

    Parameters:
        input_files         - tuple / list, files to be merged
        output_folder       - str, optional, path to output folder, default to
                              parent of first input file
        output_name         - str, optional, name of output file, default to name of
                              the first_input_file_merged.format
        input_nodata_value  - int, optional, no data value of input files
                              default to 0
        output_nodata_value - int, optional, no data value of output file
                              default to 0
        keep_separate       - bool, optional, True for placing input files
                              into separate bands of the output file
        output_format       - str, optional, format of the output file, default to GTiff
                              short name from https://gdal.org/drivers/raster/index.html
        output_datatype     - str, optional, datatype of the output file, default to  Int16
                              one of: ubyte | uint8 | uint16 | int16 | uint32 | int32 | float32 | float64
                              Float32, Float64, CInt16, CInt32, CFloat32 or CFloat64
        output_crs          - str, optional, of the form EPSG:int default to the most
                              repeated CRS of input files
        output_pixel_size   - tuple, optional, default to input pixel size of first input file
        creation_option     - str, optional, GDAL creation options available for specific formats
                              ref: https://gdal.org/drivers/raster/index.html,  default to None
                              eg: 'COMPRESS=LZW'
    Return:
        merged_file_path,   - str, full path of the merged output file

    """
    logger.debug("Merging files")
    if output_crs:
        # TODO: assuming all input files are with same CRS, do checks and
        #  reproject based on most repeated crs of input files
        pass

    # also assumes all inputs are perfect, do validations on them
    output = Path(output_folder) / Path(output_name)
    Path(output_folder).mkdir(exist_ok=True, parents=True)
    command = ("rio",)
    command += ("stack",) if keep_separate else ()
    if not keep_separate:
        command += ("merge",)
        command += ("-r", str(output_pixel_size[0]), "-r",
                    str(output_pixel_size[1])) if output_pixel_size else ()
        command += ("--nodata", str(output_nodata_value))
        command += ("-t", output_datatype) if output_datatype else ()

    command += ("-o", f"{str(output)}")
    command += ("-f", output_format) if output_format else ()
    command += ("--co", creation_option) if creation_option else ()
    command += ("--overwrite",)
    command += tuple([f"{str(input_file)}" for input_file in input_files])
    logger.debug("merging in progress ...")
    resp = subprocess.run(command, shell=False, capture_output=True)
    if resp.returncode != 0:
        logger.error(
            f"rio merge / stack function failed! command: {command} with error: {resp.stderr.decode('utf-8')}")
        return ""

    return output


def create_normalised_difference_index(
        filename_band_A: PosixPath,
        filename_band_B: PosixPath,
        output_folder: Optional[PosixPath] = None,
        output_name: Optional[PosixPath] = None,
        offset: int = 100,
        scaling_factor: int = 100,
        output_format: str = "COG",
        output_datatype: str = "uint8",
        creation_option: str = None,
) -> PosixPath:
    """
    Function to create normalised difference index images (B-A)/(B+A)

    Parameters:
        filename_band_A     - str, band A path
        filename_band_B     - str, band B path
        output_folder       - str, optional, path to output folder, default to
                              parent of first input file
        output_name         - str, optional, name of output file, default to name of
                              the first_input_file_merged.format
        offset              - int, optional, offset the index value by a constant, default 1
        scaling_factor      - int, optional, scale the index value by a constant, default 100
        output_format       - str, optional, format of the output file, default to GTiff
                              short name from https://gdal.org/drivers/raster/index.html
        output_datatype     - str, optional, datatype of the output file, default to  Int16
                              one of: Byte, UInt16, Int16, UInt32, Int32, UInt64, Int64,
                              Float32, Float64, CInt16, CInt32, CFloat32 or CFloat64
        creation_option     - str, optional, GDAL creation options available for specific formats
                              ref: https://gdal.org/drivers/raster/index.html,  default to None
                              eg: 'COMPRESS=LZW'
    Return:
        merged_file_path,   - str, full path of the merged output file

    """

    output = Path(output_folder) / output_name
    Path(output_folder).mkdir(exist_ok=True, parents=True)
    img_A = rio.open(filename_band_A)
    img_B = rio.open(filename_band_B)
    np.seterr(divide='ignore', invalid='ignore')

    index_array = np.true_divide(
        img_B.read(1).astype('float') - img_A.read(1).astype('float'),
        img_B.read(1).astype('float') + img_A.read(1).astype('float'))
    index_array = (index_array * scaling_factor) + offset
    index_array[np.isnan(index_array)] = 0
    index_array[np.isinf(index_array)] = 0
    try:
        with rio.Env():
            profile = img_A.profile
            profile.update(
                dtype=rio.uint8,
                count=1,
                compress="lzw",
                driver=output_format,
                nodata=0
            )

            with rio.open(output, 'w', **profile) as dst:
                dst.write(index_array.astype(rio.uint8), 1)
        del index_array, img_A, img_B

        return output
    except Exception as e:
        logger.error(f"Failed to creating normalised difference index >> {e}")
        raise Exception("Failed to creating normalised difference index")


def mask_cloud(
        input_file: PosixPath,
        output_folder: Optional[PosixPath],
        output_name: Optional[PosixPath],
        cloud_mask_bands: List[PosixPath],
        cloud_mask_threshold: List[int],
        target_value: int = 50,
        level: str = "L1C"
):
    """
        masking cloud pixels
    :param input_file:
    :param output_folder:
    :param output_name:
    :param cloud_mask_bands:
    :param cloud_mask_threshold:
    :param target_value:
    :param level:
    :return:
    """
    if len(cloud_mask_bands) != len(cloud_mask_threshold):
        logger.error("Cloud masking failed, number of mask bands != thresholds")
        return

    logger.debug("Creating Cloud mask")
    output = Path(output_folder) / output_name
    Path(output_folder).mkdir(exist_ok=True, parents=True)

    img_A = rio.open(cloud_mask_bands[0])
    img_B = rio.open(cloud_mask_bands[1])
    img_C = rio.open(input_file)

    np.seterr(divide='ignore', invalid='ignore')

    img_array = img_C.read(1)
    img_array[img_A.read(1) > cloud_mask_threshold[0]] = target_value
    img_array[img_B.read(1) > cloud_mask_threshold[1]] = target_value

    with rio.Env():
        profile = img_C.profile
        profile.update(
            dtype=rio.uint8,
            count=1,
            compress="lzw",
            driver="COG",
            nodata=0
        )

        with rio.open(output, 'w', **profile) as dst:
            dst.write(img_array.astype(rio.uint8), 1)
    del img_array, img_A, img_B, img_C
    logger.debug("Creating Cloud mask completed")

