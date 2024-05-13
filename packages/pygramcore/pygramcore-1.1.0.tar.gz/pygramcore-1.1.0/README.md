<h1 align="center">
  <br>
  <img src="https://github.com/jtayped/pygramcore/blob/main/images/icon.png?raw=true" alt="PyGramCore" width="200">
  <br>
  📷 pygramcore
  <br>
</h1>

<h4 align="center">An easy-to-use Instagram SDK using <a href="https://www.selenium.dev/" target="_blank">Selenium</a>.</h4>

<div align="center">
  <a href="https://pypi.org/project/PyGramCore/">
    <img src="https://img.shields.io/pypi/v/pygramcore?style=for-the-badge">
  </a>
  <a href="https://github.com/jtayped/pygramcore/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/jtayped/pygramcore?style=for-the-badge" alt="License">
  </a>
  <a href="https://github.com/jtayped/pygramcore/issues">
    <img src="https://img.shields.io/github/issues/jtayped/pygramcore?style=for-the-badge" alt="License">
  </a>
  <a href="https://www.linkedin.com/in/jtayped/">
    <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn">
  </a>
</div>

<div align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#related">Related</a>
</div>

<div id="key-features"></div>

## 🔑 Key Features

- **Modular Elements**: Easily use and customize modular elements such as Posts, Comments, and Users.

  - **Users**: Follow, direct message, get posts, and more.

  - **Posts**: Like, comment, download, and more.

  - **Stories** (Coming soon...)

  - **Comments** (Coming soon...)

<div id="how-to-use"></div>

## 🔧 How To Use

First of all, install the package using:

```bash
pip install pygramcore
```

To take authenticated actions, initialize your Instagram account with your email/password and login:

```python
from pygramcore import Account

Account.login("youremail@email.com", "yourpassword123")
Account.save_cookies("path/to/file.pkl")
```

To initialize an account from cookies:

```python
Account.load_cookies("path/to/file.pkl")
```

This will allow you to post images, comment on other peoples posts, send DMs, etc...

```python
Account.post("path/to/image.png", "Your very interesting caption")
```

To search for a user simply:

```python
from pygramcore import User

user = User("username123_")
```

Here is an example of the usage of a user:

```python
# Get a list of Post() objects
posts = user.get_posts(limit=50)

# Like the first 10 posts in the user's feed
for post in posts[:10]:
  # Get URLs of the images in the post
  urls = post.get_images()

  # Like & comment the post
  post.comment("Nice post!")
  post.like()
```

Please refer to the [docs](https://github.com/jtayped/pygramcore/tree/main/docs) for more.

<div id="related"></div>

## ❓ About the Project
This Python package was created as a fun project to enhance my proficiency in writing "professional" Python code, building packages, implementing semantic versioning, and ensuring code maintainability.
I am still a relatively new developer, and I welcome any contributions and feedback to help me improve.
It is important to note that this project is not intended to replace essential packages such as [InstaPy](https://github.com/InstaPy/InstaPy), nor do I anticipate that it will.

## 🙋‍♂️ You may also like...

- [✂️📱TikTok Manager](https://github.com/jtayped/tiktok-manager) - A script that manages MULTIPLE TikTok accounts by schedueling automatically generated videos from pre-selected YouTube channels to TikTok in advance.
- [🧑‍💼My Portfolio](https://joeltaylor.business) - Check out my front-end and SEO skills on my Portfolio!
