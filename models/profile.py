import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional
from utils.logger import logger

@dataclass
class ClickPoint:
    x: int
    y: int
    interval: float
    button: str = 'left'      # left, right, middle
    click_type: str = 'single' # single, double
    delay_awal: float = 0.0

@dataclass
class Profile:
    name: str
    points: List[ClickPoint]
    loop_type: str = 'infinite' # infinite, fixed
    loop_count: int = 1

class ProfileManager:
    def __init__(self, profiles_dir='profiles'):
        self.profiles_dir = profiles_dir
        if not os.path.exists(profiles_dir):
            os.makedirs(profiles_dir)

    def save_profile(self, profile: Profile):
        filepath = os.path.join(self.profiles_dir, f"{profile.name}.json")
        try:
            data = {
                'name': profile.name,
                'loop_type': profile.loop_type,
                'loop_count': profile.loop_count,
                'points': [asdict(p) for p in profile.points]
            }
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Profile '{profile.name}' saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save profile '{profile.name}': {e}")

    def load_profile(self, name: str) -> Optional[Profile]:
        filepath = os.path.join(self.profiles_dir, f"{name}.json")
        if not os.path.exists(filepath):
            logger.warning(f"Profile '{name}' not found.")
            return None
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                points = [ClickPoint(**p) for p in data.get('points', [])]
                logger.info(f"Profile '{name}' loaded successfully.")
                return Profile(
                    name=data.get('name', name),
                    points=points,
                    loop_type=data.get('loop_type', 'infinite'),
                    loop_count=data.get('loop_count', 1)
                )
        except Exception as e:
            logger.error(f"Failed to load profile '{name}': {e}")
            return None

    def get_all_profiles(self) -> List[str]:
        return [f[:-5] for f in os.listdir(self.profiles_dir) if f.endswith('.json')]
