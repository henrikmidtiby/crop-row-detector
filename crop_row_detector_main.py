import argparse

from convert_orthomosaic_to_list_of_tiles import convert_orthomosaic_to_list_of_tiles
from crop_row_detector import crop_row_detector

parser = argparse.ArgumentParser(description="Detect crop rows in segmented image")
parser.add_argument("segmented_orthomosaic", help="Path to the segmented_orthomosaic that you want to process.")
parser.add_argument(
    "--orthomosaic",
    help="Path to the orthomosaic that you want to plot on. " "if not set, the segmented_orthomosaic will be used.",
)
parser.add_argument(
    "--tile_size", default=3000, type=int, help="The height and width of tiles that are analyzed. " "Default is 3000."
)
parser.add_argument(
    "--output_tile_location", default="output/mahal", help="The location in which to save the mahalanobis tiles."
)
parser.add_argument(
    "--generate_debug_images",
    default=False,
    type=bool,
    help="If set to true, debug images will be generated, default is False",
)
parser.add_argument(
    "--tile_boundary",
    default=False,
    type=bool,
    help="if set to true will plot a boundary on each tile " "and the tile number on the tile, is default False.",
)
parser.add_argument(
    "--run_specific_tile",
    nargs="+",
    type=int,
    help="If set, only run the specific tile numbers. " "(--run_specific_tile 16 65) will run tile 16 and 65.",
)
parser.add_argument(
    "--run_specific_tileset",
    nargs="+",
    type=int,
    help="takes two inputs like (--from_specific_tile 16 65). " "this will run every tile from 16 to 65.",
)
parser.add_argument(
    "--expected_crop_row_distance",
    default=20,
    type=int,
    help="The expected distance between crop rows in pixels, default is 20.",
)
parser.add_argument(
    "--run_parallel",
    default=True,
    type=bool,
    help="If set to true, the program will run in parallel mode, default is True.",
)
args = parser.parse_args()

# Initialize the tile separator
tsr = convert_orthomosaic_to_list_of_tiles()
tsr.run_specific_tile = args.run_specific_tile
tsr.run_specific_tileset = args.run_specific_tileset
tsr.tile_size = args.tile_size
tsr.output_tile_location = args.output_tile_location
segmented_tile_list = tsr.main(args.segmented_orthomosaic)
if args.orthomosaic is None:
    plot_tile_list = tsr.main(args.segmented_orthomosaic)
else:
    plot_tile_list = tsr.main(args.orthomosaic)


# Initialize the crop row detector
crd = crop_row_detector()
crd.generate_debug_images = args.generate_debug_images
crd.tile_boundary = args.tile_boundary
crd.expected_crop_row_distance = args.expected_crop_row_distance
crd.threshold_level = 12
crd.run_parralel = args.run_parallel
crd.main(segmented_tile_list, plot_tile_list, args)


# python3 crop_row_detector_main.py rødsvingel/input_data/rødsvingel.tif --orthomosaic rødsvingel/input_data/2023-04-03_Rødsvingel_1._års_Wagner_JSJ_2_ORTHO.tif --output_tile_location rødsvingel/tiles_crd --tile_size 500 --tile_boundary True --generate_debug_images True --run_specific_tile 16
# gdal_merge.py -o rødsvingel/rødsvingel_crd.tif -a_nodata 255 rødsvingel/tiles_crd/mahal*.tiff
