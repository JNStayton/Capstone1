### API: BoardGameAtlas
#### URL: https://www.boardgameatlas.com/api/docs

### Outline
1. What goal will your website be designed to achieve? 

- This website will access the BoardGameAtlas API to allow users to gain access to and search through a 
variety of board games. 
- Users can visit the site, search games (there are lots of API endpoints; can search by name, publisher, or any other number of game details), view game details, including:
  - Rules
  - Number of players 
  - Current low prices (with links to vendor site to purchase)
  - Images
  - Videos (ie tutorials)
- Registered/logged-in users can view and post, in addition to game details listed above:
  - Reviews
  - Game lists (and create their own lists; favorites, wishlists, etc)

The goal is to have an easy-to-use app to search for new tabletop games to play, to have a 
resource for learning a new game, and to create (potentially) shareable lists (wishlists, play lists, games to bring to meetups, what have you).

2. What kind of users will visit your site? In other words, what is the demographic of your users? 
- The target demographic is, well, tabletop gamers. But I’d like the site itself to be friendly 
enough that a new gamer could find something for themselves, too.

3. What data do you plan on using? You may have not picked your actual API yet, which is fine, just outline what kind of data you would like it to contain. 

- The API has several GET and POST routes; the GET routes are pretty much centered around 
searching the games database and returning either a single game object or a list of game objects based on the search parameters. There are particular GET routes for retrieving images/details/prices, listing and sorting based on various search queries (publishers, artists, numbers of players, etc). The game object itself has all of the game’s individual data. 

- The POST routes from the API are centered around creating users, game lists, reviews, and submitting FAQs. However, I will not be accessing the API's POST routes. I will instead save users, reviews, and game lists to my own PostgreSQL database, and have my own schema for creating table data with the specific game object ID from the API response saved as a reference point.

4. In brief, outline your approach to creating your project (knowing that you may not know everything in advance and that these details might change later). Answer questions like the ones below, but feel free to add more information: 

   - What does your database schema look like? 
     - Tables would include Users, Reviews, Lists, and would be one-to-many (one User, many Reviews and Lists). 


   - What kinds of issues might you run into with your API? 
     - On a basic note, I might have trouble reading the data for some of the endpoints. I’ve been playing around with it on Postman to get a feel for and gain more comfort with the data. If the API is down, I might have functionality issues. It seems like the data on the API is updated pretty regularly, especially with the pricing and discounts sections. 

   - Is there any sensitive information you need to secure? 
     - Users authentication requires just a username, email, and password. I would need to make sure to include basic authentication, unique usernames across my app, and password hashing to make it more secure. But no payment information is logged on the API or on my end.


   - What functionality will your app include?
     - Searching, viewing, and links to external sites (to purchase a game, if interested). Logged in users also get to save their own lists (favorites, wish lists, etc), and read and post reviews and and ratings. There’s also a functionality within the API for “play logs”, where users can post when/where they played the game, players, some game notes, etc -- that might be a fun interactive part to add, if it’s not too much trouble. Then in addition to lists, they could have like… a game journal that could be shared with other players/users.


   - What will the user flow look like?
     - Home page: Search functionality, sign-up and login,  listing of games by various criteria (10 top rated games, 10 games currently on sale, etc).
     - Search page: Display games ordered by search criteria, with options for filtering
     - Game page: Display details about specific game. (Option to add/edit game details, including game pictures, videos, reviews, ratings if logged in)
     - User page: Display user profile, including lists, reviews, and starred (favorited) games


   - What features make your site more than CRUD? Do you have any stretch goals? 
     - Most of the stretch goals are around logged-in users. These are all sort of just… potentials  right now. 
     - Recommendations based off of favorited games
     - Potential email updates when a game in a list goes on sale
     - The game-journal, potentially, described above - could be shared and edited among users
     - Review/rating functionality
