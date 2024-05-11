# type: ignore

import click
from ouster.cli.plugins import cli_mapping_impl
from ouster.sdk.io_type import OusterIoType
from ouster.cli.plugins.source import source
from ouster.cli.plugins.source_save import SourceSaveCommand
from ouster.cli.plugins.source_util import (source_multicommand,
                                            SourceCommandType,
                                            SourceCommandContext)


@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.argument("filename", required=True)
@click.option('-p', '--prefix', default="", help="Output prefix.")
@click.option('-d', '--dir', default="", help="Output directory.")
@click.option('-m', '--min-dist', default=2.0, help="Min distance (m) for points to "
              "save. Default value is 2m")
@click.option('-s', '--voxel-size', default=0.1, help="Voxel map size for downsampling."
              "This parameter is the same as the open3D voxel size. Default value is 0.1. "
              "The bigger the value, the fewer points it outputs")
@click.option('--field',
              required=False,
              type=click.Choice(['SIGNAL',
                                 'NEAR_IR',
                                 'REFLECTIVITY'],
                                case_sensitive=False),
              default="REFLECTIVITY",
              help="Chanfield for output file key value. Choose between SIGNAL, NEAR_IR, "
              "REFLECTIVITY. Default field is REFLECTIVITY")
@click.option('--decimate', required=False, type=bool,
              default=True, help="Downsample the point cloud to output. Default is On")
@click.option('--verbose', is_flag=True, default=False,
              help="Print point cloud status much frequently. Default is Off")
@click.option('--overwrite', is_flag=True, default=False, help="If true, overwrite "
              "existing files with the same name.")
@click.pass_context
@source_multicommand(type=SourceCommandType.CONSUMER)
def point_cloud_convert(ctx: SourceCommandContext, filename: str, prefix: str, 
                        dir: str, min_dist: float, voxel_size: float, field: str, 
                        decimate: bool, overwrite: bool, verbose: bool, **kwargs) -> None:

    cli_mapping_impl.points_convert_impl(ctx, filename, min_dist, voxel_size,
                                         field, verbose, decimate, overwrite,
                                         kwargs["format"], dir, prefix)


@click.command
@click.option('--slam-name', default='kiss_slam', help="Slam name")
@click.option('--max-range', required=False,
              default=150.0, help="Max valid range")
@click.option('--min-range', required=False,
              default=1.0, help="Min valid range")
@click.option('-v', '--voxel-size', required=False,
              type=float, help="Voxel map size")
@click.pass_context
@source_multicommand(type=SourceCommandType.PROCESSOR)
def source_slam(ctx: SourceCommandContext, slam_name: str, max_range: float,
                min_range: float, voxel_size: float, **kwargs) -> None:
    """
    Run SLAM with a SOURCE.\n

    Example values for voxel_size:\n
        Outdoor: 1.4 - 2.2\n
        Large indoor: 1.0 - 1.8\n
        Small indoor: 0.4 - 0.8\n
    If voxel_size is not specifiied, the algorithm will use the first 10 scans to calculate it.\n
    Small voxel size could give more accurate results but take more memory and
    longer processing. For real-time slam, considing using a slightly larger voxel size
    and use visualizer to monitor the SLAM process.
    """
    cli_mapping_impl.run_slam_impl(ctx, slam_name, max_range, min_range, voxel_size)


source.commands['ANY']['slam'] = source_slam
SourceSaveCommand.implementations[OusterIoType.PCD] = point_cloud_convert
SourceSaveCommand.implementations[OusterIoType.LAS] = point_cloud_convert
SourceSaveCommand.implementations[OusterIoType.PLY] = point_cloud_convert
