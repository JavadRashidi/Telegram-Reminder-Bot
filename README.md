# Reminder Bot

A Telegram bot built using the Pyrogram library that helps users set and manage reminders, manage administrative tasks, and interact with various bot functionalities.

## Features

### User Features
- **Start Command:** Personalized welcome message with options for navigation.
- **Task Reminder:** Allows users to:
  - Add tasks with reminders at specified times.
  - View all scheduled reminders.
- **Referral System:** Tracks users who join through referral links.
- **VIP Section:** Dedicated VIP section for premium functionalities.
- **About Section:** Provides details about the bot.
- **Support:** Access to the support system for assistance.

### Admin Features
- **Admin Panel:** Restricted access panel for administrators to manage bot and user activities.

### Reminder Management
- Set reminders with user-friendly time input (12-hour or 24-hour format).
- Automatically triggers reminder notifications at the specified times.
- Persistent storage for reminders using the `Database` class.

### Background Tasks
- Periodically checks and sends due reminders.
- Deletes reminders after they are sent.

## Tech Stack
- **Python Libraries:**
  - `pyrogram`: Telegram Bot API implementation.
  - `pyromod`: Enhanced Telegram bot functionalities.
  - `logging`: Logging and debugging support.
  - `asyncio`: Asynchronous task management.
  - `datetime`: Date and time operations.
- **Database Management:** Handled via the custom `dbt.Database` module.

## Files
- `handlers.py`: Contains modules for handling support, referral links, VIP features, and bot information.
- `admin_panel.py`: Logic for the admin panel.
- `config.py`: Configuration file for API credentials and bot settings.

## Commands & Functionalities

### User Commands
- **/start:** Initializes interaction with the bot.
- **/reminder:** Shortcut for opening the reminder feature.
- **/link:** Referral link management.
- **/vip:** Access to VIP features.
- **/about:** Information about the bot.
- **/support:** Access to the support system.

### Admin Commands
- Accessible only to designated Admins defined in the `ADMIN_ID`.

### Inline Options
- Inline keyboard for adding or managing tasks:
  - Add task
  - Complete task

## How it Works
1. **Task Reminder Flow:**
   - Users can input task names and specify reminder times.
   - Tasks are stored in the database and checked periodically.
   - Users receive notification messages when reminders are due.

2. **Admin Panel:**
   - Provides tools for managing users and bot configurations.

3. **Referral System:**
   - Tracks and updates user referrals, notifying the inviter of successful referrals.

## Setup and Usage

1. Clone the repository:
   ```bash
   git clone <repository_url>
