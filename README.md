# GeoTracker
WORK IN PROGRESS

## Features

- User authentication (login, signup, logout)
- Real-time location tracking
- Display nearby points of interest on a map
- Geofencing capabilities (add/remove geofences)
- Basic UI with Bootstrap

## Setup

1. **Clone the Repository:**

    ```bash
    git clone https://github.com/yourusername/geotracker.git
    cd geotracker
    ```

2. **Create a Virtual Environment:**

    ```bash
    python -m venv .env
    source .env/bin/activate  # On Windows use `.env\Scripts\activate`
    ```

    *seperate files modification needed for .env*

3. **Install Dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure the Database:**

    Edit the `settings.py` file to configure your database settings. The default setup uses SQLite.

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

5. **Run Migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a Superuser (Admin):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the Development Server:**

    ```bash
    python manage.py runserver
    ```

8. **Access the Application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## Key Files

- `views.py`: Contains all the view logic for the application.
- `urls.py`: URL configuration for routing requests to the appropriate views.
- `forms.py`: Contains form classes for user signup and geofence creation.
- `models.py`: Contains the database models, including the `Geofence` model.
- `templates/`: HTML templates for rendering the web pages.
- `static/maps/`: Directory where the generated map HTML files are stored.

## Troubleshooting

- If you encounter issues with the map not loading, ensure the path to the `map.html` file is correct.
- Ensure you have the correct API keys configured in the `views.py` for location tracking and Geoapify services.
- For any authentication issues, ensure you have set up the authentication URLs correctly in your `urls.py` and that the forms are correctly handling CSRF tokens.

## Enhancements

- Add more detailed styles and UI enhancements using Bootstrap or custom CSS.
- Implement additional features such as user profiles, more detailed geofence configurations, or real-time notifications.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License.