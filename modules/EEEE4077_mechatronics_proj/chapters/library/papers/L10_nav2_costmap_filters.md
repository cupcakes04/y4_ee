# L10: Nav2 Costmap Filters: Keepout Zones and Speed Limits

- **Key:** L10
- **Authors:** ROS 2 Nav2 Maintainers & Documentation
- **Venue / Year:** ROS 2 Official Documentation (Rolling/Jazzy), 2024–2026
- **Status:** S (Verified page structure and title; full body inspection pending)

---

## Technical Summary
Details the implementation and operation of **Nav2 Costmap Filters**. Costmap Filters utilize spatial grid masks published alongside `CostmapFilterInfo` metadata to apply rule-based modulations directly onto costmaps without modifying static occupancy maps. Key filter implementations include:
1. **Keepout Zones:** Mark specific geometric polygons as impassable hazards.
2. **Speed Limits:** Modulate maximum permissible linear robot velocity when operating within designated corridors.

---

## Project Relevance & Usage
- **Downstream Consumer (Module 1):** Provides the official ROS 2 architectural interface for receiving our projected planar hazard polygons directly into navigation planning without manual CAD interventions.

---

## BibTeX
```bibtex
@misc{nav2_costmap_filters,
  author       = {{Nav2 Development Team}},
  title        = {Navigating with Costmap Filters: Keepout Zones and Speed Limits},
  year         = {2024},
  howpublished = {\url{https://docs.nav2.org/configuration/packages/configuring-costmap-filters.html}}
}
```
