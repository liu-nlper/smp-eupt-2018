****

#	SMP EUPT 2018

****

##	Categories
-	[Abstract](#abstract)
-   [Set Up](#setup)
-   [Usage](#usage)
-   [Analysis](#analysis)
-   [Visualization](#visual)
-   [Experiment](#exp)

****

##	<a name="abstract"> Abstract </a>

[SMP EUPT 2018](https://biendata.com/competition/smpeupt2018/)

****

##  <a name="setup"> Set Up </a>

### Install

```Shell
# python 2.7
python -m pip install numpy
python -m pip install scipy
python -m pip install enum34
python -m pip install ConfigParser
python -m pip install xgboost
python -m pip install scikit-learn
python -m pip install gensim
python -m pip install jieba
```

### Dirs

```Shell
mkdir data/
mkdir data/feature/
mkdir data/index/
mkdir data/log/
mkdir data/out/
mkdir data/raw/
```

****

##	<a name="usage"> Usage </a>

```Shell
# Overall
python -m bin.go

# Normalize data
python -m bin.go --package bin.preprocess.normalize --object Json2CSV 

# Generate index
python -m bin.go --package bin.preprocess.normalize --object IndexGenerator 

# Generate feature
python -m bin.go --package bin.feature.statistics --object SentenceLength    

# Feature visualization
python -m bin.go --package bin.feature.content --object ContentLength --func visual 

# Builds a model
python -m bin.go --package bin.experiment.singlerun --object SingleRun

# Cross validation
python -m bin.go --package bin.experiment.cv --object CrossValidation
```

****

##	<a name="analysis"> Analysis </a>

### Content Length

| Label | Max   | Min   | Mean  |
| ----  | ----  | ----  | ----  |
| 人类作者 | 101487 | 105   | 2616  |
| 机器翻译 | 3382   | 371   | 1095  |
| 自动摘要 | 1443   | 65    | 254   |
| 机器作者 | 6971   | 0     | 3238  |

##	<a name="visual"> Visualization </a>

### Content Length

<div align="center">
    <img src="img/content_length_hist.png" height="300px" />
    <img src="img/content_length_kde.png" height="300px" />
</div>

### Word Number

<div align="center">
    <img src="img/word_num_hist.png" height="300px" />
    <img src="img/word_num_kde.png" height="300px" />
</div>

### Word Set Number

<div align="center">
    <img src="img/word_set_num_3_hist.png" height="300px" />
    <img src="img/word_set_num_3_kde.png" height="300px" />
</div>

### Chinese Char Ratio

<div align="center">
    <img src="img/chinese_char_ratio_hist.png" height="300px" />
    <img src="img/chinese_char_ratio_kde.png" height="300px" />
</div>

### Digit Char Ratio

<div align="center">
    <img src="img/digit_char_ratio_hist.png" height="300px" />
    <img src="img/digit_char_ratio_kde.png" height="300px" />
</div>

****

##	<a name="exp"> Experiment </a>

| Version               | Online    | Offline   | Note                      |
| ----                  | ------    | -------   | ----                      |
| v005                  | ------    | 0.90112   | add digit_char_ratio      |
| v004                  | ------    | 0.89020   | add chinese_char_ratio    |
| v003                  | ------    | 0.85419   | add word_set_num          |
| v002                  | ------    | 0.80656   | add word_num              |
| v001                  | ------    | 0.79878   | add content_length        |