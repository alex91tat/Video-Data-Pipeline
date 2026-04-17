from services.base_service import BaseService
import os

REGIONAL_BRANDING = {
    "RO": "studio_original_ro.png",
    "DE": "studio_original_de.png",
    "JP": "studio_original_jp.png",
}

class ComplianceService(BaseService):
    def run(self, scenes: list) -> dict:
        print("[ComplianceService] Starting compliance checks...")
        flagged_scenes = self._safety_scan(scenes)
        self._apply_regional_branding()
        print("[ComplianceService] Compliance checks done.")
        return flagged_scenes
    

    def _safety_scan(self, scenes: list) -> dict:
        flagged_scenes = {}
        for index, scene in enumerate(scenes):
            if scene.get("type") == "action":
                flagged_scenes[index] = {
                    "start": scene["start"],
                    "reason": "violence",
                    "action": "blur",
                }

        if flagged_scenes:
            print(f"[ComplianceService] Flagged {len(flagged_scenes)} scene(s) for blurring.")
        else:
            print("[ComplianceService] No scenes flagged.")
        return flagged_scenes


    def _apply_regional_branding(self) -> None:
        for region, logo in REGIONAL_BRANDING.items():
            print(f"[ComplianceService] Applying branding for {region}: {logo}")