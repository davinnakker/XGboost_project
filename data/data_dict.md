# Housing Dataset — Data Dictionary

This document describes the fields contained in the housing dataset.

| Column Name | Description |
|---|---|
| `id` | Unique ID for each home sold |
| `date` | Date of the home sale |
| `price` | Sale price of the home |
| `bedrooms` | Number of bedrooms |
| `bathrooms` | Number of bathrooms, where `.5` represents a bathroom with a toilet but no shower |
| `sqft_living` | Square footage of the interior living space |
| `sqft_lot` | Square footage of the land lot |
| `floors` | Number of floors in the home |
| `waterfront` | Binary variable indicating whether the home overlooks a waterfront |
| `view` | Rating of the property view quality on a scale from `0` to `4` |
| `condition` | Rating of the home's condition on a scale from `1` to `5` |
| `grade` | Construction and design quality rating on a scale from `1` to `13`:<br>- `1–3`: Below average construction/design<br>- `7`: Average construction/design<br>- `11–13`: High-quality construction/design |
| `sqft_above` | Square footage of interior living space above ground level |
| `sqft_basement` | Square footage of interior living space below ground level |
| `yr_built` | Year the house was originally built |
| `yr_renovated` | Year of the home's most recent renovation |
| `zipcode` | ZIP code where the property is located |
| `lat` | Latitude coordinate |
| `long` | Longitude coordinate |
| `sqft_living15` | Average interior living space square footage of the nearest 15 neighboring homes |
| `sqft_lot15` | Average land lot square footage of the nearest 15 neighboring homes |

---

## Notes

- Square footage values are measured in square feet.
- Neighbor-based features (`sqft_living15` and `sqft_lot15`) provide local neighborhood context for each property.
- Ratings such as `view`, `condition`, and `grade` are ordinal scales where higher values indicate better quality.