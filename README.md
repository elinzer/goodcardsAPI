### Set up

* Install `pyenv` and `pip` if not already installed
* Set Python 3.12.0 as the local version for this project with `pyenv install 3.12.0` (if not already installed)
  and `pyenv local 3.12.0`
* Create a virtual environment using `pyenv virtualenv 3.12.0 ENV_NAME_HERE`
* Activate the virtual env using `pyenv activate ENV_NAME_HERE`
* While in the virtual env run `pip install -r requirements.txt`

### Running Celery Tasks

Celery is used for background task processing (e.g., fetching cards from Scryfall API).

1. **Start Redis** (required as the message broker):
   ```bash
   redis-server
   # Or if using Homebrew:
   brew services start redis
   ```

2. **Start the Celery worker** (in a separate terminal with virtual env activated):
   ```bash
   cd goodcards2
   celery -A goodcards2 worker --loglevel=info
   ```

3. **Trigger a task**:

   - **Via Django shell**:
     ```bash
     python manage.py shell
     ```
     ```python
     from cards.tasks import fetch_cards_from_scryfall

     # Fetch 10 random cards
     fetch_cards_from_scryfall.delay(limit=10)

     # Or fetch cards from a specific set
     fetch_cards_from_scryfall.delay(set_code='DSK', limit=50)
     ```

   - **Via API endpoint** (if configured in your views)
