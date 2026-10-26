import ccxt
import time
import requests
import cv2
import numpy as np
import json
import logging

logging.basicConfig(filename='bot_stability.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

exchange = ccxt.binance()
TOKEN = "8893498514:AAHkYC4Ui9U9_tvsa6B9g2CMftz1V9ADvJ8"
CHAT_ID = "@CryptoVisionA_bot"


def send_telegram_photo_with_buttons(image_path, caption):
    url = f"https://api.telegram.org/bot{TOKEN}/sendPhoto"

    # أزرار تفاعلية باللغة الإنجليزية للجمهور العالمي
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "📊 Live Refresh", "callback_data": "refresh_market"},
                {"text": "🌐 Channel Link", "url": "https://t.me/CryptoVisionA_bot"}
            ]
        ]
    }

    with open(image_path, 'rb') as photo:
        payload = {
            "chat_id": CHAT_ID,
            "caption": caption,
            "parse_mode": "Markdown",
            "reply_markup": json.dumps(keyboard)
        }
        files = {"photo": photo}
        try:
            requests.post(url, data=payload, files=files)
        except Exception as e:
            logging.error(f"Telegram error: {e}")


def generate_english_chart(symbol, prices, is_hot):
    img = np.zeros((350, 600, 3), dtype=np.uint8)
    img.fill(20)

    min_p, max_p = min(prices), max(prices)
    if max_p == min_p:
        max_p += 1

    points = []
    for i, p in enumerate(prices):
        x = int(i * (560 / (len(prices) - 1))) if len(prices) > 1 else 300
        y = int(300 - ((p - min_p) / (max_p - min_p)) * 240)
        points.append((x, y))

    line_color = (0, 255, 255) if is_hot else (0, 255, 120)

    for i in range(len(points) - 1):
        cv2.line(img, points[i], points[i + 1], line_color, 3)
        cv2.circle(img, points[i + 1], 5, (0, 140, 255), -1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    colored_edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    blended = cv2.addWeighted(img, 0.8, colored_edges, 0.2, 0)

    status_text = "Status: 🔥 HIGH VOLATILITY ALERT!" if is_hot else "Status: AI Vision Active [Global]"
    cv2.putText(blended, f"AI VISION: {symbol}", (25, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2)
    cv2.putText(blended, status_text, (25, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1)

    image_path = "english_chart.png"
    cv2.imwrite(image_path, blended)
    return image_path


def monitor_global_market():
    symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOGE/USDT', 'AVAX/USDT']

    for symbol in symbols:
        try:
            ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=12)
            closing_prices = [candle[4] for candle in ohlcv]

            last_close = closing_prices[-1]
            prev_close = closing_prices[-2]
            change = ((last_close - prev_close) / prev_close) * 100

            is_hot = abs(change) >= 0.5
            img_path = generate_english_chart(symbol, closing_prices, is_hot)

            if is_hot:
                caption = (
                    f"🚨 *AI SMART ALERT: High Volatility Detected!*\n\n"
                    f"🔹 **Pair:** `{symbol}`\n"
                    f"📈 **Change:** `{change:.2f}%` ⚡\n"
                    f"💵 **Price:** `{last_close}`\n"
                    f"🌐 *Market Stream: Global English Feed*"
                )
            else:
                caption = (
                    f"🧠 *AI Vision Technical Report*\n\n"
                    f"🔹 **Pair:** `{symbol}`\n"
                    f"📈 **Change:** `{change:.2f}%`\n"
                    f"💵 **Price:** `{last_close}`\n"
                    f"🌐 *Market Stream: Global English Feed*"
                )

            send_telegram_photo_with_buttons(img_path, caption)
            logging.info(f"Sent English global report for {symbol}")
            time.sleep(3)

        except Exception as e:
            logging.error(f"Error in global monitor for {symbol}: {e}")


if __name__ == "__main__":
    logging.info("Global English Bot started successfully.")
    print("Global English AI Vision Bot is running...")

    while True:
        try:
            monitor_global_market()
        except Exception as outer_e:
            logging.error(f"Outer loop error: {outer_e}")

        time.sleep(300)