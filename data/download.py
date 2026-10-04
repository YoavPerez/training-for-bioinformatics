"""Dataset fetchers.

    python data/download.py --sample                         # CI subset (~150 MB download)
    python data/download.py --drive 2011_09_30_drive_0027    # full KITTI raw drive (sync)
    python data/download.py --drive 2011_09_30_drive_0027 --extract-oxts   # + 100 Hz OXTS
    python data/download.py --static-imu                     # module 3: 16 h static IMU (MILUV, ~1.7 GB download)

LICENSE NOTICE. KITTI is published under Creative Commons Attribution-NonCommercial-ShareAlike 3.0
(https://www.cvlibs.net/datasets/kitti/raw_data.php). It may be used for training and research only,
NOT for commercial purposes. Cite Geiger et al., "Vision meets Robotics: The KITTI Dataset", IJRR 2013.

MILUV (static IMU, module 3) is CC BY 4.0: Shalaby et al., "MILUV: A Multi-UAV Indoor Localization dataset
with UWB and Vision", https://doi.org/10.25452/figshare.plus.28386041.v1

The sample keeps the KITTI directory layout (velodyne + OXTS only, images skipped) under
data/samples/kitti/, and adds data/samples/skewed/scan.npz for the module 3 deskew exercise.
"""

import argparse
import io
import sys
import urllib.request
import zipfile
from pathlib import Path

import numpy as np

BASE_URL = "https://s3.eu-central-1.amazonaws.com/avg-kitti/raw_data"
DATA_DIR = Path(__file__).resolve().parent
SAMPLE_DRIVE = "2011_09_26_drive_0002"
LICENSE = "KITTI raw: CC BY-NC-SA 3.0 — non-commercial research and training use only."


class HttpRangeFile(io.RawIOBase):
    """Seekable read-only file over HTTP range requests, so zip members can be fetched selectively."""

    def __init__(self, url: str, block: int = 1 << 20):
        self.url = url
        self.block = block
        self.pos = 0
        self.cache: dict[int, bytes] = {}
        # Size from a 1-byte range GET (pre-signed URLs often reject HEAD requests).
        with urllib.request.urlopen(urllib.request.Request(url, headers={"Range": "bytes=0-0"})) as r:
            self.size = int(r.headers["Content-Range"].split("/")[-1])

    def readable(self) -> bool:
        return True

    def seekable(self) -> bool:
        return True

    def tell(self) -> int:
        return self.pos

    def seek(self, offset: int, whence: int = 0) -> int:
        self.pos = {0: offset, 1: self.pos + offset, 2: self.size + offset}[whence]
        return self.pos

    def _block(self, i: int) -> bytes:
        if i not in self.cache:
            start = i * self.block
            end = min(start + self.block, self.size) - 1
            req = urllib.request.Request(self.url, headers={"Range": f"bytes={start}-{end}"})
            with urllib.request.urlopen(req) as r:
                self.cache[i] = r.read()
            if len(self.cache) > 64:
                self.cache.pop(next(iter(self.cache)))
        return self.cache[i]

    def readinto(self, b) -> int:
        n = min(len(b), self.size - self.pos)
        out = bytearray()
        while len(out) < n:
            i, off = divmod(self.pos + len(out), self.block)
            out += self._block(i)[off : off + n - len(out)]
        b[:n] = out
        self.pos += n
        return n


def fetch_members(url: str, dest: Path, keep) -> int:
    """Extracts zip members for which keep(name) is true. Returns the number of files written."""
    with zipfile.ZipFile(io.BufferedReader(HttpRangeFile(url), buffer_size=1 << 20)) as z:
        names = [n for n in z.namelist() if not n.endswith("/") and keep(n)]
        for k, name in enumerate(names, 1):
            target = dest / name
            if target.exists():
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(z.read(name))
            if k % 25 == 0 or k == len(names):
                print(f"  {k}/{len(names)} files", file=sys.stderr)
        return len(names)


