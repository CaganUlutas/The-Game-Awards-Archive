# 🏆 The Game Awards Archive

**Live Demo:** [thegameawardsarchive.onrender.com](https://thegameawardsarchive.onrender.com)

A comprehensive, Django-powered web archive cataloguing every game nominated and awarded at **The Game Awards** from 2014 to 2025. Featuring 226+ games with rich metadata pulled from multiple APIs, the site delivers an immersive, premium browsing experience across all devices.

<div align="center">
  <img src="assets/Home%20Animation.gif" alt="The Game Awards Archive - Main Animation" />
</div>

<br/>

## 📸 GIFs & Gallery

<table align="center">
  <tr>
    <td><img src="assets/Home%20Main%20Page.gif" alt="Home Page View"/></td>
    <td><img src="assets/Top%20Games%20Page.gif" alt="Top Games View"/></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><img src="assets/Details%20Page.gif" alt="Game Details View" width="50%"/></td>
  </tr>
</table>

## ✨ Features

### 🏠 Home Page
- **Dynamic Hero Section** with an auto-playing YouTube trailer background for each year's Game of the Year winner.
- **Year Selector** to browse nominations and winners across all ceremony years (2014–2025).
- **Category-Grouped Cards** showing every nominated game with Metacritic scores, developer names, and winner badges.

### 🎮 Game Details Page
- **Rich Metadata:** Description, release date, genres, developers, Metacritic score, and platform availability.
- **Embedded YouTube Trailers** with auto-play support.
- **Steam Integration:**
  - Review score with a circular SVG gauge and color-coded badges (Overwhelmingly Positive → Negative).
  - Total review count and estimated ownership figures (via SteamSpy).
  - Screenshot gallery with a full-screen lightbox modal and keyboard/click navigation.
- **HowLongToBeat Data:** Main Story, Main + Extras, and Completionist playtime estimates.
- **Store Links:** Direct buttons to Steam, PlayStation Store, Xbox Store, and Nintendo eShop.
- **Nomination & Award History:** Full timeline of every nomination and win for the game.

### 🏅 Hall of Fame
- A vertical timeline showcasing every **Game of the Year** winner from 2014 to 2025.

### 📊 Top Games
- Paginated ranking of all games sorted by Metacritic score (20 per page).

### 🔍 Search
- Full-text search across all game titles with instant results.

### 📱 Responsive Design
- Fully optimized for desktop, tablet, and mobile with custom breakpoints, smooth animations, and premium typography.

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python, Django 6.0 |
| **Frontend** | HTML5, CSS3 (Custom styling with modern aesthetics), Vanilla JavaScript |
| **Database** | SQLite (Development), PostgreSQL (Production) |
| **Deployment** | Render, Gunicorn, WhiteNoise |
| **External APIs** | RAWG, Steam Store API, Steam Reviews API, SteamSpy, HowLongToBeat |

## 📁 Project Structure

```
gameawards/
├── manage.py
├── requirements.txt
├── build.sh                          # Render deployment script
├── .env.example                      # Environment variable template
│
├── gameawards/                       # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── awards/                           # Main Django app
│   ├── models.py                     # Game, AwardYear, Category, Nomination
│   ├── views.py                      # Page views & logic
│   ├── urls.py                       # URL routing
│   ├── admin.py                      # Admin panel configuration
│   │
│   ├── templates/awards/
│   │   ├── home.html                 # Home page with hero & year selector
│   │   ├── game_details.html         # Game detail page
│   │   ├── hall_of_fame.html         # GOTY winners timeline
│   │   ├── top_games.html            # Metacritic-ranked game list
│   │   └── search_results.html       # Search results page
│   │
│   ├── static/awards/
│   │   ├── base.css                  # Shared styles (navbar, footer, etc.)
│   │   ├── home.css                  # Home page styles
│   │   ├── details.css               # Game details page styles
│   │   ├── hall_of_fame.css          # Hall of Fame page styles
│   │   ├── top_games.css             # Top Games page styles
│   │   ├── lightbox.js               # Screenshot lightbox modal logic
│   │   └── icons/                    # Favicon & store logos
│   │
│   ├── fixtures/
│   │   ├── tga_data.json             # Core nomination/award data
│   │   └── all_data.json             # Full database dump (games + metadata)
│   │
│   └── management/commands/          # Custom data pipeline commands
│       ├── fetch_game_details.py     # RAWG API → game metadata
│       ├── fetch_developers.py       # RAWG API → developer names
│       ├── fetch_store_links.py      # RAWG API → store URLs
│       ├── fetch_trailers.py         # YouTube scraping → trailer URLs
│       ├── fetch_steam_data.py       # Steam + SteamSpy → reviews, screenshots, owners
│       └── fetch_hltb.py             # HowLongToBeat → playtime estimates
│
└── assets/                           # README GIFs & images
```

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/CaganUlutas/The-Game-Awards-Archive.git
   cd The-Game-Awards-Archive
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your keys:
   #   DJANGO_SECRET_KEY=your-secret-key
   #   RAWG_API_KEY=your-rawg-api-key
   ```

5. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Load the data fixture:**
   ```bash
   python manage.py loaddata awards/fixtures/all_data.json
   ```

7. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Open in browser:**
   Navigate to `http://127.0.0.1:8000/`

## 🔧 Custom Management Commands

These commands form the data pipeline that populates and enriches the database:

| Command | Description |
|---------|-------------|
| `fetch_game_details` | Fetches core game metadata (description, genres, platforms, scores) from the RAWG API. |
| `fetch_developers` | Fetches and updates developer names from the RAWG API. |
| `fetch_store_links` | Fetches Steam, PlayStation, Xbox, and Nintendo store URLs from the RAWG API. |
| `fetch_trailers` | Scrapes YouTube search results to find and save official game trailer embed URLs. |
| `fetch_steam_data` | Fetches Steam review scores, screenshots, and estimated ownership data from Steam & SteamSpy APIs. Supports `--all` and `--limit` flags. |
| `fetch_hltb` | Fetches HowLongToBeat playtime estimates (Main Story, Main + Extras, Completionist). |

**Usage example:**
```bash
python manage.py fetch_game_details
python manage.py fetch_steam_data --all --limit 10
```

## 🌐 Deployment

The project is deployed on **Render** with the following configuration:

- **Build Command:** `./build.sh` (installs deps, collects static files, runs migrations, loads fixture data)
- **Start Command:** `gunicorn gameawards.wsgi`
- **Static Files:** Served via WhiteNoise middleware
- **Database:** PostgreSQL (automatically configured via `DATABASE_URL`)

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License & Copyright

The underlying source code of this project is provided under the **MIT License** for educational and reference purposes. 

**However, the overall project, including its specific design, branding, layout, and the concept of "The Game Awards Archive" is © All Rights Reserved.** 

You may not directly clone, duplicate, republish, or monetise this exact application or its complete user interface without explicit permission.

---

## ⚖️ Disclaimer

**This is an unofficial, non-commercial fan/portfolio project.** It is not affiliated with, endorsed by, or associated with The Game Awards, Geoff Keighley, or any related entities. All game data, trailers, logos, and related imagery belong to their respective copyright and trademark owners.
