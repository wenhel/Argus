

## Introduction
Argus is an AI Surveillance System for Spatial-Temporal Activity Detection in Surveillance Scenarios. In this year's [ACTEV Challenge](https://actev.nist.gov/prizechallenge#tab_leaderboard), two teams used the system in thie Challenge, they are MUDSML from Monash University and INF from Carnegie Mellon University. This system helps them wins the first and the second place in the Phase 1 challenge. 

The prototype system was first implemented for SED project start from 2017. The code of the pipeline is developed as a docker based system. Later in the ACTEV Challenge we merge the system with the ACTEV CLI an created the current system Argus. [Argus](https://en.wikipedia.org/wiki/Argus_Panoptes) is a many-eyed giant in Greek mythology.

![Leaderboard of Phase 1](intro/leaderboad.png)

## The Architecture
![Architecture](intro/pipeline_sx.png)

## Run with the ACTEV CLI
![Run with the ACTEV CLI Part 1](intro/pipeline_s1.png)
![Run with the ACTEV CLI Part 2](intro/pipeline_s2.png)

## Implementation
### Running with Dockerized Models
![GPU Management](intro/pipeline_s4.png)

### GPU Management
![GPU Management](intro/pipeline_s3.png)


## The Current Pipeline
![Architecture](intro/actev_pipeline.png )