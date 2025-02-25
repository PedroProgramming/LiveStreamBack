import os, time, subprocess
from .models import LiveStream

def is_file_complete(file_path, timeout=5):
    last_size = -1
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if os.path.exists(file_path):
            current_size = os.path.getsize(file_path)
            if current_size == last_size:
                return True
            last_size = current_size
        time.sleep(0.5)
    
    return False

def generate_master_playlist(path_folder, resolutions):
    master_file = os.path.join(path_folder, "master.m3u8")
    playlist_content = "#EXTM3U\n"

    bandwidth_map = {
        "480p": 500000,
        #"720p": 1000000,
        #"1080p": 2500000
    }

    for resolution, params in resolutions.items():
        resolution_folder = os.path.join(path_folder, resolution)
        playlist_path = f"{resolution}/{resolution}.m3u8"

        if os.path.exists(os.path.join(resolution_folder, f"{resolution}.m3u8")):
            width, height = map(int, params['scale'].split(":"))
            playlist_content += f"#EXT-X-STREAM-INF:BANDWIDTH={bandwidth_map[resolution]},RESOLUTION={width}x{height}\n"
            playlist_content += f"{playlist_path}\n"

    with open(master_file, "w") as f:
        f.write(playlist_content)

def process_segment(path_segment, resolutions, path_folder):

    for resolution, params in resolutions.items():
        output_path = os.path.join(path_folder, resolution)
        os.makedirs(output_path, exist_ok=True)

        ffmpeg_command = [
            "ffmpeg", "-i", path_segment,
            "-vf", f"scale={params['scale']}", 
            "-c:v", "libx264", 
            "-b:v", params["bitrate"], 
            "-preset", "fast",
            "-hls_time", "1", 
            "-hls_playlist_type", "event",
            "-hls_flags", "append_list",
            "-hls_list_size", "10",
            "-hls_segment_filename", f"{output_path}/{resolution}-%03d.ts",
            f"{output_path}/{resolution}.m3u8"
        ]
        result = subprocess.run(ffmpeg_command, check=True)

        if result.returncode != 0:
            print(f"Erro no FFmpeg: {result.stderr.decode()}")
        else:
            pass
    generate_master_playlist(path_folder, resolutions)

def monitor_hls_directory(stream_key):
    HLS_PATH = f"/tmp/hls"

    resolutions = {
        "480p": {"scale": "854:480", "bitrate": "1000k"},
        # "720p": {"scale": "1280:720", "bitrate": "2500k"},
        # "1080p": {"scale": "1920:1080", "bitrate": "5000k"}
    }

    path_folder = f"{HLS_PATH}/{stream_key}"
    os.makedirs(path_folder, exist_ok=True)

    time_verify = time.time()    

    processed_files = set()
    while True:
        if time.time() - time_verify >= 180:
            live = LiveStream.objects.filter(stream_key__iexact=stream_key).first()
            time_verify = time.time()
            if not live or not live.is_active:
                break

        for root, _, files in os.walk(HLS_PATH):

            for file in files:
                if file.endswith(".ts") and file not in processed_files:
                    file_path = os.path.join(root, file)
                    if is_file_complete(file_path):
                        processed_files.add(file)
                        process_segment(file_path, resolutions, path_folder)
                    else:
                        pass
        time.sleep(1)
    return