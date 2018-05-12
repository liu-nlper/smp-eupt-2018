****

#	SMP EUPT 2018

****

##	Categories
-	[Abstract](#abstract)
-   [Set Up](#setup)
-   [Usage](#usage)
-   [Analysis](#analysis)
-   [Submitting](#submitting)

****

##	<a name="abstract"> Abstract </a>

[SMP EUPT 2018](https://biendata.com/competition/smpeupt2018/)

****

##  <a name="setup"> Set Up </a>

```Shell
# python 2.7
python -m pip install numpy
python -m pip install scipy
python -m pip install enum34
python -m pip install ConfigParser
python -m pip install xgboost
python -m pip install scikit-learn
python -m pip install gensim
```

****

##	<a name="usage"> Usage </a>

```Shell
# Overall
python -m bin.go

# Builds a model
python -m bin.go --package bin.run.singlerun --object SingleRun 
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

![Content Length](img/content-length.png)
