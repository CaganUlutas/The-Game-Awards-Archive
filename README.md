# 🏆 The Game Awards Archive

The Game Awards Archive is a Django-based web application that serves as a historic database for all the games nominated and awarded at The Game Awards between 2014-2025. This application provides a comprehensive look at the best video games, featuring extensive details, trailers, and developer information.

> **[💬 README İPUCU:]** *Aşağıdaki yerine tutucu (placeholder) görsellerin kodlarını (`![Görsel Açıklaması](...)` veya `<img .../>`) GitHub üzerinden silip kendi oluşturduğun GIF veya ekran görüntülerini sürükleyip bırakabilirsin. Görsellerini yükledikten sonra bu ipucunu da kendi dosyandan silebilirsin.*

<div align="center">
  <!-- Ana sayfanın hareketli bir GIF'ini buraya eklemen çok şık duracaktır -->
  <img src="https://via.placeholder.com/800x400.png?text=Drop+Your+Main+App+GIF+Here+(e.g.+Home+Page+Video+Auto-playing)" alt="Main App Animation" />
</div>

<br/>

## 📸 GIFs / Gallery

<table align="center">
  <tr>
    <td><img src="https://via.placeholder.com/400x250.png?text=Drop+Home+Page+Screenshot+Here" alt="Home Page"/></td>
    <td><img src="https://via.placeholder.com/400x250.png?text=Drop+Hall+of+Fame+Screenshot+Here" alt="Hall of Fame Details"/></td>
  </tr>
  <tr>
    <td><img src="https://via.placeholder.com/400x250.png?text=Drop+Top+Games+Screenshot+Here" alt="Top Games View"/></td>
    <td><img src="https://via.placeholder.com/400x250.png?text=Drop+Game+Details+Screenshot+Here" alt="Game Details View"/></td>
  </tr>
</table>

## ✨ Features

- **Hall of Fame:** Browse through the winners of the prestigious "Game of the Year" award.
- **Top Games:** Explore the highest-rated games based on their Metacritic scores, complete with pagination.
- **Yearly & Category Filtering:** Discover games by filtering through specific years and award categories on the home page.
- **Rich Game Details:** Integrated with the [RAWG API](https://rawg.io/apidocs) to fetch and display in-depth game information including developers, genres, and release dates.
- **Video Trailers:** Automatically fetches and plays YouTube trailers for Game of the Year winners smoothly with a responsive video background.
- **Responsive Design:** A polished, modern, and visually appealing UI optimized for all devices, featuring custom animations, aesthetic typography, and a premium look.

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **Frontend:** HTML, CSS (Custom styling with modern aesthetics), Vanilla JavaScript
- **Database:** SQLite (Development)
- **External APIs:** RAWG Video Games Database API

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd gameawards
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   Since there might not be a `requirements.txt`, ensure you have the necessary packages:
   ```bash
   pip install django requests
   ```

4. **Environment Variables:**
   Make sure you configure any necessary API Keys (like your RAWG API Key) if required by the custom management commands.

5. **Run Database Migrations:**
   ```bash
   python manage.py migrate
   ```

6. **Fetch Game Data (Custom Commands):**
   The project includes custom logic to populate the database with extensive details from RAWG:
   ```bash
   python manage.py fetch_game_details
   python manage.py fetch_developers
   ```

7. **Run the Development Server:**
   ```bash
   python manage.py runserver
   ```

8. **Experience the Archive:**
   Navigate to `http://127.0.0.1:8000/` in your web browser.

## 📁 Project Structure

- `manage.py`: Django entry point.
- `gameawards/`: Core project settings, URLs, and configurations.
- `awards/`: A Django app containing the main logic.
  - `views.py` & `urls.py`: Request handlers and routing.
  - `models.py`: Database schema definitions for Awards, Nominations, etc.
  - `templates/awards/`: HTML layouts and pages (`home.html`, `game_details.html`, `top_games.html`, etc.).
  - `management/commands/`: Custom scripts built to feed external API data into the local database (`fetch_game_details.py`, `fetch_developers.py`).

## 🤝 Contributing
Contributions, issues, and feature requests are welcome!

## 📝 License & Copyright

The underlying source code of this project is provided under the **MIT License** for educational and reference purposes. 

**However, the overall project, including its specific design, branding, layout, and the concept of "The Game Awards Archive" is © All Rights Reserved.** 

You may not directly clone, duplicate, republish, or monetise this exact application or its complete user interface without explicit permission.

---

## ⚖️ Disclaimer

**This is an unofficial, non-commercial fan/portfolio project.** It is not affiliated with, endorsed by, or associated with The Game Awards, Geoff Keighley, or any related entities. All game data, trailers, logos, and related imagery belong to their respective copyright and trademark owners.
