# LabGym: quantifying user-defined behaviors
<!-- start elevator-pitch -->
LabGym can:

1. **TRACK** multiple animals / objects without restrictions on recording environments
2. **IDENTIFY** user-defined social or non-social behaviors without restrictions on behavior types / animal species
3. **QUANTIFY** user-defined behaviors by providing quantitative measures for each behavior
4. **MINE** the analysis results to show statistically significant findings

A tutorial video for a high-level understanding of what LabGym can do, how it works, and how to use it:

[![Watch the video](https://img.youtube.com/vi/YoYhHMPbf_o/hqdefault.jpg)](https://youtu.be/YoYhHMPbf_o)


Cite LabGym: https://www.cell.com/cell-reports-methods/fulltext/S2667-2375(23)00026-7.

<!-- end elevator-pitch -->

<p>&nbsp;</p>

## Identifies user-defined behaviors

LabGym is equipped with three distinct modes of behavior identification to suit different scenarios:

1. **'Interactive advanced'**

   This mode is for analyzing the behavior of each individual in a group of animals or objects. Below are two examples. Left: LabGym can differentiate between a finger 'holding a peanut' vs. 'offering a peanut', discern whether a chipmunk is 'taking the offer' or 'loading peanut', and identify the status of the peanut itself as 'being held', 'being taken', or 'being loaded'. Right: it can distinguish in a group of flies which fly is 'singing’ a courtship song, which one is ‘being courted’, which one is ‘resting’, and which one is ‘locomotion’.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_chipmunks_1.gif?raw=true)    ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_flies_1.gif?raw=true)

2. **'Interactive basic'**

   Optimized for speed, this mode considers the entire interactive group (2 or more individuals) as an entity, streamlining the processing time compared to the **'Interactive advanced'** mode. It is ideal for scenarios where individual behaviors within the group are uniform or when the specific actions of each member are not the primary focus of the study.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_chipmunks_2.gif?raw=true)    ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_flies_2.gif?raw=true)

3. **'Non-interactive'**

   This mode is for identifying solitary behaviors of individuals that are not engaging in interactive activities. It is suitable for studies where the emphasis is on non-social or independent behaviors.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_mice_1.gif?raw=true)    ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_mice_2.gif?raw=true)

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_larvae.gif?raw=true)    ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Categorizer_rats.gif?raw=true)

<p>&nbsp;</p>

## Quantifies user-defined behaviors

LabGym computes a range of motion and kinematics parameters for each behavior defined by users. The parameters include **count**, **duration**, and **latency** of behavioral incidents, as well as **speed**, **acceleration**, **distance traveled**, and the **intensity** and **vigor** of motions during the behaviors. LabGym outputs these parameters in spreadsheets.

![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Analysis_output.jpg?raw=true)

<p>&nbsp;</p>

LabGym also provides visualization of analysis results, including annotated videos that visually mark each behavior event, temporal raster plots that show every behavior event overtime. The temporal raster plots below were output by LabGym and show the changes in behavior events of rodent before and after amphetamine treatments (See detailed explanation in Hu et al. (2023) Cell Reports Methods 3(3): 100415).

![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Quantify%20behavior.jpg?raw=true)

<p>&nbsp;</p>

## Mines the analysis results

LabGym outputs diverse spreadsheets that store the behavior parameters that it calculates. It is labor intensive to dig into these spreadsheets manually for statistical analysis across different experimental groups and behavioral types and parameters. To address this, LabGym contains a data-mining module that automatically performs the statistical tests on every behavioral parameter across the experimental groups of your choice. The data-mining result below displays the details of the comparisons that show statistically significant differences between groups.

![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Results_mining.jpg?raw=true)

<p>&nbsp;</p>

## Accessible and User-Friendly

LabGym eliminates the need for coding due to its intuitive user interface, ensuring ease of use for all users regardless of their programming skills. While the software operates efficiently without GPUs, it can achieve enhanced speed on systems equipped with NVIDIA GPUs and the CUDA toolkit (version==11.7) installed.

<p>&nbsp;</p>

# How to use LabGym?

