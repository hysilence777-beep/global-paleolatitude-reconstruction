# Global paleolatitude reconstruction

Python code and input data for reconstructing the paleogeographic coordinates of individual samples with pyGPlates and the Merdith et al. (2021) plate-motion model.

Associated study: *Latitude-constrained low-18O magmatism links plate motion to Earth's hydrosphere-lithosphere cycle* (manuscript aeg2420).

## Scope

The script reconstructs each sample from its present-day latitude and longitude to the age specified for that sample. It uses the reconstruction plate ID already supplied in the input table. It does not assign plate IDs from polygon intersections, infer detrital source locations, filter oxygen isotope measurements, or perform the study's statistical analyses or Monte Carlo simulations.

This English-language version retains the calculations, input filenames, output fields, and error-handling behavior of the supplied original script. Only comments and console messages were translated.

## Files

| File | Description |
| --- | --- |
| `GlobalPaleolatitude-single.py` | English-language point-by-point reconstruction script. |
| `Global.csv` | Unmodified input table containing 17,143 records. This is a CSV file that can be opened in Excel. |
| `1000_0_rotfile_Merdith_et_al.rot` | Author-supplied copy of the Merdith et al. rotation model. |
| `shapes_continents_Merdith_et_al.gpmlz` | Author-supplied continental geometry file accompanying the plate model. |
| `requirements.txt` | Package versions used for the validation run. |
| `THIRD_PARTY_NOTICES.md` | Plate-model attribution, source links, and third-party licensing information. |
| `SHA256SUMS.txt` | SHA-256 checksums of the distributed files, excluding this checksum file itself. |
| `LICENSE` | MIT license for the original Python script only. |

Keep the script, CSV file, and both plate-model files together in the same working directory. The script uses relative paths, not paths relative to the script's own location.

## Input data

`Global.csv` contains the following columns. Column names are case-sensitive.

| Column | Meaning | Units or convention |
| --- | --- | --- |
| `ID` | Identifier of an input record. | Preserve the supplied identifiers and record order. |
| `Latitude` | Present-day latitude. | Decimal degrees, north positive, from -90 to 90. |
| `Longitude` | Present-day longitude. | Decimal degrees, east positive, from -180 to 180. |
| `Plate_ID` | Reconstruction plate ID compatible with the supplied rotation model. | Integer plate identifier. |
| `Age` | Reconstruction age for the individual record. | Millions of years before present (Ma). |

The distributed table spans 0.1-1000 Ma. Repeated coordinates and ages can represent different input records and are retained. The table is the reconstruction input, not a complete table of oxygen isotope measurements. Consult the associated study and its supplementary datasets for sample provenance and isotope data.

## Run

The translation was validated on Windows with Python 3.12.14, pyGPlates 1.0.0, and pandas 3.0.1. These are the validation environment versions, not a claim about the environment originally used to prepare the manuscript.

From the directory containing all four input/script files:

```bash
python GlobalPaleolatitude-single.py
```

The script prints progress for each record and writes:

```text
output_latitude_reconstruction.csv
```

Running it again in the same directory overwrites that output file. It does not modify `Global.csv` or the plate-model files.

## Output

The output CSV contains:

| Column | Description |
| --- | --- |
| `ID` | Identifier copied from the input record. |
| `Original_Latitude` | Input latitude in decimal degrees. |
| `Original_Longitude` | Input longitude in decimal degrees. |
| `Plate_ID` | Input plate ID. |
| `Age` | Input reconstruction age in Ma. |
| `Reconstructed_Latitude` | Reconstructed latitude in decimal degrees. |
| `Reconstructed_Longitude` | Reconstructed longitude in decimal degrees. |

The script uses the default reconstruction anchor of pyGPlates, plate ID 0. Reconstructed positions depend on the selected rotation model, its reference frame, the input plate IDs, and the sample ages.

## Validation and workflow notes

- All 17,143 supplied input records produced reconstructed coordinates in the validation run, with no records added to `invalid_points`.
- The original and English-language scripts produced byte-identical output CSV files in the same validation environment. No scientific calculations or input values were changed during translation.
- The continental geometry file is loaded to preserve the original workflow, but it is not used to assign plate IDs or to rotate the sample points. The supplied `Plate_ID` column and rotation model determine the reconstruction.
- Invalid coordinates or failed point reconstructions are skipped. The original error-handling behavior is retained: error details are printed and collected in memory in `invalid_points`, but no separate error file is written. When using another dataset, inspect the console messages and compare input and output record counts.
- This workflow does not quantify reconstruction uncertainty or correct for sediment transport. Such interpretation requires the geological context discussed in the associated study.

## Model attribution and citation

The model files are third-party scientific data, not new plate-model results from this repository. Please cite:

A. S. Merdith, S. E. Williams, A. S. Collins, M. G. Tetley, J. A. Mulder, M. L. Blades, A. Young, S. E. Armistead, J. Cannon, S. Zahirovic, R. D. Mueller, *Extending full-plate tectonic models into deep time: Linking the Neoproterozoic and the Phanerozoic*. Earth-Science Reviews **214**, 103477 (2021). https://doi.org/10.1016/j.earscirev.2020.103477

Original model archive: https://doi.org/10.5281/zenodo.4450249

Additional model information: [EarthByte model README](https://www.earthbyte.org/webdav/ftp/incoming/mchin/plate-models/MERDITH2021/README.txt).

The files distributed here are the copies supplied with the reconstruction script. Their exact bytes are identified by `SHA256SUMS.txt`; they have not been replaced with files from a newer model release. See `THIRD_PARTY_NOTICES.md` for rights information.

## License and availability

The original Python script is released under the MIT license in `LICENSE`. That license does not apply to `Global.csv`, the third-party model files, or third-party Python packages. The model files retain their original rights and attribution. No additional reuse license is granted to `Global.csv` by the script's MIT license.

This repository covers the paleogeographic reconstruction component and its input data. It should not be described as containing all analysis or simulation code for the associated study.
