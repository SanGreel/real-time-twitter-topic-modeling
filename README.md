## Real-time Twitter topic modeling with PySpark
  The main purpose of this solution is to identify the topics under active discussion at the moment in a certain area.<br/>
  As the published news articles can be distorted and there is a delay between the actual event and publication in the news. Both of these factors are critical for market players, and those who have instant access to reliable information have a clear advantage.<br/>
  As a source, we chose Twitter because of its popularity and prevalence throughout the world, legitimate access to real-time data and the many topics discussed in it.<br/>
As an example, there are many cases when companies use Twitter to identify vulnerability in their security systems since information about it often comes in social networks.<br/><br/>

  For algorithm for topic modeling, we settled on the LDA - Latent Dirichlet Allocation - unsupervised learning algorithm, which assumes that the topics of the documents have a Dirichlet distribution and the words in the topics also have a Dirichlet distribution. The technical part of the can be found in the [realtime_twitter_topic_modeling_pyspark.ipynb](https://github.com/SanGreel/real-time-twitter-topic-modeling/blob/master/realtime_twitter_topic_modeling_pyspark.ipynb).
<br/>
### Team
1. Andrew Kurochkin, [SanGreel](https://github.com/SanGreel).
2. Yevhen Pozdniakov, [YevgenyW](https://github.com/YevgenyW).
3. Oleksandr Smyrnov, [smirale](https://github.com/smirale).
4. Dmytro Babenko, [DmytroBabenko](https://github.com/DmytroBabenko).
5. Anton Shcherbyna, [antonshcherbyna](https://github.com/antonshcherbyna).
<br/>
### Data
Twitter data was collected with the script that can be found in the folder [twitter-data-collector](https://github.com/SanGreel/real-time-twitter-topic-modeling/tree/master/twitter-data-collector) . The main purpose of the script is to collect tweets from Twitter API (you should have Twitter Developer account).
<br/>
#### Final dataset
- 332548 tweets (10Gb in mongodb, ~100Mb in csv) from New-York geolocation since 30 of May up to 15 of June;
- 6617029 tweets (~1.69Gb in csv) from USA geolocation since 15 of June up to now.
All collected data can be downloaded via link: https://drive.google.com/file/d/1QxGI2esat6BnrPv0YE5Ud6uma49Lccty/view?usp=sharing.
<br/>

### Instruction to reproduce
0. If you don't have PySpark, install it.

1. Install requirements:
```
pip install -r requirements.txt
```

2. Install and update git submodules:
```
git submodule init
git submodule update
```

3. Now you are ready to go throw the file [realtime_twitter_topic_modeling_pyspark.ipynb](https://github.com/SanGreel/real-time-twitter-topic-modeling/blob/master/realtime_twitter_topic_modeling_pyspark.ipynb), where you can find full pipeline from loading data to modeling and comparison with Google trends.