Extended user guide: (https://github.com/yujiahu415/LabGym/blob/master/LabGym%20user%20guide_v2.2.pdf).

***Put your mouse cursor above each button in the user interface to see a detailed description for it***.

<p>&nbsp;</p>

![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/User%20interface.jpg?raw=true)

<p>&nbsp;</p>

LabGym comprises three modules, each tailored to streamline the analysis process. Together, these modules create a cohesive workflow, enabling users to prepare, train, and analyze their behavioral data with accuracy and ease.

1. **'Preprocessing Module'**: This module is for optimizing video footage for analysis. It can enhance video contrast to make the relevant details more discernible. It can trim videos to focus solely on the necessary time windows. It can also crop frames to remove irrelevant regions.

2. **'Training Module'**: Here, you can customize LabGym according to your specific research needs. You can train a Detector in this module to detect animals or objects of your interest in videos. You can also train a Categorizer to recognize specific behaviors that are defined by you.

3. **'Analysis Module'**: After customizing LabGym to your need, you can use this module for automated behavioral analysis in videos. It not only outputs comprehensive analysis results but also delves into these results to mine significant findings.

<p>&nbsp;</p>

## How to teach LabGym to recognize behaviors defined by you

Follow these three steps (three buttons in the **‘Training Module’**):

1. **'Generate Behavior Examples'**: Use this button to input your video files and let LabGym generate behavior examples from these videos. Each behavior example is comprised of an **Animation** paired with a **Pattern Image**, spanning a specific behavior episode that is defined by you.

2. **'Sort Behavior Examples'**: Once your behavior examples are generated, use this button to select appropriate examples and sort them according to their behavior types.

3. **'Train Categorizers'**: Finally, use this button to feed the sorted behavior examples into the system to train a Categorizer. The trained Categorizer is stored in LabGym and can categorize these behaviors automatically in future analyses.

LabGym has three modes of behavior identification, so it offers three modes for behavior examples:

1. **'Interactive advanced'**

   In this mode, each pair of **Animation** and **Pattern Image** highlights an entire interactive group, with a 'spotlight' focusing on the main character. The categorization is based on the main character’s behavior. In the example below, behaviors of the chipmunk ('taking the offer'), the peanuts ('being taken' and 'being held'), and the hand ('offering peanut') can be distinguished.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Chipmunks.gif?raw=true)

2. **'Interactive basic'**

   This mode captures all relevant animals or objects in each pair of **Animation** and **Pattern Image**. Sort these as one collective unit. In the following example of fly courtship behavior, behaviors like 'orientating', 'singing while licking', and 'attempted copulation' could be categorized, focusing on specific actions like the courtship steps of a male fly while disregarding the female's response, if the research focuses only on male courtship behaviors.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Flies.gif?raw=true)

3. **'Non-interactive'**

   Each pair of **Animation** and **Pattern Image** in this mode represents a 'monodrama', focusing solely on individual animals or objects without interaction.

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Mice.gif?raw=true)

   ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Larvae.gif?raw=true)

<p>&nbsp;</p>

## How does LabGym detect animals / objects?

LabGym employs two distinct methods for detecting animals or objects in different scenarios.

