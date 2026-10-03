# Team Conventions

> Fill this in during module 0 with your mentor. Examples show the **format** of an entry, not the decision.
> Status: ☐ draft ☐ reviewed by mentor ☐ adopted. Reviewer: ______ Commit: ______

## 1. Frame names

| Frame id | Description | Origin | Axes (x / y / z) | Reference doc |
|---|---|---|---|---|
| `______` | | | | |
| `______` | | | | |

*Format example:* `` `<name>` | <what it is attached to> | <where the origin is> | <x dir> / <y dir> / <z dir> | <datasheet or devkit section> ``

## 2. Transform naming

- Symbol meaning: `T_a_b` = ______________________________________
- Composition rule, written out: `T_a_c = ______ * ______`
- Point transform, written out: `p_a = ______ * p_b`
- Variable naming in code: ______ (format example: `<type>_<to>_<from>`)

## 3. Rotations and quaternions

- Convention (Hamilton / JPL): ______
- Storage order in memory and files (`wxyz` / `xyzw`): ______
- Library notes (which libraries use which order): ______
- Sign: canonical hemisphere enforced? ☐ yes (rule: ______) ☐ no
- Euler angles allowed in: ______ (sequence: ______)

## 4. Units

| Quantity | Unit | Notes |
|---|---|---|
| Length | | |
| Angle | | |
| Time | | |
| Angular rate | | |
| Acceleration | | |
| Latitude / longitude | | |

## 5. Time

- Timestamp source (sensor clock / host clock / GNSS time): ______
- Epoch: ______
- Representation (type and resolution): ______
- Synchronization method between sensors: ______
- Rule for which timestamp a scan carries (first point / last point / mid): ______

## 6. Geodesy

- Datum / ellipsoid: ______
- Local frame type (ENU / NED): ______
- Local origin definition: ______

## 7. Code and data

- File formats for trajectories: ______ (format example: `<name> — <column order>`)
- Config file format and location: ______
- Experiment record must include: ______

## 8. Open questions / decisions log

| Date | Decision | Reason | Decided by |
|---|---|---|---|
| | | | |
