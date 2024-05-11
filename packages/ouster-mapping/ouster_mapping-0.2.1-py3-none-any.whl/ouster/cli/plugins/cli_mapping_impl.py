# type: ignore
import os
import sys
import click
import logging
from typing import Optional
import ouster.sdk.util.pose_util as pu
from ouster.sdk import osf, client
from ouster.sdk.util import default_scan_fields
import numpy as np
import laspy

from ouster.cli.plugins.source_util import SourceCommandType
from ouster.cli.plugins.source_save import (determine_filename,
                                            create_directories_if_missing,
                                            _file_exists_error)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('mapping')


def run_slam_impl(ctx: SourceCommandType,
                  slam_name: str = "kiss_slam",
                  max_range: float = 150.0,
                  min_range: float = 1.0,
                  voxel_size: float = None):


    def make_kiss_slam():
        if slam_name == "kiss_slam":
            try:
                from ouster.mapping.slam import KissBackend
            except ImportError as e:
                raise click.ClickException("kiss-icp, a package required for slam, is "
                                           "unsupported on this platform. Error: " + str(e))

            return KissBackend(info=ctx.scan_source.metadata,
                               max_range=max_range,
                               min_range=min_range,
                               voxel_size=voxel_size)
        else:
            raise ValueError("Only support KISS-ICP SLAM for now")


    try:
        slam_engine = make_kiss_slam()
    except (ValueError, click.ClickException) as e:
        logger.error(str(e))
        return


    def slam_scans_generator(scan_source, slam_engine):
        scan_start_ts = None
        for scan in scan_source:
            scan_ts = client.core.first_valid_column_ts(scan)
            if scan_ts == scan_start_ts:
                logger.info("SLAM restarts as scan iteration restarts")
                slam_engine = make_kiss_slam()
            if not scan_start_ts:
                scan_start_ts = scan_ts
            scan_slam = slam_engine.update(scan)
            yield scan_slam

    ctx.scan_iter = slam_scans_generator(ctx.scan_iter, slam_engine)