1. **Subtract background**

   This method is fast and accurate but requires stable illumination and static background in videos to analysis. It does not require training neural networks, but you need to define a time window during which the animals are in motion for effective background extraction. A shorter time window leads to quicker processing. Typically, a duration of 10 to 30 seconds is adequate.

    ***How to select an appropriate time window for background extraction?***

    To determine the optimal time window for background extraction, consider the animal's movement throughout the video. In the example below, in a 60-second video, selecting a 20-second window where the mouse moves frequently and covers different areas is ideal. The following three images are backgrounds extracted using the time windows of the first, second, and last 20 seconds, respectively. In the first and last 20 seconds, the mouse mostly stays either in left or right side and moves little and the extracted backgrounds contain animal trace, which is not ideal. In the second 20 seconds, the mouse frequently moves around and the extracted background is perfect:

    ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Background_extraction_demo.gif?raw=true)  ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Extracted_background_0-20.jpg?raw=true)  ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Extracted_background_20-40.jpg?raw=true)  ![alt text](https://github.com/yujiahu415/LabGym/blob/master/Examples/Extracted_background_40-60.jpg?raw=true)

2. **Use trained Detectors**

   This method incorporates Detectron2 (https://github.com/facebookresearch/detectron2), offering more versatility but at a slower processing speed compared to the **‘Subtract Background’** method. It excels in differentiating individual animals or objects, even during collisions, which is particularly beneficial for the **'Interactive advanced'** mode. To enhance processing speed, use a GPU or reduce the frame size during analysis. To train a **Detector** in **‘Training Module’**: 

    1. Click the **‘Generate Image Examples’** button to extract image frames from videos.
    2. Use free online annotation tools like Roboflow (https://roboflow.com) to annotate the outlines of animals or objects in these images. For annotation type, choose 'Instance Segmentation', and export the annotations in 'COCO instance segmentation' format, which generates a ‘*.json’ file. In **'Interactive advanced'** mode, focus on images where individuals collide and annotate these boundaries precisely. Exposing the **Detector** to a variety of collision scenarios during training can significantly minimize identity switching in subsequent analyses.
    3. Use the **‘Train Detectors’** button to input these annotated images and commence training your **Detectors**.

<p>&nbsp;</p>

# Installation

1. Install Python3 (version >= 3.9.7)

    Do not install the latest version of Python3 since it might not be compatible yet.

2. In your terminal / cmd prompt, type:

        python3 -m pip install LabGym

3. If want to use **Detectors**, after LabGym is installed, install Detectron2 separately (https://detectron2.readthedocs.io/en/latest/tutorials/install.html):

        python3 -m pip install 'git+https://github.com/facebookresearch/detectron2.git'

<p>&nbsp;</p>

# Initiate user interface for each use

First, you need to activate python3 in your terminal / CMD by typing:

      python3

After python3 is activated, type:

      from LabGym import gui

And then type:

      gui.gui()

Now the user interface is inititated and ready to use

<p>&nbsp;</p>

# If you encounter any issues when using LabGym:

Refer to the open / closed issues or open a new issue or contact the author: Yujia Hu (henryhu@umich.edu).

For instructions on how to contribute to LabGym, please see [CONTRIBUTING.md](./CONTRIBUTING.md).

<p>&nbsp;</p>

# Changelog:

**v2.2**:

1. Added functions of testing Detectors / Categorizers so that the accuracy of a trained Detector / Categorizer can be tested and reported.
2. Added behavior mode 'Static image' so that LabGym can now analyze behaviors in static images.
3. Made the spreadsheets for storing behavioral metrics transposed so that they can be more compatible with other platforms.
4. Other minor optimizations.

**v2.1**:

1. Improved the user interface and the Extended User Guide. 
2. Added a tutorial video.

**v2.0**:

1. Implemented the analysis pipeline for complex interactive behaviors. 
2. Major improvement on analysis speed.
3. Bug fix.

**v1.9**:

1. Implemented Detector-based detection method. Now the changing background or illumination in videos is no longer a problem for LabGym. 
2. Implemented data mining functional unit.
3. Implemented preprocessing functional unit.
4. Simplified code and further optimized the processing speed.
5. Implemented basic analysis for interactive behavior.

**v1.8**:

1. In previous versions, if no animal is detected in a frame, this frame will be skipped. From now on, such frames will not be skipped, and the behavioral classification and quantification will be output as 'NA's so that the raster plots and the quantification results can be perfectly aligned for every frame with other data (e.g., ephys recordings).
2. An 'uncertain level' can be added into the Categorizers for reducing the false positives in behavior classification. The Categorizer will output an ‘NA’ if the difference between probability of the highest-likely behavior and the second highest-likely behavior is less than the uncertainty level.
3. Simplified the user interface. 
4. Optimized the processing speed.

**v1.7**:

1. Improved the background extraction and the tracking, making them faster and more accurate. 

**v1.6**:

1. Added a version checker. If a newer version of LabGym is available, users will see a reminder when initiate the user interface. 

**v1.5**:

1. Simplified the user interface and made it more self-illustrative.
2. Added an option of whether to output the distances in pixels when calculating behavior parameters. Previously all the distances were just normalized by the size of a single animal.

**v1.4**:

1. Made the time points in the output time-series sheets more precise.
2. Fixed an error when using the option of 'load background image'.

**v1.3**:

1. Improved background subtraction and the tracking is more accurate.
2. Now LabGym not only can work for videos with illumination transitions from dark to bright, but can also work for those from bright to dark.

**v1.2**:

1. Now LabGym can also be used in categorizing binary behaviors (yes or no behavior, or behaviors with only 2 categories)
2. Fixed a bug that caused a path error if users did not select any behavior parameters for quantification.
3. Now users have an option to choose whether to relink newly detected animals to deregistered IDs.

**v1.1**:

1. Changed a typo in setup.

**v1.0**:

Initial release.

<p>&nbsp;</p>
