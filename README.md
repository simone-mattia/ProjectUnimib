# University of Milano-Bicocca Projects

## RDP Bruteforce Anomaly Detection
- Anomaly detection model that allows to distinguish legitimate RDP login from bruteforce attempts;
- The model has been trained with three different training sets that vary only for anomalous traffic:
  - the first one has been created using the most common bruteforce tools;
  - the second by an [internally developed tool](AnomalyDetectionBruteRDP/brute.py);
  - the third is the union of the first two training sets;
- The aim is to validate the hypothesis that it is essential to work on a heterogeneous dataset to avoid false negative.

## SpotifyTop200
- Descriptive and inferential analysis of Spotify top 200 songs between 2017-2021;
- Project for the exam of "Foundations of Probability and Statistics";
- [Here](SpotifyTop200/README.md) you can find the report.