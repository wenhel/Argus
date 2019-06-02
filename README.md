

## Introduction
Argus is an AI Surveillance System for Spatial-Temporal Activity Detection in Surveillance Scenarios. In this year's [ACTEV Challenge](https://actev.nist.gov/prizechallenge#tab_leaderboard), two teams used the system in thie Challenge, they are MUDSML from Monash University and INF from Carnegie Mellon University. This system helps them wins the first and the second place in the Phase 1 challenge. 

The prototype system was first implemented for SED project start from 2017. The code of the pipeline is developed as a docker based system. Later in the ACTEV Challenge we merge the system with the ACTEV CLI an created the current system Argus. [Argus](https://en.wikipedia.org/wiki/Argus_Panoptes) is a many-eyed giant in Greek mythology.

![Leaderboard of Phase 1](https://github.com/wenhel/Argus/blob/master/Intro/leaderboad.png)

## The Architecture
![Architecture](https://github.com/wenhel/Argus/blob/master/Intro/pipeline_sx.png)

## Run with the ACTEV CLI
![Run with the ACTEV CLI Part 1](https://github.com/wenhel/Argus/blob/master/Intro/pipeline_s1.png)
![Run with the ACTEV CLI Part 2](https://github.com/wenhel/Argus/blob/master/Intro/pipeline_s2.png)

## Implementation
### Running with Dockerized Models
![GPU Management](https://github.com/wenhel/Argus/blob/master/Intro/pipeline_s4.png)

### GPU Management
![GPU Management](https://github.com/wenhel/Argus/blob/master/Intro/pipeline_s3.png)


## The Current Pipeline
![Architecture](https://github.com/wenhel/Argus/blob/master/Intro/actev_pipeline.png )

## Demos
We run our pipeline on several videos recorded by surveillance cameras. 

![](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_010113_03_000505_000639.png)
Vehicle and Person-Vehicle Activities [full video](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_010113_03_000505_000639.mp4)

![](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_040005_10_001453_001515.png)
Person-Vehicle Activities  [full video](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_040005_10_001453_001515.mp4)

![](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_040203_03_000938_001490.png)
Vehicle Activities [full video](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_040203_03_000938_001490.mp4)

![](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_050101_09_001427_001474.png)
Person Activities [full video](https://www.andrew.cmu.edu/user/wenhel/demos/project1/VIRAT_S_050101_09_001427_001474.mp4)