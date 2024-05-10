import toml
import subprocess
import time
from pathlib import Path
import dataclasses
from typing import Optional as Opt, List, Dict
import argparse


CFD = Path(__file__).parent


@dataclasses.dataclass
class Cfg:
    run: str
    pre_run: Opt[str] = None
    post_run: Opt[str] = None


def run(
    file: str,
    cfg: Cfg,
):
    run, pre_run, post_run = cfg.run, cfg.pre_run, cfg.post_run
    if pre_run:
        pre_run = pre_run.replace("<file>", file)
        subprocess.run(
            pre_run.split("\n"),
            check=False,
            shell=True,
        )
    run = run.replace("<file>", file)
    s = time.time()
    subprocess.run(run.split("\n"), check=False, shell=True)
    e = time.time()
    print("Time:", e - s)
    if post_run:
        post_run = post_run.replace("<file>", file)
        subprocess.run(
            post_run.split("\n"),
            check=False,
            shell=True,
        )


class CfgMgr:
    _configs: Dict[str, Cfg]
    _from_ext: Dict[str, str]

    def __init__(self):
        self._configs = {}
        self._from_ext = {}
        self.update_from_file(CFD / "runner.toml")
        self.load_ancestors()

    def update(self, cfg: Dict):
        for p in cfg["profile"]:
            name = p.pop("name")
            self._configs[name] = Cfg(**p)
        for e in cfg["from_ext"]:
            self._from_ext[e["ext"]] = e["profile"]

    def update_from_file(self, path: Path):
        with path.open() as f:
            self.update(toml.load(f))

    @staticmethod
    def _get_ancestors(d: Path) -> List[Path]:
        files = []
        while True:
            f = d / "runner.toml"
            if f.exists():
                files.append(f)
            p = d.parent
            if p == d:
                break
            d = p
        return files[::-1]

    def load_ancestors(self, d=Path(".")):
        for f in self._get_ancestors(d):
            self.update_from_file(f)

    def get(self, profile: str) -> Cfg:
        return self._configs.get(profile)

    def get_from_ext(self, e: str) -> Opt[Cfg]:
        return self.get(self._from_ext.get(e))


@dataclasses.dataclass
class CliParam:
    file: str
    ext: str = "AUTO"
    profile: Opt[str] = None


mgr = CfgMgr()


def to_run_cfg(p: CliParam):
    import os

    if p.ext != "AUTO" and p.profile is not None:
        raise
    if p.profile is not None:
        assert p.ext == "AUTO"
        return mgr.get(p.profile)
    e = (
        p.ext
        if p.ext != "AUTO"
        else os.path.splitext(p.file)[1].lstrip(".")
    )
    return mgr.get_from_ext(e)


def cli():
    parser = argparse.ArgumentParser("run")
    parser.add_argument(
        "--profile",
        "-p",
        type=str,
    )
    parser.add_argument(
        "--ext",
        "-e",
        type=str,
        default="AUTO",
    )
    parser.add_argument(
        "file",
        type=str,
        # required=True,
    )
    args = parser.parse_args()
    args = CliParam(args.file, args.ext, args.profile)
    run_cfg = to_run_cfg(args)
    if run_cfg is None:
        print("no matching profile found.")
        exit(1)

    run(args.file, run_cfg)


if __name__ == "__main__":
    cli()
