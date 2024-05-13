from dataclasses import dataclass
from typing import Literal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from urllib.parse import urlparse, urljoin
import time

from ..pygram import *
from ..exceptions.user import *
from ..utils import *
from ..constants import *


def user_dialog_action(func):
    """
    Decorator function that opens and closes the user dialog. The user dialog is where you can take actions on a user, such as: unfollowing, adding or removing from close friends, etc...
    """

    def wrapper(user: "User", *args, **kwargs):
        if not user.is_following():
            raise UserNotFollowed(user.name)

        # Raises a click interception error if the dialog was open already
        try:
            user.open_user_dialog()
        except ElementClickInterceptedException:
            pass

        # Perform function being decorated
        value = func(user, *args, **kwargs)

        # Attempt to close the user dialog, some actions
        # close the dialog automatically (e.g. unfollowing)
        try:
            user._driver.implicitly_wait(0)
            user.close_user_dialog()
        except:
            pass
        finally:
            user._driver.implicitly_wait(IMPLICIT_WAIT)

        return value

    return wrapper


def check_private(func):
    """
    Decorator that checks if a user is private.

    Raises:
        UserIsPrivate: Raises whent the user is private
    """

    def wrapper(user: "User", *args, **kwargs):
        if user.is_private():
            raise UserIsPrivate(user.name)

        value = func(user, *args, **kwargs)
        return value

    return wrapper


def check_following(func):
    """
    Decorator that checks if the logged in account follows the user.

    Raises:
        UserNotFollowed: Raises when the user is not followed.
    """

    def wrapper(user: "User", *args, **kwargs):
        if not user.is_following():
            raise UserNotFollowed(user.name)

        value = func(user, *args, **kwargs)
        return value

    return wrapper


