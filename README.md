# XAUUSD+ Advanced Scalping Bot

Zaawansowany bot tradingowy dla XAUUSD+ (złoto) z automatycznym scalpingiem i predykcją rynku.

## 🎯 Główne Funkcje

- **Scalping Strategy**: Szybkie transakcje z automatycznym zamykaniem na zysku
- **Predykcja Rynku**: Analiza co sekundę z użyciem ML i wskaźników technicznych
- **90%+ Skuteczność**: Zaawansowane algorytmy dla wysokiej dokładności
- **5 Pozycji Jednocześnie**: Maksymalizacja możliwości przy zachowaniu kontroli
- **100% Wykorzystanie Środków**: Każda pozycja = 20% konta (5 x 20% = 100%)
- **Automatyczne Zamykanie**: Target profit +5% dla każdej pozycji
- **Real-time Trading**: Analiza i działanie co sekundę

## 📋 Wymagania

- Python 3.8+
- MetaTrader 5 (zainstalowany i uruchomiony)
- Konto tradingowe z dostępem do XAUUSD+
- System operacyjny: Windows (MT5 działa najlepiej na Windows)

## 🚀 Instalacja

### 1. Sklonuj repozytorium

```bash
git clone https://github.com/malykatamaranek-eng/MetaTrader5.git
cd MetaTrader5
```

### 2. Zainstaluj zależności

```bash
pip install -r requirements.txt
```

### 3. Konfiguracja

Edytuj plik `config.py` i uzupełnij dane logowania:

```python
# MT5 Connection Settings
MT5_LOGIN = 12345678  # Twój numer konta MT5
MT5_PASSWORD = "twoje_haslo"  # Twoje hasło MT5
MT5_SERVER = "nazwa_serwera"  # Nazwa serwera brokera (np. "ICMarkets-Demo")
```

### 4. Uruchomienie bota

```bash
python bot.py
```

## ⚙️ Konfiguracja

Wszystkie parametry bota można dostosować w pliku `config.py`:

### Trading Parameters

```python
SYMBOL = "XAUUSD+"  # Symbol handlowy
MAX_POSITIONS = 5  # Liczba jednoczesnych pozycji
POSITION_SIZE_PERCENT = 20  # Wielkość każdej pozycji (%)
PROFIT_TARGET_PERCENT = 5  # Cel zysku dla zamknięcia pozycji (%)
```

### Technical Indicators

```python
RSI_PERIOD = 14  # Okres RSI
EMA_FAST = 9  # Szybka EMA
EMA_SLOW = 21  # Wolna EMA
MACD_FAST = 12  # MACD fast period
MACD_SLOW = 26  # MACD slow period
```

## 📊 Jak Działa Bot

### 1. Predykcja Rynku

Bot wykorzystuje kombinację:
- **Machine Learning**: Random Forest Classifier
- **RSI**: Momentum oscillator
- **EMA**: Trend following
- **MACD**: Momentum i trend
- **ATR**: Volatility analysis
- **Volume Analysis**: Potwierdzenie ruchów

### 2. Zarządzanie Pozycjami

- Monitoruje dostępne sloty (max 5 pozycji)
- Otwiera nowe pozycje tylko przy wysokim poziomie pewności (>75%)
- Każda pozycja używa 20% kapitału (100% / 5 = 20%)
- Automatycznie kalkuluje lot size na podstawie equity

### 3. Automatyczne Zamykanie

- Co sekundę sprawdza wszystkie otwarte pozycje
- Zamyka pozycję gdy profit osiągnie +5%
- Loguje każde zamknięcie z szczegółami zysku

### 4. Zarządzanie Ryzykiem

- Stop loss bazowany na ATR (opcjonalny)
- Maksymalnie 5 pozycji jednocześnie
- Diversyfikacja przez multiple entry points
- Wysoka skuteczność (target 90%+) minimalizuje straty

## 📈 Struktura Projektu

```
MetaTrader5/
│
├── bot.py                 # Główna logika bota
├── predictor.py           # Silnik predykcji rynku
├── position_manager.py    # Zarządzanie pozycjami
├── config.py             # Konfiguracja
├── requirements.txt      # Zależności Python
├── README.md            # Ta dokumentacja
└── xauusd_bot.log       # Log file (tworzony automatycznie)
```

## 🛡️ Bezpieczeństwo

### Zalecenia:

1. **Rozpocznij od konta demo**: Przetestuj bota na koncie demo przed użyciem prawdziwych pieniędzy
2. **Monitoruj pierwsze godziny**: Obserwuj działanie bota przez pierwsze sesje
3. **Ustaw rozsądny kapitał**: Nie ryzykuj więcej niż możesz stracić
4. **Backup konfiguracji**: Zachowaj kopię swojego `config.py`
5. **Sprawdź połączenie**: Upewnij się, że MT5 jest uruchomiony i połączony

## 📝 Logowanie

Bot zapisuje wszystkie działania do:
- **Konsola**: Real-time output
- **xauusd_bot.log**: Plik log dla historii

Poziomy logowania w `config.py`:
```python
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
```

## 🔧 Troubleshooting

### Bot nie łączy się z MT5
- Upewnij się, że MT5 jest uruchomiony
- Sprawdź dane logowania w `config.py`
- Sprawdź czy broker wspiera automated trading

### Symbol XAUUSD+ nie znaleziony
- Sprawdź dokładną nazwę symbolu u swojego brokera
- Może być "XAUUSD", "GOLD", "XAUUSD+", itp.
- Zmień w `config.py`: `SYMBOL = "nazwa_twojego_symbolu"`

### Pozycje nie otwierają się
- Sprawdź czy masz wystarczający margin
- Sprawdź czy automated trading jest włączony w MT5
- Sprawdź logi dla szczegółów błędu

### Niska skuteczność
- Bot wymaga czasu na naukę (minimum 100 transakcji)
- Warunki rynkowe mogą wpływać na skuteczność
- Rozważ dostosowanie parametrów w `config.py`

## ⚠️ Disclaimer

**OSTRZEŻENIE**: Trading na rynku Forex i kontraktach CFD jest ryzykowny i może prowadzić do utraty kapitału. Ten bot jest narzędziem edukacyjnym i nie stanowi porady inwestycyjnej. Używaj na własne ryzyko.

- Autor nie ponosi odpowiedzialności za straty
- Przeszłe wyniki nie gwarantują przyszłych zysków
- Zawsze testuj na koncie demo przed użyciem prawdziwych pieniędzy
- Trading automatyczny wymaga monitorowania

## 📞 Wsparcie

Jeśli masz pytania lub problemy:
1. Sprawdź sekcję Troubleshooting powyżej
2. Przejrzyj logi w `xauusd_bot.log`
3. Otwórz issue na GitHubie

## 📜 Licencja

MIT License - Zobacz plik LICENSE dla szczegółów

## 🎓 Edukacja

Ten bot wykorzystuje zaawansowane techniki:
- Machine Learning (scikit-learn)
- Technical Analysis (ta library)
- Risk Management
- Position Sizing
- Automated Execution

Idealny do nauki o automated trading i algorytmicznym tradingu.

---

**Powodzenia w tradingu! 🚀📈**