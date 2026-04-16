import hashlib
import os

class IngestService:
    SUPPORTED_EXTENSIONS = [".mp4", ".mov", ".mkv", ".avi"]

    def run(self, file_path: str) -> bool:
        print("[IngestService] Starting ingest...")
        return self._check_integrity(file_path) and self._validate_format(file_path)
    

    def _check_integrity(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            print(f"[IngestService] File not found: {file_path}")
            return False
        checksum = self._compute_checksum(file_path)
        print(f"[IngestService] Checksum: {checksum}")
        return True


    def _compute_checksum(self, file_path: str) -> str:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()


    def _validate_format(self, file_path: str) -> bool:
        _, ext = os.path.splitext(file_path)
        if ext.lower() not in self.SUPPORTED_EXTENSIONS:
            print(f"[IngestService] Unsupported format: {ext}")
            return False
        print(f"[IngestService] Format valid: {ext}")
        return True