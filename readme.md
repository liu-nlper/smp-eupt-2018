****

#	SMP EUPT 2018

****

##	Categories
-	[Abstract](#abstract)
-   [Set Up](#setup)
-   [Usage](#usage)
-   [Analysis](#analysis)
-   [Visualization](#visual)
-   [Special Case](#case)
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

**More visual graphs** for features can be found [here](doc/visual.md).

### Content Length

<div align="center">
    <img src="/img/content_length_hist.png" height="300px" />
    <img src="/img/content_length_kde.png" height="300px" />
</div>

### Chinese Char Ratio

<div align="center">
    <img src="/img/chinese_char_ratio_hist.png" height="300px" />
    <img src="/img/chinese_char_ratio_kde.png" height="300px" />
</div>

### Char Set Ratio

<div align="center">
    <img src="/img/char_set_ratio_hist.png" height="300px" />
    <img src="/img/char_set_ratio_kde.png" height="300px" />
</div>

> Some interesting discoveries, the distribution of *human author* is more natural while other authors have *biases*. If we can eliminate these biases in the model (such as translation model), can we make the model more effective? 

****

##	<a name="case"> Special Case </a>

| ID    | 标签         |
| ----  | ----         |
| 18772 | 机器翻译      |

****

##	<a name="exp"> Experiment </a>

| Version   | Base Version  | Online    | Offline       | Note                                              |
| ----      | ----          | ------    | -------       | ----                                              |
| v015      | v014          | ------    | 0.95990       | add contain_word_location (consider delete it)    |
| v014      | v013          | ------    | 0.95988       | add last_char_is_chinese                          |
| v013      | v011          | ------    | 0.95897       | add last_char_is_dot                              |
| ~~v012~~  | ~~v009~~      | ------    | ~~0.94145~~   | ~~add space_ratio~~                               |
| v011      | v010          | ------    | 0.94155       | add space_ratio                                   |
| v010      | v009          | ------    | 0.94150       | add space_num                                     |
| v009      | v008          | ------    | 0.93625       | add ave_chinese_continuous_length                 |
| v008      | v007          | ------    | 0.92077       | add word_ratio_3                          |    
| v007      | v006          | ------    | 0.91387       | add char_set_ratio                        |
| v006      | v005          | ------    | 0.91188       | add english_char_ratio                    |   
| v005      | v004          | ------    | 0.90359       | add digit_char_ratio                      |
| v004      | v003          | ------    | 0.89415       | add chinese_char_ratio                    |
| v003      | v002          | ------    | 0.85627       | add word_set_num                          |
| v002      | v001          | ------    | 0.81059       | add word_num                              |
| v001      | v000          | ------    | 0.80358       | add content_length                        |