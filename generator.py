from dataclasses import dataclass
from typing import List, Set, Tuple
import random
import time

@dataclass(frozen=True)
class Tech:
    name: str
    tags: Tuple[str, ...] = ()

@dataclass
class Step:
    number: int
    stance: str
    combo: List[Tech]

BLOCKS_SINGLE = [
    Tech("jodan uke", ("block",)),
    Tech("gyaku jodan uke", ("block", "gyaku")),
    Tech("chudan soto uke", ("block",)),
    Tech("gyaku chudan soto uke", ("block", "gyaku")),
    Tech("chudan uchi uke", ("block",)),
    Tech("gyaku chudan uchi uke", ("block", "gyaku")),
    Tech("gedan barai", ("block",)),
    Tech("gyaku gedan barai", ("block", "gyaku")),
    Tech("morote chudan uke", ("block",)),
    Tech("juji uke", ("block",)),
    Tech("osae uke", ("block",)),
]

BLOCKS_DOUBLE_SIMULTANEOUS = [
    Tech("jodan uke gedan barai", ("block", "double")),
    Tech("chudan uchi uke gedan barai", ("block", "double")),
    Tech("chudan soto uke gedan barai", ("block", "double")),
]

BLOCKS_DOUBLE_SEQUENTIAL = [
    Tech("jodan uke y gedan barai", ("block", "double")),
    Tech("gedan barai y jodan uke", ("block", "double")),
    Tech("chudan soto uke y chudan uchi uke", ("block", "double")),
    Tech("chudan uchi uke y gedan barai", ("block", "double")),
]

PUNCHES_OI = [
    Tech("oi seiken jodan tsuki", ("punch", "oi")),
    Tech("oi seiken chudan tsuki", ("punch", "oi")),
    Tech("oi seiken gedan tsuki", ("punch", "oi")),
    Tech("oi seiken chudan tate tsuki", ("punch", "oi")),
    Tech("oi seiken chudan ura tsuki", ("punch", "oi")),
    Tech("oi seiken jodan age tsuki", ("punch", "oi")),
]

PUNCHES_GYAKU = [
    Tech("gyaku seiken jodan tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken chudan tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken gedan tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken chudan tate tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken chudan ura tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken chudan kagi tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken gedan shita tsuki", ("punch", "gyaku")),
    Tech("gyaku seiken jodan ago uchi", ("punch", "gyaku")),
]

PUNCHES_MOROTE = [
    Tech("jodan morote tsuki", ("punch", "morote")),
    Tech("chudan morote tsuki", ("punch", "morote")),
    Tech("gedan morote tsuki", ("punch", "morote")),
]

URAKEN = [
    Tech("uraken ganmen uchi", ("strike", "uraken")),
    Tech("uraken sayu uchi", ("strike", "uraken")),
    Tech("uraken hizo uchi", ("strike", "uraken")),
    Tech("uraken mawashi uchi", ("strike", "uraken")),
    Tech("uraken oroshi uchi", ("strike", "uraken")),
]

SHUTO = [
    Tech("shuto ganmen uchi", ("strike", "shuto")),
    Tech("shuto sakotsu uchi", ("strike", "shuto")),
    Tech("shuto sakotsu uchikomi", ("strike", "shuto")),
    Tech("shuto hizo uchi", ("strike", "shuto")),
    Tech("shuto jodan uchi", ("strike", "shuto")),
    Tech("haito jodan uchi", ("strike", "shuto")),
    Tech("haito chudan uchi", ("strike", "shuto")),
]

TETTSUI = [
    Tech("tettsui oroshi uchi", ("strike", "tettsui")),
    Tech("tettsui yoko uchi", ("strike", "tettsui")),
    Tech("tettsui kome kami uchi", ("strike", "tettsui")),
    Tech("tettsui hizo uchi", ("strike", "tettsui")),
]

ELBOW = [
    Tech("hiji chudan ate", ("elbow",)),
    Tech("hiji jodan age ate", ("elbow",)),
    Tech("hiji chudan yoko uchi", ("elbow",)),
    Tech("hiji chudan mawashi uchi", ("elbow",)),
    Tech("hiji jodan oroshi uchi", ("elbow",)),
    Tech("ushiro hiji chudan ate", ("elbow",)),
    Tech("shotei hiji yoko uchi", ("elbow", "shotei")),
    Tech("gyaku shotei hiji yoko uchi", ("elbow", "shotei", "gyaku")),
]