def points_convert_impl(ctx: SourceCommandType, filename: str, min_dist: float,
                        voxel_size: float, field: str, verbose: bool,
                        decimate: Optional[str], overwrite: bool,
                        out_format: str, out_dir: Optional[str],
                        out_prefix: Optional[str]) -> None:
    """
    Save point cloud from an OSF file into specific formats

    Output file format depends on output filename extension. The valid output files
    extensions are .las, .ply and .pcd. Default output format is .ply. For large point
    cloud, the output will be split into multiple files and each file is around 1G.
    Currently this tool only supports single lidar OSF files.
    """

    if decimate:
        try:
            import point_cloud_utils as pcu
        except ImportError as e:
            # point-cloud-utils needs scipy which is not supported on Mac M1
            # with Mac OS < 12.0
            raise click.ClickException("point_cloud_utils, a package required for point cloud decimation, is "
                                       "unsupported on this platform. Error: " + str(e))

    scans = ctx.scan_iter
    info = ctx.scan_source.metadata

    outfile_ext = "." + out_format
    output_file_path = determine_filename(out_prefix, out_dir, filename, 
                                          outfile_ext, info)
    create_directories_if_missing(output_file_path)

    # files pre exist check step
    file_wo_ext, outfile_ext = os.path.splitext(output_file_path)
    may_existed_file = file_wo_ext + '-000'+ outfile_ext

    if (os.path.isfile(output_file_path) or os.path.isfile(may_existed_file)) and not overwrite:
        print(_file_exists_error(f'{output_file_path} or {may_existed_file}'))
        exit(1)

    def save_iter():
        points_to_process = np.empty(shape=[0, 3])
        keys_to_process = np.empty(shape=[0, 1])
        points_keys_total = np.empty(shape=[0, 4])

        # hard-coded parameters and counters #
        # affect the running time. smaller value mean longer running time. Too large
        # may lead to crash
        down_sample_steps = 100
        # affect per output file size. makes output file size ~1G
        max_pnt_per_file = 10000000
        file_numb = 0

        # variables for point cloud status printout
        points_sum = 0
        points_saved = 0
        points_zero = 0
        points_near_removed = 0
        points_down_removed = 0

        valid_fields = default_scan_fields(
            info.format.udp_profile_lidar, flags=False)
        channel_field = client.ChanField.from_string(field)

        if channel_field not in valid_fields:
            valid_fields_str = ", ".join(map(str, list(valid_fields.keys())))

            sys.exit(f"Exit! field {field} is not available in the low bandwidth mode\n"
                    f"use -f and choose a valid field from {valid_fields_str}")

        xyzlut = client.XYZLut(info, use_extrinsics=True)

        def process_points(points, keys):
            nonlocal points_keys_total, points_down_removed, points_saved

            pts_size_before = points.shape[0]

            if decimate:
                # can be extended for RGBA values later
                points, keys = pcu.downsample_point_cloud_on_voxel_grid(
                    voxel_size, points, keys)
                keys = keys[:, np.newaxis]

            pts_size_after = points.shape[0]

            points_down_removed += pts_size_before - pts_size_after
            points_saved += pts_size_after

            pts_keys_pair = np.append(points, keys, axis=1)
            points_keys_total = np.append(points_keys_total, pts_keys_pair, axis=0)

        def save_file(file_wo_ext: str, outfile_ext: str):
            nonlocal points_keys_total
            logger.info(f"Output file: {file_wo_ext + outfile_ext}")
            pc_status_print()

            if outfile_ext == ".ply":
                # CloudCompare PLY color point cloud using the range 0-1
                with open(file_wo_ext + outfile_ext, 'w') as f:
                    # Write PLY header
                    f.write("ply\n")
                    f.write("format ascii 1.0\n")
                    f.write(
                        "element vertex {}\n".format(
                            points_keys_total.shape[0]))
                    f.write("property float x\n")
                    f.write("property float y\n")
                    f.write("property float z\n")
                    f.write("property float key\n")
                    f.write("end_header\n")
                    for i in range(points_keys_total.shape[0]):
                        f.write("{} {} {} {}\n".format(
                            points_keys_total[i, 0], points_keys_total[i, 1],
                            points_keys_total[i, 2], points_keys_total[i, 3] / 255))
            elif outfile_ext == ".las":
                LAS_file = laspy.create()
                LAS_file.x = points_keys_total[:, 0]
                LAS_file.y = points_keys_total[:, 1]
                LAS_file.z = points_keys_total[:, 2]
                # LAS file only has intensity but we can use it for other field
                # value
                LAS_file.intensity = points_keys_total[:, 3]
                LAS_file.write(file_wo_ext + outfile_ext)
            elif outfile_ext == ".pcd":
                with open(file_wo_ext + outfile_ext, 'w') as f:
                    # Write PCD header
                    f.write("FIELDS x y z key\n")
                    f.write("SIZE 4 4 4 4\n")
                    f.write("TYPE F F F F\n")
                    f.write("COUNT 1 1 1 1\n")
                    f.write("WIDTH %d\n" % (points_keys_total.shape[0]))
                    f.write("HEIGHT 1\n")
                    f.write("POINTS %d\n" % (points_keys_total.shape[0]))
                    f.write("DATA ascii\n")
                    for i in range(points_keys_total.shape[0]):
                        f.write("{} {} {} {}\n".format(
                            points_keys_total[i, 0], points_keys_total[i, 1],
                            points_keys_total[i, 2], points_keys_total[i, 3]))

            points_keys_total = np.empty(shape=[0, 4])

        def pc_status_print():
            nonlocal points_sum, points_near_removed, points_down_removed, points_saved, points_zero
            near_minus_zero = points_near_removed - points_zero
            near_removed_pernt = (near_minus_zero / points_sum) * 100
            down_removed_pernt = (points_down_removed / points_sum) * 100
            zero_pernt = (points_zero / points_sum) * 100
            save_pernt = (points_saved / points_sum) * 100
            logger.info(
                f"Point Cloud status info\n"
                f"{points_sum} points accumulated during this period,\n{near_minus_zero} "
                f"near points are removed [{near_removed_pernt:.2f} %],\n{points_down_removed} "
                f"down sampling points are removed [{down_removed_pernt:.2f} %],\n{points_zero} "
                f"zero range points are removed [{zero_pernt:.2f} %],\n{points_saved} points "
                f"are saved [{save_pernt:.2f} %].")
            points_sum = 0
            points_zero = 0
            points_saved = 0
            points_near_removed = 0
            points_down_removed = 0

        scan_start_ts = None
        empty_pose = True
        finish_saving = False
        finish_saving_action = True
        logger.info("Start processing...")
        try:
            for scan_idx, scan in enumerate(scans):
                scan_ts = client.core.first_valid_column_ts(scan)
                if scan_ts == scan_start_ts:
                    finish_saving = True
                    logger.info("Scan iteration restarts")
                if finish_saving:
                    # Save point cloud and printout when scan iteration restarts
                    # This action only do once
                    if finish_saving_action:
                        process_points(points_to_process, keys_to_process)
                        save_file(f"{file_wo_ext}-{file_numb:03}", outfile_ext)
                        logger.info("Finished point cloud saving.")
                        finish_saving_action = False
                    yield scan
                    continue
                if not scan_start_ts:
                    scan_start_ts = scan_ts

                # Pose attribute is per col global pose so we use identity for scan
                # pose
                column_poses = scan.pose

                if (empty_pose and column_poses.size > 0
                        and not np.array_equal(column_poses[client.first_valid_column(scan)], np.eye(4))):
                    empty_pose = False

                points = xyzlut(scan)
                keys = scan.field(channel_field)

                if scan_idx and scan_idx % 100 == 0:
                    logger.info(f"Processed {scan_idx} lidar scan")

                # to remove near points
                row_index = scan.field(client.ChanField.RANGE) > (min_dist * 1000)
                zero_row_index = scan.field(client.ChanField.RANGE) == 0
                dewarped_points = pu.dewarp(points, column_poses=column_poses)
                filtered_points = dewarped_points[row_index]
                filtered_keys = keys[row_index]

                curr_scan_points = row_index.shape[0] * row_index.shape[1]
                points_sum += curr_scan_points
                points_near_removed += curr_scan_points - np.count_nonzero(row_index)
                points_zero += np.count_nonzero(zero_row_index)

                # may not need below line
                shaped_keys = filtered_keys.reshape(filtered_keys.shape[0], 1)
                points_to_process = np.append(points_to_process, filtered_points,
                                            axis=0)
                keys_to_process = np.append(keys_to_process, shaped_keys, axis=0)

                # downsample the accumulated point clouds #
                if scan_idx % down_sample_steps == 0:
                    process_points(points_to_process, keys_to_process)
                    points_to_process = np.empty(shape=[0, 3])
                    keys_to_process = np.empty(shape=[0, 1])
                    if verbose:
                        pc_status_print()

                # output a file to prevent crash due to oversize #
                if points_keys_total.shape[0] >= max_pnt_per_file:
                    save_file(f"{file_wo_ext}-{file_numb:03}", outfile_ext)
                    file_numb += 1

                yield scan
        
        except KeyboardInterrupt:
            pass

        finally:
            if empty_pose:
                logger.info(
                    "Warning: Empty lidar scan pose in lidarscan stream!!!\n"
                    "Suggest: Append slam option to ouster-cli command or use a "
                    "SLAM output OSF file as an input.")

            # handle the last part of point cloud or the first part of point cloud if
            # the size is less than down_sample_steps
            if not finish_saving:
                if keys_to_process.size > 0:
                    process_points(points_to_process, keys_to_process)

                save_file(f"{file_wo_ext}-{file_numb:03}", outfile_ext)
                logger.info("Finished point cloud saving.")
    
    ctx.scan_iter = save_iter()


class SLAMOSFWriter:

    def __init__(self, metadata_json_str: str,
                 output_path: str, chunk_size: int):
        lidar_sensor_meta = osf.LidarSensor(metadata_json_str)
        self.writer = osf.Writer(output_path, "SLAM_Output_OSF", chunk_size)
        # TODO sensor_id may changed depends on how will we handle multi live
        # sensor
        sensor_osf_id = dict()
        # Fix the sensor id logic. Later need to extend to multisensor
        single_sensor_id = 0
        sensor_osf_id[single_sensor_id] = self.writer.addMetadata(
            lidar_sensor_meta)

        self.lidar_stream = osf.LidarScanStream(
            self.writer, sensor_osf_id[single_sensor_id])

    def write_scan(self, scan_ts, scan):
        self.lidar_stream.save(scan_ts, scan)

    def close(self):
        self.writer.close()
