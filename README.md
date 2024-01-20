# CS50w - Commerce

![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)

Video demo of **[Commerce](https://www.youtube.com/watch?v=WMQmilydvbs)**

## Description

This is a eBay-like e-commerce auction site that will allow users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist”. Instructions for completing this project can be found at https://cs50.harvard.edu/web/2020/projects/2/commerce/

This project is part of the **[CS50’s Web Programming with Python and JavaScript](https://cs50.harvard.edu/web/2020/)**.

### HOMEPAGE

This is the index/homepage. Banners redirect user to the specific category by clicking on it.
Newest and most popular items (based on bids count) are displayed on mainpage.

<p align="center">
  <img src="./auctions/static/auctions/README_images/homepage.png">
</p>

### Categories

It is possible to apply category filter by selected wanted category.

<p align="center">
  <img src="./auctions/static/auctions/README_images/categories.png">
</p>

### SELL

On this page, user can sell his items by providing a title, a category, a brief description, starting price and some pictures. It is possible to add severals pictures.

<p align="center">
  <img src="./auctions/static/auctions/README_images/sell.png">
</p>

### Auction

This is the main page for any listed auction. User can see pictures by hovering mouse on pictures, bid, add/remove to wishlist, view details about the auction and comment.

Message is displayed if user bid, if got the highest bid and when item is added/removed from wishlist.

<p align="center">
  <img src="./auctions/static/auctions/README_images/auction.png">
</p>

### Bids

<p align="center">
  <img src="./auctions/static/auctions/README_images/bids.png">
</p>

### Wishlist

This is where wishlisted items will be display. There is three sections as "on going", "won" and "lost".

<p align="center">
  <img src="./auctions/static/auctions/README_images/wishlist.png">
</p>

### My Auctions

This is where items posted by the user will be display. At any time, user can decide to close his auction. There is two section "active" and "closed".

<p align="center">
  <img src="./auctions/static/auctions/README_images/myauctions.png">
</p>

<p align="center">
  <img src="./auctions/static/auctions/README_images/close.png" width=355 height=350>
  <img src="./auctions/static/auctions/README_images/closed.png" width=355 height=350>
</p>

## Instructions

Install [Python](https://www.python.org/downloads/), then you can install [Django](https://docs.djangoproject.com/en/4.2/topics/install/) :

```
python -m pip install Django
```

Clone this repository and launch Wiki web app with :

```
python manage.py runserver
```

## Credit

**[CS50w](https://pll.harvard.edu/course/cs50s-web-programming-python-and-javascript)**<br>
**[David J. Malan](https://cs.harvard.edu/malan/)**<br>
**[Brian Yu](https://brianyu.me/)**<br>
**[Doug Lloyd](https://hls.harvard.edu/doug-lloyd/)**<br>