def fetch_calib(date: str, dest: Path) -> None:
    fetch_members(f"{BASE_URL}/{date}_calib.zip", dest, lambda n: n.endswith(".txt"))


def fetch_drive(drive: str, dest: Path, sensors=("oxts", "velodyne_points"), kind: str = "sync") -> Path:
    date = drive[:10]
    url = f"{BASE_URL}/{drive}/{drive}_{kind}.zip"
    print(f"fetching {url} ({', '.join(sensors)})", file=sys.stderr)
    fetch_members(url, dest, lambda n: any(f"/{s}/" in n for s in sensors))
    fetch_calib(date, dest)
    return dest / date / f"{drive}_{kind}"


# --- module 3 skewed sample --------------------------------------------------------------------

SKEW_YAW_RATE = np.radians(45.0)  # [rad/s] synthetic rotation added on top of the recorded motion
SWEEP = 0.1  # [s] one revolution of the HDL-64E


def _yaw(a: float) -> np.ndarray:
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def make_skewed_sample(drive_dir: Path, out: Path, frame: int = 40) -> None:
    """Takes one KITTI raw scan as the reference and adds strong synthetic motion distortion.

    The raw scan's own (small) distortion is ignored: the scan is treated as the undistorted reference.
    The sensor is assumed to translate with the recorded OXTS velocity and to rotate with a synthetic
    45 deg/s yaw rate. Each point gets a timestamp from its azimuth within a 0.1 s sweep.
    Saved arrays: points (skewed, sensor frame at each point's time), times, reference (undistorted,
    sensor frame at t_ref = 0), traj_t and traj_T (T_world_sensor samples covering the sweep).
    """
    sys.path.insert(0, str(DATA_DIR.parent / "pipeline" / "python"))
    from slampipe import kitti

    drive = kitti.Drive(drive_dir)
    pts = drive.scan(frame)[:, :3].astype(float)
    pts = pts[np.linalg.norm(pts, axis=1) > 3.0][::4]  # thin out for test speed
    v = float(drive.oxts().vf[frame])

    azimuth = np.mod(-np.arctan2(pts[:, 1], pts[:, 0]), 2 * np.pi)  # clockwise sweep from +x
    times = azimuth / (2 * np.pi) * SWEEP

    traj_t = np.linspace(0.0, SWEEP, 21)
    traj_T = np.repeat(np.eye(4)[None], traj_t.size, axis=0)
    for k, t in enumerate(traj_t):
        traj_T[k, :3, :3] = _yaw(SKEW_YAW_RATE * t)
        traj_T[k, :3, 3] = [v * t, 0.0, 0.0]

    skewed = np.empty_like(pts)
    for i, (p, t) in enumerate(zip(pts, times, strict=True)):
        R, tr = _yaw(SKEW_YAW_RATE * t), np.array([v * t, 0.0, 0.0])
        skewed[i] = R.T @ (p - tr)  # T_world_sensor(t)^-1 applied to the point at t_ref = 0
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        out / "scan.npz",
        points=skewed,
        times=times,
        reference=pts,
        traj_t=traj_t,
        traj_T=traj_T,
        note=np.array(f"KITTI {drive_dir.name} frame {frame}; synthetic yaw rate 45 deg/s; {LICENSE}"),
    )


# --- module 3 static IMU recording (MILUV) -----------------------------------------------------

MILUV_IMU_ZIP = "https://ndownloader.figshare.com/files/52251866"  # imu_calib.zip, CC BY 4.0
MILUV_ROBOT = "ifo001"
# Flight-controller IMU, 16 h static. Nominal 200 Hz in the authors' config; derive the real rate from t.
MILUV_TOPIC = "/mavros/imu/data_raw"


