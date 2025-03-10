# Project 1

Name: Yuke Li （李宇科）

ID: 2024234328

### Metrics Enhancement  
I have optimized the execution logic of `metrics.m` to support **batch processing of multiple images** in a single run. The improved version now:  
1. Automatically calculates **average metrics** across all input images  
2. Outputs consolidated results with both statistical summaries and per-image diagnostics  

Usage method: 

Ensure that the working directory is set to the current directory and run the `metric.m` file directly.

### Execution Guide  
**1. Dependency Installation**  
Before running the code, ensure required packages are installed using:  

```bash
pip install -r requirements.txt
```
*Note: This should be executed in your Python environment terminal.*  

**2. Jupyter Notebook Execution**  
To use `work.ipynb`:  

- Open the notebook in **Jupyter Lab** or **Jupyter Notebook**  
- Confirm the working directory matches the notebook's location (verify using):  
```python
import os
print(os.getcwd()) 
```
- Sequential Execution: 