@dataclass
class User(metaclass=Navigator):
    """
    Represents an Instagram user.

    Args:
        name (str): Username of the user.
    """

    name: str

    def __post_init__(self):
        self._driver: webdriver.Chrome

    @property
    def url(self):
        url = urljoin(INSTAGRAM_URL, self.name)
        return url

    @check_authorization
    def is_private(self) -> bool:
        """
        Checks if the user has a private account.

        Returns:
            bool: Whether the account is private.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        self._driver.implicitly_wait(2)

        # Attempt to find the div that contains "This account is private"
        elements_found = self._driver.find_elements(
            By.XPATH,
            '//div[@class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x6s0dn4 x1oa3qoh x1nhvcw1"]',
        )

        self._driver.implicitly_wait(IMPLICIT_WAIT)

        return bool(elements_found)

    @check_authorization
    def follow(self) -> None:
        """
        Follows the user with the current account logged in.

        Raises:
            UserAlreadyFollowed: Raises when the user is already followed. Use `.is_followed()` to check if followed.
            NotAuthenticated: Raises when the current account is not logged in.
        """
        if self.is_following():
            raise UserAlreadyFollowed(self.name)

        follow_btn = self._driver.find_element(
            By.XPATH, '//button[@class=" _acan _acap _acas _aj1- _ap30"]'
        )
        follow_btn.click()

    @check_authorization
    @check_private
    @check_following
    @user_dialog_action
    def unfollow(self):
        """
        Unfollows the user with the current account logged in.

        Raises:
            UserNotFollowed: Raises when the user is not followed. Use `.is_followed()` to check if followed.
            NotAuthenticated: Raises when the current account is not logged in.
            UserIsPrivate: Raises when the user is private.
        """
        unfollow_btn = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div:nth-child(8)",
        )
        unfollow_btn.click()

    @check_authorization
    def is_following(self):
        """
        Check whether the account logged in follows the user.

        Returns:
            bool: whether the account logged in follows the user.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        follow_btn = self._driver.find_element(
            By.CSS_SELECTOR, "button._acan._acap._aj1-._ap30"
        )
        classes = follow_btn.get_attribute("class")

        # "_acat" when following
        # "_acas" when not
        return "_acat" in classes

    @check_authorization
    @check_private
    @check_following
    @user_dialog_action
    def add_close_friend(self):
        """
        Adds the user to the current account's close friends.

        Raises:
            UserCloseFriend: Raises when the user is already a close friend.
            NotAuthenticated: Raises when the current account is not logged in.
            UserNotFollowed: Raises when the user is not followed.
        """
        if self.is_close_friend():
            raise UserCloseFriend(self.name)
        self.open_user_dialog()

        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, 'svg[aria-label="Close friend"]'
        )
        close_friend_btn.click()

    @check_authorization
    @check_following
    @user_dialog_action
    def remove_close_friend(self):
        """
        Removes the user from the current account's close friends.

        Raises:
            UserNotCloseFriend: Raises when the user is not close friends already.
            NotAuthenticated: Raises when the current account is not logged in.
            UserNotFollowed: Raises when the user is not followed.
        """
        if not self.is_close_friend():
            raise UserNotCloseFriend(self.name)
        self.open_user_dialog()

        close_friend_btn = self._driver.find_element(
            By.CSS_SELECTOR, "svg[aria-label='Close friend']"
        )
        close_friend_btn.click()

    @check_authorization
    @user_dialog_action
    def is_close_friend(self) -> bool:
        """
        Checks if the user is a close friend.

        Returns:
            bool: Whether the user is a close friend

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
        """
        # A user isn't a close friend if not followed in the first place
        if not self.is_following():
            return False

        # Check if already close friend
        close_friends_icon = self._driver.find_element(
            By.CSS_SELECTOR,
            'svg[aria-label="Close friend"]',
        )

        classes = close_friends_icon.get_attribute("class")
        return "x1g9anri" in classes

    @check_authorization
    @check_following
    @user_dialog_action
    def mute(
        self,
        *modes: Literal["posts", "stories"],
    ):
        """
        Mutes the user's posts and/or stories. It is important to note that this function only enables the option, and can't disable it.

        Args:
            modes ("posts" and/or "stories"): Modes to mute, which can be posts and/or stories.

        Usage:
        ```python
        user = User("username")
        user.mute("stories", "posts")
        ```

        Raises:
            ValueError: if a mode in the arguments does not exist.
            NotAuthenticated: Raises when the current account is not logged in.
            UserNotFollowed: Raises when the user is not followed.
        """
        if isinstance(modes[0], str):
            modes = list(modes)

        if not all(mode in ["posts", "stories"] for mode in modes):
            raise ValueError("This mute mode does not exist!")

        mute_menu = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div:nth-child(6)",
        )
        mute_menu.click()

        mute_btns = self._driver.find_elements(
            By.XPATH,
            '//input[@dir="ltr"]',
        )

        # Associate mute modes to indexes of the options on the menu
        mode_indexes = {"posts": 0, "stories": 1}
        for mode in modes:
            mute_btn_idx = mode_indexes[mode]
            mute_btn = mute_btns[mute_btn_idx]

            # Check if the mode is checked already
            is_checked = mute_btn.get_attribute("aria-checked")
            if is_checked.lower() == "false":
                mute_btn.click()

        # Submit options
        submit_btn = self._driver.find_element(
            By.CSS_SELECTOR,
            "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1y1aw1k.x1sxyh0.xwib8y2.xurb0ha.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div",
        )
        submit_btn.click()

    def get_total_posts(self) -> int:
        """
        Get the user's total amount of posts.

        Returns:
            int: total posts
        """
        posts_span, _, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        posts_str = posts_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(posts_str.replace(",", ""))
        return followers

    def get_followers(self) -> int:
        """
        Get the user's total amount of followers

        Returns:
            int: total followers
        """
        # Gets the string value (e.g. "156,204")
        _, followers_span, _ = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        followers_str = followers_span.get_property("title")

        # Remove the commas and convert to integer
        followers = int(followers_str.replace(",", ""))
        return followers

    def get_following(self) -> int:
        """
        Get the amount of people the user follows.

        Returns:
            int: total following
        """
        _, _, following_span = self._driver.find_elements(By.CSS_SELECTOR, "span._ac2a")
        following_str = following_span.find_element(By.CSS_SELECTOR, "span").text

        # Remove the commas and convert to integer
        followers = int(following_str.replace(",", ""))
        return followers

    @check_authorization
    @check_private
    def send_dm(self, message: str) -> None:
        """
        Send a DM (direct message) to the user.

        Args:
            message (str): Message to send the user.

        Raises:
            NotAuthenticated: Raises when the current account is not logged in.
            UserIsPrivate: Raises when the user is private.
        """
        # Enter the DMs
        message_btn = self._driver.find_element(By.XPATH, '//div[text()="Message"]')
        message_btn.click()

        # Write the the message
        message_input = self._driver.find_element(
            By.XPATH,
            '//div[@aria-describedby="Message"]',
        )
        write(message_input, message)

        # Send message
        message_input = message_input.send_keys(Keys.ENTER)

        # Wait for message to send, moving on immediately after doesn't send the message
        time.sleep(0.5)

    @check_private
    def get_posts(self, reels=True, limit=25) -> list:
        """
        Get a list of posts from the user's account.

        Args:
            reels (bool, optional): Whether to include reels or not. Defaults to True.
            limit (int, optional): Limits the amount of posts to retrieve. Defaults to 25 and can't be above 100.

        Returns:
            list[Post]: List of post objects

        Usage:
        ```python
        # Fetch username's posts
        user = User("username")
        posts = user.get_posts()

        # Like his first three posts
        for post in posts[:3]:
            post.like()
        ```

        Raises:
            UserIsPrivate: Raises when the user is private.
        """
        from .post import Post

        css_selector = "a[href^='/p/']"
        if reels:
            css_selector += ",a[href^='/reel/']"

        posts = []

        # Scroll down to load posts
        while len(posts) < limit:
            # Scroll down
            self._driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)

            # Wait for new posts to load
            WebDriverWait(self._driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, css_selector))
            )

            # Get all posts
            post_elements = self._driver.find_elements(By.CSS_SELECTOR, css_selector)

            # Add new posts to the list
            for post_element in post_elements:
                href = post_element.get_attribute("href")
                path = urlparse(href).path
                id = path.split("/")[2]

                post = Post(id)
                posts.append(post)

            # If no new posts loaded, break the loop
            if len(post_elements) == 0:
                break

        return posts[:limit]

    def open_user_dialog(self):
        dialog_btn = self._driver.find_element(By.XPATH, '//div[text()="Following"]')
        dialog_btn.click()

    def close_user_dialog(self):
        close_btn = self._driver.find_element(
            By.CSS_SELECTOR,
            'svg[aria-label="Close"]',
        )
        close_btn.click()