def fetch_static_imu(dest: Path) -> Path:
    """Extracts one MILUV static IMU bag, converts its IMU topic to npz (t, acc, gyro), deletes the bag.

    Also keeps the dataset authors' own Allan-variance results (yaml, csv, png) for comparison.
    Needs ~11 GB of temporary disk space and the `rosbags` package (pure Python, no ROS install).
    """
    import shutil

    import numpy as np
    from rosbags.highlevel import AnyReader

    dest.mkdir(parents=True, exist_ok=True)
    out = dest / f"{MILUV_ROBOT}_mavros_imu.npz"
    if out.exists():
        return out
    # Figshare redirects to S3 links that expire after seconds: keep the stable URL so that every range
    # request follows a fresh redirect.
    with zipfile.ZipFile(io.BufferedReader(HttpRangeFile(MILUV_IMU_ZIP, block=8 << 20), buffer_size=8 << 20)) as z:
        prefix = f"imu_calib/{MILUV_ROBOT}/"
        for name in z.namelist():
            if name.startswith(prefix) and name.endswith((".yaml", ".csv", ".png", ".log", ".config")):
                (dest / Path(name).name).write_bytes(z.read(name))
        bag_name = next(n for n in z.namelist() if n.startswith(prefix) and n.endswith(".bag"))
        bag = dest / Path(bag_name).name
        if not bag.exists():  # a previous run may have extracted it already
            print(f"extracting {bag_name} (~11 GB uncompressed) ...", file=sys.stderr)
            with z.open(bag_name) as src, open(bag.with_suffix(".part"), "wb") as dst:
                shutil.copyfileobj(src, dst, length=16 << 20)
            bag.with_suffix(".part").rename(bag)
    print("converting the IMU topic (takes a while) ...", file=sys.stderr)
    t, acc, gyro = [], [], []
    with AnyReader([bag]) as reader:
        conns = [c for c in reader.connections if c.topic == MILUV_TOPIC]
        if not conns:  # an empty list would make rosbags read every topic
            sys.exit(f"topic {MILUV_TOPIC} not in bag; topics: {sorted({c.topic for c in reader.connections})}")
        for conn, _, raw in reader.messages(connections=conns):
            m = reader.deserialize(raw, conn.msgtype)
            t.append(m.header.stamp.sec + 1e-9 * m.header.stamp.nanosec)
            acc.append((m.linear_acceleration.x, m.linear_acceleration.y, m.linear_acceleration.z))
            gyro.append((m.angular_velocity.x, m.angular_velocity.y, m.angular_velocity.z))
    np.savez(
        out,
        t=np.array(t),
        acc=np.array(acc),
        gyro=np.array(gyro),
        note=np.array(f"MILUV {MILUV_ROBOT} {MILUV_TOPIC}, static, CC BY 4.0"),
    )
    bag.unlink()
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--sample", action="store_true", help="download the CI sample subset")
    parser.add_argument("--drive", help="full KITTI raw drive, e.g. 2011_09_30_drive_0027")
    parser.add_argument("--extract-oxts", action="store_true", help="also fetch 100 Hz OXTS (unsynced extract)")
    parser.add_argument("--static-imu", action="store_true", help="16 h static IMU recording for module 3")
    parser.add_argument("--dest", type=Path, default=DATA_DIR / "kitti")
    args = parser.parse_args()
    print(LICENSE, file=sys.stderr)

    if args.sample:
        dest = DATA_DIR / "samples" / "kitti"
        drive_dir = fetch_drive(SAMPLE_DRIVE, dest)
        make_skewed_sample(drive_dir, DATA_DIR / "samples" / "skewed")
        print(f"sample ready: {drive_dir}", file=sys.stderr)
    if args.drive:
        drive_dir = fetch_drive(args.drive, args.dest)
        if args.extract_oxts:
            fetch_drive(args.drive, args.dest, sensors=("oxts",), kind="extract")
        print(f"drive ready: {drive_dir}", file=sys.stderr)
    if args.static_imu:
        out = fetch_static_imu(DATA_DIR / "static_imu")
        print(f"static IMU ready: {out}", file=sys.stderr)
    if not (args.sample or args.drive or args.static_imu):
        parser.print_help()


if __name__ == "__main__":
    main()
