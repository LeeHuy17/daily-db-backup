# 🛡️ Daily Database Backup Script

This script automatically backs up `.sql` and `.sqlite3` files every day at 00:00 AM and sends an email notification.

## 🚀 Features
- Auto backup `.sql` and `.sqlite3` files in current directory
- Store backups in `/backup` folder
- Send email notification (success or failure)

## ⚙️ Setup

1. Clone repo
2. Create `.env` from `.env.example`
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
