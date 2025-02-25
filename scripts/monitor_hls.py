import os
import time
import requests


def monitor_hls_directory(stream_key):
    BACKEND_URL = f"http://127.0.0.1:8000/api/v1/live/upload_segment/{stream_key}"
    HLS_PATH = f"/tmp/hls/"

    processed_files = set()
    while True:
        for root, _, files in os.walk(HLS_PATH):
            for file in files:
                if file.endswith(".ts") and file not in processed_files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            response = requests.post(
                                BACKEND_URL,
                                data={"stream_key": stream_key},
                                files={"file": f},
                            )
                        if response.status_code == 200:
                            print(f"Segment {file} enviado com sucesso.")
                            processed_files.add(file)
                        else:
                            print(f"Falha ao enviar {file}: {response.text}")
                    except Exception as e:
                        print(f"Erro ao enviar {file}: {e}")
        time.sleep(1)

if __name__ == "__main__":
    print("Monitorando HLS... Esperando pela chave de stream")