KICKS_BASE = [
    Tech("chusoku jodan mae geri", ("kick",)),
    Tech("chusoku chudan mae geri", ("kick",)),
    Tech("chusoku chudan mae keage", ("kick",)),
    Tech("haisoku jodan mawashi geri", ("kick",)),
    Tech("haisoku chudan mawashi geri", ("kick",)),
    Tech("chusoku gedan mawashi geri", ("kick",)),
    Tech("haisoku uchi mawashi geri", ("kick",)),
    Tech("haisoku soto mawashi geri", ("kick",)),
    Tech("sokuto chudan yoko geri keage", ("kick",)),
    Tech("sokuto chudan yoko geri kekomi", ("kick",)),
    Tech("kakato chudan ushiro geri", ("kick",)),
    Tech("kakato jodan oroshi geri", ("kick",)),
    Tech("sokuto kansetsu geri", ("kick",)),
]

KNEE = [
    Tech("hiza chudan geri", ("knee",)),
    Tech("hiza mawashi geri", ("knee",)),
]

SANBON = [
    Tech("sanbon seiken chudan tsuki", ("combo", "sanbon")),
    Tech("sanbon seiken jodan tsuki", ("combo", "sanbon")),
]

TURN = Tech("mawatte", ("turn",))
GEDAN_BARAI = Tech("gedan barai", ("block",))
SHUTO_NO_KAMAE = Tech("shuto no kamae", ("block", "shuto"))


def make_modori(kick: Tech) -> Tech:
    return Tech(f"{kick.name} modori", kick.tags + ("modori",))

def make_nihon(tech: Tech) -> Tech:
    return Tech(f"nihon {tech.name}", tech.tags + ("nihon",))

def make_nikai(tech: Tech) -> Tech:
    return Tech(f"nikai {tech.name}", tech.tags + ("nikai",))

def make_ikio_do(tech1: Tech, tech2: Tech) -> Tech:
    combined_tags = tuple(set(tech1.tags + tech2.tags + ("ikio",)))
    return Tech(f"{tech1.name} ikio do {tech2.name}", combined_tags)


