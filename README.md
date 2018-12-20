# LMS
#### PPPoSD final project
<b>Author: Julia Shenshina</b>

A learning management system (<b>LMS</b>) is a software application for the administration, documentation, tracking, reporting and delivery of educational courses, training programs, or learning and development programs.
### Installation
Download the project to the target direcory with
```python
git clone https://github.com/julia-shenshina/LMS.git
```
To install run
```python
cd /target_directory_path/LMS
pip install -r requirements/requirements.txt
ip install -r requirements/dev_requirements.txt
pip install -e .
```
### Run
```python
lms runserver
```
### Tests
```python
python setup.py test
```