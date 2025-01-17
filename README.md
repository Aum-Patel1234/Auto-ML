# Project Setup for EC2

## EC2 Instance Configuration

### EC2 Type
- **Instance Type:** t2.micro (Free Tier eligible)
- **vCPU:** 1
- **Memory:** 1 GB

### Step 1: Update and Install
SSH into the EC2 instance and update the package list:

```bash
sudo apt update -y
sudo apt upgrade -y
```

### Step 2: Install Required Software
Install Python, Pip, and virtual environment tools:

```
sudo apt install python3.12 -y
```

### Step 3: Set Up Your Project
Clone Your Project: Use git to clone your project repository:

```bash
git clone https://github.com/Aum-Patel1234/Auto-ML.git
```
```
pip install -r requirements.txt
```
# Django Project Setup and File Upload Configuration

## Django Configuration for File Uploads

### Step 1: Update `settings.py`
Configure file storage in your `settings.py`:

```python
import os
```

# Directory to store uploaded files
```bash
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### Step 2: Apply Migrations
Run migrations to set up the database (if needed):

```
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Start the Django Development Server
Run the development server on port 8000 (or your preferred port):

```
python manage.py runserver 0.0.0.0:8000
```

### Step 4: Install Gunicorn
Install Gunicorn with the following command:

```
pip install gunicorn
```



# the config is still incomplete start nginx server
will complete 