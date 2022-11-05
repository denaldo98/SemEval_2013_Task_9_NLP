
# SemEval-2013-Task-9
Project realized for the course *Advanced Human Languages Technologies* at *Universitat Politècnica de Catalunya* (Master in *Artificial Intelligence*).

**Authors:**
- Denaldo Lapi
- Francesco Aristei


The project consists in solving Task 9 of the *Semeval-2013: International Workshop on Semantic Evaluation* ([link to the paper)](https://aclanthology.org/S13-2056/).

The task concerns the recognition of drugs and extraction of drug-drug interactions that appear in biomedical literature. It is divided in two subtasks:

-   Task 9.1: Recognition and classification of drugs (NERC).
-   Task 9.2: Detection and classification of drug-drug interactions between pairs of drugs (DDI).

The tasks is solved by using 3 different approaches:

 - Rule-based approach
 - Traditional Machine-Learning approach
 - Deep Learning approach
 

## Documentation and Reports

 - [Assignment_1_AHLT](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/Assignment_1_AHLT.pdf) contains the procedures followed to solve Task 9.1 by using the Rule-based approach and the traditional Machine Learning-based approach. The report provides also the main snippets of Python code, together with the obtained final results.
 - [Assignment_2_AHLT](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/Assignment_2_AHLT.pdf) contains the procedures followed to solve Task 9.2 by using the Rule-based approach and the traditional Machine Learning-based approach. The report provides also the main snippets of Python code, together with the obtained final results.
- [Assignment_3_AHLT](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/Assignment_3_AHLT.pdf) contains procedure followed to solve  Task 9.1 and Task 9.2 by using the Deep Learning-based approach. The report provides also the main snippets of Python code, together with the obtained final results on both tasks.

## Results
Results obtained in the Devel and Test Datasets 

### Task 9.1 (NERC)
*Best results:* 
-   **Devel set**: 
	- Precision: 76.2%, 
	- Recall: 68.3%, 
	- F1: 71.9%
-   **Test set**: 
	- Precision: 68.8%, 
	- Recall: 72.8%, 
	- F1: 69.2%

Below we show the results obtained with each approach.
#### Rule-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.1_rule_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set

#### Machine Learning-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.1_ml_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set
#### Deep Learning-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.1_dl_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set

### Task 9.2 (DDI)
*Best results:* 
-   **Devel set**: 
	- Precision: 68.3%, 
	- Recall: 60.0%, 
	- F1: 62.9%
-   **Test set**: 
	- Precision: 58.5%, 
	- Recall: 62.9%, 
	- F1: 60.4%

Below we show the results obtained with each approach.
#### Rule-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.2_rule_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set
#### Machine Learning-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.2_ml_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set
#### Deep Learning-based approach
![Perfomance on the devel dataset (on the left) and on the test dataset (on the right](https://github.com/denaldo98/SemEval-2013-Task-9/blob/main/results/9.2_dl_based.PNG)
N.B. On the left results obtained on the Devel set, on the right results obtained on the Test set
