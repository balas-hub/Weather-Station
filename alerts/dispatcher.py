import os
import json
import logging
import requests
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

CONFIG_FILE = os.path.join(settings.BASE_DIR, 'alerts_config.json')

def get_telegram_config():
    """Retrieves Telegram credentials from alerts_config.json or settings.py."""
    config = {
        "bot_token": getattr(settings, 'TELEGRAM_BOT_TOKEN', ''),
        "chat_id": getattr(settings, 'TELEGRAM_CHAT_ID', ''),
        "enabled": False
    }

    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if data.get("telegram_bot_token"):
                    config["bot_token"] = data.get("telegram_bot_token")
                if data.get("telegram_chat_id"):
                    config["chat_id"] = data.get("telegram_chat_id")
                config["enabled"] = data.get("telegram_enabled", bool(config["bot_token"] and config["chat_id"]))
        except Exception as e:
            logger.error(f"[TELEGRAM] Error reading config file: {e}")

    if not config["enabled"] and config["bot_token"] and config["chat_id"]:
        config["enabled"] = True

    return config

def save_telegram_config(bot_token: str, chat_id: str, enabled: bool = True):
    """Saves Telegram credentials to alerts_config.json."""
    config = {
        "telegram_bot_token": bot_token.strip(),
        "telegram_chat_id": chat_id.strip(),
        "telegram_enabled": enabled
    }
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    return config

def send_telegram_alert(title: str, message: str, historical_note: str = "", custom_token: str = None, custom_chat_id: str = None) -> tuple[bool, str]:
    """
    Dispatches notification to Telegram Bot.
    Returns (success: bool, info_message: str).
    """
    cfg = get_telegram_config()
    token = custom_token or cfg.get("bot_token", "")
    chat_id = custom_chat_id or cfg.get("chat_id", "")

    if not token or not chat_id:
        msg = "Telegram Bot Token or Chat ID not configured."
        logger.info(f"[TELEGRAM] {msg}")
        return False, msg

    text = f"🚨 *WEATHER HAZARD ALERT*\n\n*{title}*\n\n{message}"
    if historical_note:
        text += f"\n\n🏛 *Historical Analog:*\n{historical_note}"

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        resp = requests.post(url, json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }, timeout=8)
        
        data = resp.json()
        if resp.status_code == 200 and data.get("ok"):
            return True, "Alert successfully delivered to Telegram!"
        else:
            err = data.get("description", resp.text)
            logger.error(f"[TELEGRAM] API Error: {err}")
            return False, f"Telegram API error: {err}"
    except Exception as e:
        logger.error(f"[TELEGRAM] Request failed: {e}")
        return False, f"Network error sending to Telegram: {str(e)}"

def send_email_alert(title: str, message: str, historical_note: str = "") -> bool:
    """Dispatches emergency email alert to designated recipient."""
    recipient = getattr(settings, 'ALERT_RECIPIENT_EMAIL', '')
    sender = getattr(settings, 'ALERT_EMAIL_USER', '')

    if not recipient or not sender:
        return False

    body = f"WEATHER HAZARD ALERT\n\n{title}\n\n{message}\n\n"
    if historical_note:
        body += f"Historical Analog Pattern:\n{historical_note}\n\n"
    body += "Stay safe.\nPoonamallee Weather Station"

    try:
        send_mail(
            subject=f"[WEATHER ALERT] {title}",
            message=body,
            from_email=sender,
            recipient_list=[recipient],
            fail_silently=True,
        )
        return True
    except Exception:
        return False

def send_sms_alert(title: str, message: str) -> bool:
    """Dispatches SMS alert via Twilio REST API."""
    sid = getattr(settings, 'TWILIO_ACCOUNT_SID', '')
    token = getattr(settings, 'TWILIO_AUTH_TOKEN', '')
    from_num = getattr(settings, 'TWILIO_FROM_NUMBER', '')
    to_num = getattr(settings, 'TWILIO_TO_NUMBER', '')

    if not (sid and token and from_num and to_num):
        return False

    try:
        from twilio.rest import Client
        client = Client(sid, token)
        sms_text = f"WEATHER ALERT: {title} - {message[:120]}"
        client.messages.create(body=sms_text, from_=from_num, to=to_num)
        return True
    except Exception:
        return False

def dispatch_all_channels(alert) -> list:
    """Dispatches alert across Mobile Browser, Telegram, Email, and SMS."""
    dispatched = ['mobile_browser_dashboard']

    hist_note = ""
    if alert.matched_event_name:
        hist_note = f"{alert.matched_event_name} ({alert.matched_event_date})\n{alert.matched_event_impact}\nMatch Confidence: {alert.pattern_similarity_pct:.1f}%"

    ok, _ = send_telegram_alert(alert.title, alert.description, hist_note)
    if ok:
        dispatched.append('telegram')

    if send_email_alert(alert.title, alert.description, hist_note):
        dispatched.append('email')

    if send_sms_alert(alert.title, alert.description):
        dispatched.append('sms')

    alert.channels_dispatched = dispatched
    alert.save(update_fields=['channels_dispatched'])
    return dispatched
