# trunkinator 🧌🦍🎨

Develop Trunk play/show rosters "with ease"!

> Using an Excel file containing Trunker schedules and role preferences, this sucker generates availabilities and rosters for each performance day like there's no tomorrow!
>
> **-- me, 2023**

Python dependencies: pandas, openpyxl

## 🔧 Data Setup

In order to run *Trunkinator*, the excel file being used must be in the correct format. By default, `trunker_data.xlsx` is run within the same directory as `trunkinator.py`. For a new show, I would recommend copying a previous sheet and just replacing the names and days. Each sheet of `trunker_data.xlsx` should use the following layout:

**[ ✖️ ]** = Insert element of *✖️* name into cell.

**...** = Continue trend from left/right columns.

| Trunker | [Role#1] | ... | [Role#5] | [Day#1] | ... | [Day#3] |
|---------|-----------|-------|-----------|----------|-------|----------|
| [Trunker#1] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#2] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#3] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#4] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#5] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |

Here, I assumed there were five roles, three days, and five trunkers (yikes 🥲). The number of trunkers can be easily manipulated by simply adding more rows. However, if this number of roles or performance days is not correct, I have not implemented an input method so if you can't figure out how to correct the hard-coded values yourself, (there's two variables at the top of `print_shows()` named `num_roles` and `num_days`) just shoot me an email and I'll add it.

## ▶️ Running *Trunkinator*

You can run *Trunkinator* by simply running `trunkinator.py`. It will ask for a show name, which is just the name of the Excel sheet on which the data is. Likely something to the effect of "Trash Mountain (2)" if you forgot to rename it. I haven't put in input linting so make sure the name is exactly correct.

For non-baby show week rosters, I would recommend simply making a sheet with all trunkers and then copy it and Delete the Babies.

## ❌ Troubleshooting

If you run into errors, just try it again and really, *REALLY* look at what you're typing and how you formatted the Excel sheet. If it keeps up, just email me, I probably messed up somewhere.
