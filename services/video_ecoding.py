from services.base_service import BaseService
import subprocess
import os

class VideoEncodingService(BaseService):
    RESOLUTIONS = {
        "4k": "3840x2160",
        "1080p": "1920x1080",
        "720p": "1280x720",
    }


    def run(self, file_path: str, output_path: str) -> None:
        print("[VideoEncodingService] Starting encoding...")
        self._transcode(file_path, output_path)
        self._generate_sprites(file_path, output_path)
        print("[VideoEncodingService] Encoding done.")


    def _transcode(self, file_path: str, output_path: str) -> None:
        self._transcode_h264(file_path, output_path)
        self._transcode_vp9(file_path, output_path)
        self._transcode_hevc(file_path, output_path)


    def _transcode_h264(self, file_path: str, output_path: str) -> None:
        for name, resolution in self.RESOLUTIONS.items():
            output_file = os.path.join(output_path, "video", "h264", f"{name}_h264.mp4")
            command = [
                "ffmpeg", "-i", file_path,
                "-vf", f"scale={resolution}",
                "-c:v", "libx264",
                "-c:a", "aac",
                "-y",
                output_file
            ]

            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"[VideoEncodingService] h264 encoding failed: {result.stderr}")
            
            print(f"[VideoEncodingService] Encoded {output_file}")


    def _transcode_vp9(self, file_path: str, output_path: str) -> None:
        for name, resolution in self.RESOLUTIONS.items():
            output_file = os.path.join(output_path, "video", "vp9", f"{name}_vp9.webm")
            command = [
                "ffmpeg", "-i", file_path,
                "-vf", f"scale={resolution}",
                "-c:v", "libvpx-vp9",
                "-c:a", "libopus",
                "-y",
                output_file
            ]

            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"[VideoEncodingService] vp9 encoding failed: {result.stderr}")
            
            print(f"[VideoEncodingService] Encoded {output_file}")


    def _transcode_hevc(self, file_path: str, output_path: str) -> None:
        for name, resolution in self.RESOLUTIONS.items():
            output_file = os.path.join(output_path, "video", "hevc", f"{name}_hevc.mkv")
            command = [
                "ffmpeg", "-i", file_path,
                "-vf", f"scale={resolution}",
                "-c:v", "libx265",
                "-c:a", "aac",
                "-y",
                output_file
            ]

            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode != 0:
                raise RuntimeError(f"[VideoEncodingService] hevc encoding failed: {result.stderr}")
            
            print(f"[VideoEncodingService] Encoded {output_file}")


    def _generate_sprites(self, file_path: str, output_path: str) -> None:
        thumbnails_path = os.path.join(output_path, "images", "thumbnails")
        sprite_path = os.path.join(output_path, "images", "sprite_map.jpg")

        # generate thumbnails every 10 seconds
        thumb_command = [
            "ffmpeg", "-i", file_path,
            "-vf", "fps=1/10,scale=160:90",
            "-y",
            os.path.join(thumbnails_path, "thumb_%04d.jpg")
        ]

        result = subprocess.run(thumb_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"[VideoEncodingService] Thumbnail generation failed: {result.stderr}")
        
        print("[VideoEncodingService] Thumbnails generated.")

        # stitch thumbnails into sprite map
        sprite_command = [
            "ffmpeg", "-i", file_path,
            "-vf", "fps=1/10,scale=160:90,tile=10x10",
            "-y",
            sprite_path
        ]

        result = subprocess.run(sprite_command, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"[VideoEncodingService] Sprite map generation failed: {result.stderr}")
        
        print(f"[VideoEncodingService] Sprite map generated: {sprite_path}")