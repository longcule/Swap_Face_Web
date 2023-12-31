#!/usr/bin/env python3

import os
import sys
# single thread doubles cuda performance - needs to be set before torch import
if any(arg.startswith('--execution-provider') for arg in sys.argv):
    os.environ['OMP_NUM_THREADS'] = '1'
# reduce tensorflow log level
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import warnings
from typing import List
import platform
import signal
import shutil
import argparse
import torch
import onnxruntime
import tensorflow
import roop.globals
import roop.metadata
import time
# import roop.ui as ui
from roop.predicter import predict_image, predict_video
from roop.processors.frame.core import get_frame_processors_modules
from roop.utilities import has_image_extension, is_image, is_video, detect_fps, create_video, extract_frames, get_temp_frame_paths, restore_audio, create_temp, move_temp, clean_temp, normalize_output_path

if 'ROCMExecutionProvider' in roop.globals.execution_providers:
    del torch

warnings.filterwarnings('ignore', category=FutureWarning, module='insightface')
warnings.filterwarnings('ignore', category=UserWarning, module='torchvision')


def encode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [execution_provider.replace('ExecutionProvider', '').lower() for execution_provider in execution_providers]


def decode_execution_providers(execution_providers: List[str]) -> List[str]:
    return [provider for provider, encoded_execution_provider in zip(onnxruntime.get_available_providers(), encode_execution_providers(onnxruntime.get_available_providers()))
            if any(execution_provider in encoded_execution_provider for execution_provider in execution_providers)]


def suggest_max_memory() -> int:
    if platform.system().lower() == 'darwin':
        return 4
    return 16


def suggest_execution_providers() -> List[str]:
    return encode_execution_providers(onnxruntime.get_available_providers())


def suggest_execution_threads() -> int:
    if 'DmlExecutionProvider' in roop.globals.execution_providers:
        return 1
    if 'ROCMExecutionProvider' in roop.globals.execution_providers:
        return 1
    return 8


def limit_resources() -> None:

    if roop.globals.max_memory:
        memory = roop.globals.max_memory * 1024 ** 3
        if platform.system().lower() == 'darwin':
            memory = roop.globals.max_memory * 1024 ** 6
        if platform.system().lower() == 'windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetProcessWorkingSetSize(-1, ctypes.c_size_t(memory), ctypes.c_size_t(memory))
        else:
            import resource
            resource.setrlimit(resource.RLIMIT_DATA, (memory, memory))


def release_resources() -> None:
    if 'CUDAExecutionProvider' in roop.globals.execution_providers:
        torch.cuda.empty_cache()





def update_status(message: str, scope: str = 'ROOP.CORE') -> None:
    print(f'[{scope}] {message}')



def start() -> None:
    for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):

        if not frame_processor.pre_start():
            return

    # process image to image
    if has_image_extension(roop.globals.target_path):


        shutil.copy2(roop.globals.target_path, roop.globals.output_path)
        for frame_processor in get_frame_processors_modules(roop.globals.frame_processors): 
            update_status('Progressing...', frame_processor.NAME)
            frame_processor.process_image(roop.globals.source_path, roop.globals.output_path, roop.globals.output_path)
            frame_processor.post_process()
            release_resources()
        if is_image(roop.globals.target_path):
            update_status('Processing to image succeed!')
        else:
            update_status('Processing to image failed!')
        return
    

    # process image to videos
    # if predict_video(roop.globals.target_path):
    #     destroy()
    # update_status('Creating temp resources...')
    # create_temp(roop.globals.target_path)
    # update_status('Extracting frames...')
    # extract_frames(roop.globals.target_path)
    # temp_frame_paths = get_temp_frame_paths(roop.globals.target_path)
    # for frame_processor in get_frame_processors_modules(roop.globals.frame_processors):
    #     update_status('Progressing...', frame_processor.NAME)
    #     frame_processor.process_video(roop.globals.source_path, temp_frame_paths)
    #     frame_processor.post_process()
    #     release_resources()
    # # handles fps
    # if roop.globals.keep_fps:
    #     update_status('Detecting fps...')
    #     fps = detect_fps(roop.globals.target_path)
    #     update_status(f'Creating video with {fps} fps...')
    #     create_video(roop.globals.target_path, fps)
    # else:
    #     update_status('Creating video with 30.0 fps...')
    #     create_video(roop.globals.target_path)
    # # handle audio
    # if roop.globals.keep_audio:
    #     if roop.globals.keep_fps:
    #         update_status('Restoring audio...')
    #     else:
    #         update_status('Restoring audio might cause issues as fps are not kept...')
    #     restore_audio(roop.globals.target_path, roop.globals.output_path)
    # else:
    #     move_temp(roop.globals.target_path, roop.globals.output_path)
    # # clean and validate
    # clean_temp(roop.globals.target_path)
    # if is_video(roop.globals.target_path):
    #     update_status('Processing to video succeed!')
    # else:
    #     update_status('Processing to video failed!')


def destroy() -> None:
    if roop.globals.target_path:
        clean_temp(roop.globals.target_path)
    quit()


def run() -> None:
    # parse_args()
    frame_processor = ["face_swapper"]
    max_memory = suggest_max_memory()
    execution_provider = 'cpu'
    execution_threads = suggest_execution_threads()
    args = argparse.Namespace(
        frame=frame_processor,
        memory=max_memory,
        many_faces=True,
        provider=execution_provider,
        threads=execution_threads,
        warp_2d=False,
        correct_color=False,
        no_debug_window=True,
    )

    roop.globals.many_faces = args.many_faces
    roop.globals.frame_processors = args.frame
    roop.globals.max_memory = args.memory
    roop.globals.execution_providers = decode_execution_providers(args.provider)
    roop.globals.execution_threads = args.threads
    print("ulalalla")
    start_time = time.time()  # Ghi nhận thời gian trước khi gọi hàm
    start()
    end_time = time.time()  # Ghi nhận thời gian sau khi hàm hoàn thành

    execution_time = end_time - start_time
    print(f"Thời gian chạy của hàm start(): {execution_time:.4f} giây")

