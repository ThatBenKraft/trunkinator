# Trunkinator 🧌🦍🎨

Develop Trunk play/show rosters "with ease"!

> Using an Excel file containing Trunker schedules and role preferences, this sucker generates availabilities and rosters for each performance day like there's no tomorrow!
>
> **-- me, 2023**

Python dependencies: pandas, openpyxl

```
pip install pandas
pip install openpyxl
```

https://youtu.be/Eo1u-jO6hxI?si=IXa2bwc4j8SQ8_vX

## 🔧 Data Setup

In order to run *Trunkinator*, the Excel file being used must be in the correct format. By default, `trunker_data.xlsx` is run within the same directory as `trunkinator.py`. For a new show, I would recommend copying a previous sheet and just replacing the names and days. Each sheet of `trunker_data.xlsx` should use the following layout:

**[ x ]** = Insert element of *x* name or value into cell.

**...** = Continue trend from left/right columns.

| Trunker | [Role#1] | ... | [Role#5] | [Day#1] | ... | [Day#3] |
|---------|-----------|-------|-----------|----------|-------|----------|
| [Trunker#1] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#2] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#3] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#4] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |
| [Trunker#5] | [true/false] | ... | [true/false] | [true/false] | ... | [true/false] |

Here, I assumed there were five roles, three days, and five Trunkers (yikes 🥲). The number of Trunkers can be easily manipulated by simply adding/removing rows at the bottom. However, at the moment, changing the number of *roles* or *performance days* is somewhat difficult. If needed, there are two hard-coded constants towards the top of `trunkinator.py` named `NUM_ROLES` and `NUM_DAYS`, but if you are having trouble finding/setting those, just shoot me an email and I'll add an input method.

## ▶️ Running *Trunkinator*

There are two options for running *Trunkinator*. You can either run it in a popup window that looks like it's from the 90's but easy to use, or from your terminal. All you have to do is run the corresponding `.py` file. Both versions will ask for a show name, which is just the name of the Excel sheet on which the data is. Likely something to the effect of "Trash Mountain (2)" if you forgot to rename it. I haven't put in input linting so make sure the name is exactly correct.

If you don't want to ever look at the terminal or don't know how to, simply right-click `trunkinator_popup.py` and open it with Python directly.

If you are fine with using the terminal, go ahead and run `trunkinator_terminal.py` directly or in a text editor.

For non-baby show week rosters, I recommend simply copying an existing full-trunker sheet and deleting the babies (also the name of my new cover band).

## ❌ Troubleshooting

The most expected issue is not having the right dependencies. If you don't have pip to install these, try watching [this video if you're on a Mac](https://youtu.be/ioZoC8_Hk7o?si=ZxjolHqZpdqMNshC) or [this video if you're on a Windows computer](https://youtu.be/CWbT-E7f73w?si=_4cu6d-EZCaBUJwt) (If you're on Linux, somehow I think you've got this part figured out). If you run into errors, make sure they stem from the Python file itself and really, *REALLY* look at what you're typing and how you formatted the Excel sheet. If the problems keep up, email me, I likely just messed up somewhere.