class IdoGeikoGenerator:
    def __init__(self, seed=None):
        self.rng = random.Random(seed if seed is not None else int(time.time() * 1000))
        self.used_in_cycle: Set[str] = set()
        
        self.all_blocks = BLOCKS_SINGLE + BLOCKS_DOUBLE_SIMULTANEOUS + BLOCKS_DOUBLE_SEQUENTIAL
        self.all_punches = PUNCHES_OI + PUNCHES_GYAKU + PUNCHES_MOROTE
        self.all_strikes = URAKEN + SHUTO + TETTSUI
        self.kicks_modori = [make_modori(k) for k in KICKS_BASE]
        self.knee_modori = [make_modori(k) for k in KNEE]
        
        self.nihon_candidates = (
            [b for b in BLOCKS_SINGLE if "double" not in b.tags and "gyaku" not in b.tags] +
            PUNCHES_OI +
            [s for s in URAKEN if "gyaku" not in s.tags] +
            [s for s in SHUTO if "gyaku" not in s.tags] +
            [s for s in TETTSUI if "gyaku" not in s.tags] +
            [e for e in ELBOW if "gyaku" not in e.tags]
        )
        
        self.nikai_candidates = (
            PUNCHES_OI + PUNCHES_GYAKU +
            URAKEN + SHUTO + TETTSUI + ELBOW +
            self.kicks_modori + self.knee_modori +
            [Tech("shuto no kamae", ("shuto",))]
        )

    def pick(self, pool: List[Tech], used_step: Set[str]) -> Tech:
        available = [t for t in pool if t.name not in used_step and t.name not in self.used_in_cycle]
        if not available:
            available = [t for t in pool if t.name not in used_step]
        if not available:
            available = pool
        choice = self.rng.choice(available)
        used_step.add(choice.name)
        self.used_in_cycle.add(choice.name)
        return choice

    def build_nihon(self, used_step: Set[str]) -> Tech:
        base = self.pick(self.nihon_candidates, used_step)
        return make_nihon(base)

    def build_nikai(self, used_step: Set[str]) -> Tech:
        base = self.pick(self.nikai_candidates, used_step)
        return make_nikai(base)

    def build_ikio_do(self, used_step: Set[str]) -> Tech:
        hand_pool = self.all_blocks + PUNCHES_GYAKU + self.all_strikes + ELBOW
        foot_pool = self.kicks_modori + self.knee_modori
        
        if self.rng.random() < 0.7:
            tech1 = self.pick(hand_pool, used_step)
            tech2 = self.pick(hand_pool, used_step)
        else:
            tech1 = self.pick(foot_pool, used_step)
            tech2 = self.pick(foot_pool, used_step)
        return make_ikio_do(tech1, tech2)

    def build_combo(self, step_number: int, level: int, is_kokutsu: bool) -> List[Tech]:
        used: Set[str] = set()
        combo: List[Tech] = []
        
        if step_number == 4:
            combo.append(TURN)
            used.add(TURN.name)

        if step_number == 1:
            if is_kokutsu:
                combo.append(SHUTO_NO_KAMAE)
                used.add(SHUTO_NO_KAMAE.name)
            elif self.rng.random() < 0.9:
                combo.append(GEDAN_BARAI)
                used.add(GEDAN_BARAI.name)
            else:
                non_shuto_blocks = [b for b in self.all_blocks if "shuto" not in b.tags]
                combo.append(self.pick(non_shuto_blocks, used))
        else:
            if is_kokutsu:
                shuto_blocks = [b for b in self.all_blocks if "shuto" in b.tags]
                if shuto_blocks:
                    combo.append(self.pick(shuto_blocks, used))
                else:
                    combo.append(self.pick(self.all_blocks, used))
            else:
                non_shuto_blocks = [b for b in self.all_blocks if "shuto" not in b.tags]
                combo.append(self.pick(non_shuto_blocks, used))

        remaining = level - len(combo)
        if remaining <= 0:
            return combo

        strikes_for_stance = SHUTO if is_kokutsu else [s for s in self.all_strikes if "shuto" not in s.tags]

        for i in range(remaining):
            is_last = (i == remaining - 1)
            
            if is_last:
                options = ["kick", "punch", "elbow", "knee", "nihon", "nikai", "ikio"]
            else:
                options = ["punch", "strike", "kick", "elbow", "nihon", "nikai", "ikio"]
            
            choice = self.rng.choice(options)
            
            if choice == "punch":
                pool = PUNCHES_GYAKU if self.rng.random() < 0.6 else PUNCHES_OI
                combo.append(self.pick(pool, used))
            elif choice == "strike":
                combo.append(self.pick(strikes_for_stance, used))
            elif choice == "kick":
                combo.append(self.pick(self.kicks_modori, used))
            elif choice == "elbow":
                combo.append(self.pick(ELBOW, used))
            elif choice == "knee":
                combo.append(self.pick(self.knee_modori, used))
            elif choice == "nihon":
                combo.append(self.build_nihon(used))
            elif choice == "nikai":
                combo.append(self.build_nikai(used))
            elif choice == "ikio":
                combo.append(self.build_ikio_do(used))

        return combo

    def build_step(self, step_number: int, level: int, is_kokutsu: bool) -> Step:
        combo = self.build_combo(step_number, level, is_kokutsu)
        stance = "kokutsu dachi" if is_kokutsu else "zenkutsu dachi"
        return Step(step_number, stance, combo)

    def generate_cycle(self, level: int, is_kokutsu: bool = None) -> List[Step]:
        self.used_in_cycle.clear()
        if is_kokutsu is None:
            is_kokutsu = self.rng.random() < 0.3
        return [self.build_step(n, level, is_kokutsu) for n in range(1, 5)]


def format_step(step: Step) -> str:
    tech_names = ", ".join(t.name for t in step.combo)
    return f"Paso {step.number} ({step.stance}): {tech_names}"


def rotate_cycle(cycle: List[Step], start_at: int) -> List[Step]:
    idx = start_at - 1
    rotated = cycle[idx:] + cycle[:idx]
    for i, step in enumerate(rotated):
        step.number = i + 1
    return rotated