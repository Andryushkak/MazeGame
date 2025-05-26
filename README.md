# Coffee Order App (PyQt)
Цей проєкт демонструє використання шаблонів проектування (Factory Method, Decorator, Observer) на прикладі додатку замовлення кави з графічним інтерфейсом PyQt5.

## Використані шаблони проектування:
- **Factory Method**: створення кави різного типу.
- **Decorator**: додавання інгредієнтів (молоко, шоколад тощо).
- **Observer**: система оновлення статусів замовлення.

## Інструкція
1. Встановіть залежності:
```bash
pip install -r requirements.txt
```

2. Запустіть додаток:
```bash
python main.py
```

3. Для аналізу з SonarQube:
```bash
sonar-scanner
```

## Тестування
```bash
python -m unittest discover tests
```
