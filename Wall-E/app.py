import streamlit as st
import folium
import requests
from streamlit_folium import folium_static
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 📌 Email sozlamalari
EMAIL_ADDRESS = "orazbaevqudaybergen0@gmail.com"
EMAIL_PASSWORD = "jwig ssky uiuy djli"
RECIPIENT_EMAIL = "iskandarovasilbek70@gmail.com"


# Custom CSS - har ikkala rejimda ham yaxshi ko'rinadi
st.markdown("""
    <style>
    /* Text har doim ko'rinadi */
    .stMarkdown, .stText {
        color: var(--text-color) !important;
    }
    
    /* Dark mode uchun */
    @media (prefers-color-scheme: dark) {
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label {
            color: #FFFFFF !important;
        }
    }
    
    /* Light mode uchun */
    @media (prefers-color-scheme: light) {
        .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, label {
            color: #000000 !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# 🌐 Til sozlamalari
LANGUAGES = {
    "uz": {
        "title": "♻️ Axlat Konteynerlarini Kuzatuv Tizimi",
        "subtitle": "Ushbu ilova konteynerlar to'lganda avtomatik xabar yuboradi.",
        "map_title": "🗺️ WALL-E Xarita",
        "container_stats": "📊 Konteynerlar Statistikasi",
        "truck_stats": "🚛 Mashinalar Statistikasi",
        "full": "To'la",
        "half": "Yarim",
        "empty": "Bo'sh",
        "total_trucks": "Jami mashinalar",
        "active": "Faol",
        "loading": "Yuklanmoqda",
        "info": "💡 Markerlarni bosing va ma'lumot oling!",
        "resend_email": "📧 Email qayta yuborish",
        "email_sent": "✅ Email yuborildi!",
        "no_full": "ℹ️ To'lgan konteynerlar yo'q",
        "container": "Konteyner",
        "type": "Turi",
        "status": "Holati",
        "coordinates": "Koordinatalar",
        "driver": "Haydovchi",
        "language": "🌐 Til / Language",
        "success_msg": "ta to'lgan konteyner va eng yaqin mashinalar haqida email yuborildi!",
        "analytics": "📊 Analitika Dashboard",
        "view_analytics": "📈 Analitikani ko'rish",
        "back_to_map": "🗺️ Xaritaga qaytish",
        "daily_stats": "Kunlik Statistika",
        "weekly_stats": "Haftalik Statistika",
        "total_collected": "Jami yig'ilgan axlat",
        "avg_per_day": "Kunlik o'rtacha",
        "most_full": "Eng ko'p to'ladigan konteyner",
        "best_driver": "Eng yaxshi haydovchi",
        "collection_trend": "Axlat yig'ish tendensiyasi (haftalik)",
        "container_performance": "Konteynerlarning ishlashi",
        "truck_efficiency": "Mashinalar samaradorligi",
        "collections": "Yig'ilgan",
        "distance_km": "Masofa (km)",
        "kg": "kg",
        "problem": "Muammo",
        "problem_text": "Hozirgi kunda axlat konteynerlarining haddan tashqari to'lib ketishi va uning atrof-muhitga salbiy ta'siri.",
        "problem_detail": "Axlat yig'ish mashinalari belgilangan jadval bo'yicha ishlaydi. Ba'zi hollarda axlat konteynerlari to'lmaydi, boshqa hollarda esa haddan tashqari to'lib toshadi. Bu axlat tashlash joylarida tartibsizlikka olib keladi.",
        "solutions": "Yechimlar",
        "solution1": "Axlat konteynerlarini to'ldirish va bo'shatish kerakligini avtomatik aniqlash mumkin.",
        "solution2": "Maxsus tortish konteynerlari va konteynerlar holati haqida ma'lumotni 'TOZA HUDUD' tashkilotiga avtomatik uzatish tizimini ishlab chiqish.",
        "solution3": "Maxsus sensorlar asosida qo'ng'iroq markaziga avtomatik xabarnomalar yuborish mumkin.",
        "why_us": "Nega aynan bizning jamoa",
        "why_us_text": "Bizning guruh ayni muammoni hal qila oladi. Bizning guruh a'zolari ko'plab Hackathonlarda qatnashib kelgan, xususan 'Navruz Hackathon 2025, Anti-corruption va Coding Challenge'larda munosib qatnashib kelmoqda. Bundan tashqari, bizning guruh Frontend, Backend, Full-stack, AI developerlardan va UI/UX Designerlardan tashkil topgan.",
        "roadmap_title": "VAQT JADVALI DOIM YAXSHI ISHLAYDI",
        "roadmap_label": "YO'L XARITASI:",
        "test_mode": "Test rejimi",
        "test_mode_period": "Hozirgi - 6 oy",
        "test_mode_desc": "Avval Toshkent shahrida 10 ta maxsus konteyner bilan",
        "next_6_months": "Keyingi 6 oy",
        "next_6_period": "7-12 oy",
        "next_6_desc": "Keyingi Toshkent viloyatida 100 ta maxsus konteyner bilan",
        "next_9_months": "Keyingi 9 oy",
        "next_9_period": "13-21 oy",
        "next_9_desc": "Barcha viloyatlarda 1000 ta konteyner bilan",
        "year_2026": "2026 yil",
        "year_2026_period": "2026 yil",
        "year_2026_desc": "'TOZA HUDUD'ga ulangan barcha konteynerlarni qamrab olish",
        "timeline_viz": "Loyiha vaqt jadvali vizualizatsiyasi",
        "detailed_phase": "Fazalar bo'yicha batafsil ma'lumot",
        "timeline": "Vaqt jadvali",
        "location": "Joylashuv",
        "containers": "Konteynerlar",
        "goal": "Maqsad",
        "test_validate": "Tizimni sinash va tasdiqlash",
        "regional_expansion": "Viloyat bo'ylab kengayish",
        "national_deployment": "Milliy miqyosda joylashtirish",
        "full_integration": "TOZA HUDUD bilan to'liq integratsiya",
        "overall_progress": "Umumiy jarayon",
        "current_phase": "Joriy faza",
        "total_duration": "Jami davomiyligi",
        "target_containers": "Maqsadli konteynerlar",
        "months": "oy",
        "key_milestones": "Asosiy bosqichlar",
        "launch_test": "Toshkentda test fazasini ishga tushirish",
        "expand_region": "Toshkent viloyatiga kengayish (100 konteyner)",
        "deploy_all": "Barcha viloyatlarga joylashtirish (1000 konteyner)",
        "full_toza": "TOZA HUDUD bilan to'liq integratsiya",
        "tech_approach": "WALL-E Texnik Yondashuv",
        "tech_subtitle": "Muammoga yondashuvimiz va AI texnologiyalarimiz",
        "tech_stack": "Tech Stack",
        "ai_tech": "AI Texnologiyalari",
        "architecture": "Arxitektura",
        "innovation": "Innovatsiya",
        "tools_tech": "Foydalanadigan Vositalar va Texnologiyalar",
        "backend_tech": "Backend Texnologiyalari",
        "frontend_tech": "Frontend Texnologiyalari",
        "ai_ml_tech": "AI/ML Texnologiyalari",
        "iot_hardware": "IoT va Uskunalar",
        "tech_distribution": "Texnologiya taqsimoti",
        "ai_usage": "AI Texnologiyalaridan Foydalanish",
        "main_ai_components": "Asosiy AI Komponentlari",
        "computer_vision": "Kompyuter Ko'rishi",
        "route_optimization": "Marshrut Optimizatsiyasi",
        "predictive_analytics": "Bashoratli Tahlil",
        "anomaly_detection": "Anomaliya Aniqlash",
        "technology": "Texnologiya",
        "purpose": "Maqsad",
        "working_principle": "Ishlash printsipi",
        "algorithm": "Algoritm",
        "model": "Model",
        "example_cases": "Misol holatlar",
        "ai_performance": "AI Model Performance Metrics",
        "cv_accuracy": "Computer Vision Aniqligi",
        "route_opt": "Marshrut Optimizatsiyasi",
        "savings": "tejash",
        "prediction_accuracy": "Bashorat Aniqligi",
        "ai_training": "AI Model Training Pipeline",
        "data_collection": "Ma'lumot yig'ish",
        "data_preprocessing": "Ma'lumotlarni tayyorlash",
        "feature_engineering": "Xususiyatlarni yaratish",
        "model_training": "Modelni o'qitish",
        "validation_testing": "Tekshirish",
        "deployment": "Ishga tushirish",
        "monitoring": "Kuzatuv va qayta o'qitish",
        "system_arch": "Tizim Arxitekturasi",
        "layered_arch": "Qatlamli Arxitektura",
        "iot_layer": "IoT Qatlami",
        "edge_computing": "Edge Computing",
        "ai_processing": "AI/ML Processing",
        "app_layer": "Ilova Qatlami",
        "user_interface": "Foydalanuvchi Interfeysi",
        "security_devops": "Xavfsizlik va DevOps",
        "innovation_features": "Innovatsiya va Noyob Xususiyatlar",
        "our_innovation": "Bizning Innovatsion Yondashuvimiz",
        "smart_fill": "Smart Fill Level Detection",
        "smart_fill_desc": "Computer vision va weight sensors kombinatsiyasi orqali 99% aniqlikda to'lganlikni aniqlash",
        "efficiency_increase": "samaradorlik oshishi",
        "ai_route": "AI-Powered Route Optimization",
        "ai_route_desc": "Real-time yo'l tiqinlari va konteyner holati asosida dinamik marshrut tuzish",
        "fuel_saving": "yoqilg'i tejash",
        "predictive_maint": "Predictive Maintenance",
        "predictive_desc": "Konteyner va mashinalar holatini bashorat qilib, ta'mirlashni oldindan rejalashtirish",
        "repair_reduction": "ta'mirlash xarajatlarini kamaytirish",
        "waste_class": "Waste Classification AI",
        "waste_desc": "Axlat turlarini avtomatik ajratish va qayta ishlash uchun optimallash",
        "recycling_efficiency": "qayta ishlash samaradorligi",
        "env_tracking": "Environmental Impact Tracking",
        "env_desc": "CO2 emissiyasini va ekologik ta'sirni real-time kuzatuv",
        "city_ecology": "Shahar ekologiyasini yaxshilash",
        "mobile_first": "Mobile-First Approach",
        "mobile_desc": "Haydovchilar va operatorlar uchun qulay mobile interfeys",
        "user_satisfaction": "user satisfaction",
        "competitive_adv": "Raqobatdagi Afzalliklarimiz",
        "adv1": "To'liq AI-powered yechim",
        "adv2": "Real-time monitoring va analytics",
        "adv3": "Qisqa muddat ichida ROI (3-6 oy)",
        "adv4": "Scalable va flexible arxitektura",
        "adv5": "O'zbekiston sharoitiga moslashtirilgan",
        "adv6": "Open-source komponentlar asosida qurilgan",
        "adv7": "Cloud va on-premise deployment qo'llab-quvvatlash",
        "adv8": "24/7 technical support",
        "impact": "Ta'sir",
        "team_footer": "Iceberg Team",
        "footer_text": "© 2025 Iceberg Team | AI500 Tanlov | Made with ❤️ in Uzbekistan"
    },
    "ru": {
        "title": "♻️ Система Мониторинга Контейнеров",
        "subtitle": "Приложение автоматически отправляет уведомление, когда контейнеры заполнены.",
        "map_title": "🗺️ Карта WALL-E",
        "container_stats": "📊 Статистика Контейнеров",
        "truck_stats": "🚛 Статистика Машин",
        "full": "Полный",
        "half": "Наполовину",
        "empty": "Пустой",
        "total_trucks": "Всего машин",
        "active": "Активный",
        "loading": "Загружается",
        "info": "💡 Нажмите на маркеры для информации!",
        "resend_email": "📧 Отправить email повторно",
        "email_sent": "✅ Email отправлен!",
        "no_full": "ℹ️ Нет полных контейнеров",
        "container": "Контейнер",
        "type": "Тип",
        "status": "Статус",
        "coordinates": "Координаты",
        "driver": "Водитель",
        "language": "🌐 Язык / Language",
        "success_msg": "полных контейнера и информация о ближайших машинах отправлена!",
        "analytics": "📊 Аналитическая Панель",
        "view_analytics": "📈 Смотреть аналитику",
        "back_to_map": "🗺️ Вернуться к карте",
        "daily_stats": "Дневная Статистика",
        "weekly_stats": "Недельная Статистика",
        "total_collected": "Всего собрано мусора",
        "avg_per_day": "Среднее в день",
        "most_full": "Чаще всего заполняется",
        "best_driver": "Лучший водитель",
        "collection_trend": "Тенденция сбора (недельная)",
        "container_performance": "Эффективность контейнеров",
        "truck_efficiency": "Эффективность машин",
        "collections": "Собрано",
        "distance_km": "Расстояние (км)",
        "kg": "кг",
        "problem": "Проблема",
        "problem_text": "В настоящее время чрезмерное переполнение контейнеров для мусора и его негативное влияние на окружающую среду.",
        "problem_detail": "Мусоровозы работают по установленному графику. В некоторых случаях контейнеры остаются незаполненными, в других — переполняются. Это приводит к беспорядку в местах сбора мусора.",
        "solutions": "Решения",
        "solution1": "Можно автоматически определять, когда контейнеры нужно наполнять и опорожнять.",
        "solution2": "Разработка специальных взвешивающих контейнеров и автоматическая передача информации о состоянии контейнеров в организацию 'ЧИСТАЯ ТЕРРИТОРИЯ'.",
        "solution3": "Автоматические уведомления могут отправляться в call-центр на основе специальных датчиков.",
        "why_us": "Почему именно наша команда",
        "why_us_text": "Наша команда может решить эту проблему. Члены нашей команды участвовали во многих хакатонах, особенно в 'Navruz Hackathon 2025, Anti-corruption и Coding Challenge'. Кроме того, наша команда состоит из Frontend, Backend, Full-stack, AI разработчиков и UI/UX дизайнеров.",
        "roadmap_title": "ВРЕМЕННАЯ ШКАЛА ВСЕГДА РАБОТАЕТ ОТЛИЧНО",
        "roadmap_label": "ДОРОЖНАЯ КАРТА:",
        "test_mode": "Тестовый режим",
        "test_mode_period": "Текущий - 6 месяцев",
        "test_mode_desc": "Сначала в городе Ташкент с 10 специализированными контейнерами",
        "next_6_months": "Следующие 6 месяцев",
        "next_6_period": "7-12 месяцев",
        "next_6_desc": "Затем в Ташкентской области со 100 специализированными контейнерами",
        "next_9_months": "Следующие 9 месяцев",
        "next_9_period": "13-21 месяцев",
        "next_9_desc": "Во всех регионах с 1000 контейнерами",
        "year_2026": "2026 год",
        "year_2026_period": "2026 год",
        "year_2026_desc": "Покрыть все контейнеры, подключенные к 'ЧИСТАЯ ТЕРРИТОРИЯ'",
        "timeline_viz": "Визуализация временной шкалы проекта",
        "detailed_phase": "Подробная информация по фазам",
        "timeline": "Временная шкала",
        "location": "Местоположение",
        "containers": "Контейнеры",
        "goal": "Цель",
        "test_validate": "Тестирование и проверка системы",
        "regional_expansion": "Региональное расширение",
        "national_deployment": "Развертывание по всей стране",
        "full_integration": "Полная интеграция с ЧИСТАЯ ТЕРРИТОРИЯ",
        "overall_progress": "Общий прогресс",
        "current_phase": "Текущая фаза",
        "total_duration": "Общая длительность",
        "target_containers": "Целевые контейнеры",
        "months": "месяцев",
        "key_milestones": "Ключевые вехи",
        "launch_test": "Запуск тестовой фазы в Ташкенте",
        "expand_region": "Расширение в Ташкентскую область (100 контейнеров)",
        "deploy_all": "Развертывание во всех регионах (1000 контейнеров)",
        "full_toza": "Полная интеграция с ЧИСТАЯ ТЕРРИТОРИЯ",
        "tech_approach": "Технический подход WALL-E",
        "tech_subtitle": "Наш подход к проблеме и AI технологии",
        "tech_stack": "Технологический стек",
        "ai_tech": "AI Технологии",
        "architecture": "Архитектура",
        "innovation": "Инновации",
        "tools_tech": "Используемые инструменты и технологии",
        "backend_tech": "Backend Технологии",
        "frontend_tech": "Frontend Технологии",
        "ai_ml_tech": "AI/ML Технологии",
        "iot_hardware": "IoT и Оборудование",
        "tech_distribution": "Распределение технологий",
        "ai_usage": "Использование AI технологий",
        "main_ai_components": "Основные AI компоненты",
        "computer_vision": "Компьютерное зрение",
        "route_optimization": "Оптимизация маршрута",
        "predictive_analytics": "Прогнозная аналитика",
        "anomaly_detection": "Обнаружение аномалий",
        "technology": "Технология",
        "purpose": "Назначение",
        "working_principle": "Принцип работы",
        "algorithm": "Алгоритм",
        "model": "Модель",
        "example_cases": "Примеры случаев",
        "ai_performance": "Метрики производительности AI модели",
        "cv_accuracy": "Точность компьютерного зрения",
        "route_opt": "Оптимизация маршрута",
        "savings": "экономия",
        "prediction_accuracy": "Точность прогноза",
        "ai_training": "Процесс обучения AI модели",
        "data_collection": "Сбор данных",
        "data_preprocessing": "Предобработка данных",
        "feature_engineering": "Создание признаков",
        "model_training": "Обучение модели",
        "validation_testing": "Проверка",
        "deployment": "Развертывание",
        "monitoring": "Мониторинг и переобучение",
        "system_arch": "Системная архитектура",
        "layered_arch": "Слоистая архитектура",
        "iot_layer": "IoT слой",
        "edge_computing": "Edge Computing",
        "ai_processing": "AI/ML обработка",
        "app_layer": "Прикладной слой",
        "user_interface": "Пользовательский интерфейс",
        "security_devops": "Безопасность и DevOps",
        "innovation_features": "Инновации и уникальные возможности",
        "our_innovation": "Наш инновационный подход",
        "smart_fill": "Умное определение уровня заполнения",
        "smart_fill_desc": "Комбинация компьютерного зрения и весовых датчиков с точностью 99%",
        "efficiency_increase": "повышение эффективности",
        "ai_route": "AI-оптимизация маршрута",
        "ai_route_desc": "Динамическое построение маршрута на основе пробок и состояния контейнеров",
        "fuel_saving": "экономия топлива",
        "predictive_maint": "Прогнозное обслуживание",
        "predictive_desc": "Прогнозирование состояния контейнеров и машин для планирования ремонта",
        "repair_reduction": "снижение расходов на ремонт",
        "waste_class": "AI классификация отходов",
        "waste_desc": "Автоматическая сортировка типов отходов и оптимизация переработки",
        "recycling_efficiency": "эффективность переработки",
        "env_tracking": "Отслеживание экологического воздействия",
        "env_desc": "Real-time мониторинг выбросов CO2 и экологического воздействия",
        "city_ecology": "Улучшение городской экологии",
        "mobile_first": "Mobile-First подход",
        "mobile_desc": "Удобный мобильный интерфейс для водителей и операторов",
        "user_satisfaction": "удовлетворенность пользователей",
        "competitive_adv": "Наши конкурентные преимущества",
        "adv1": "Полностью AI-powered решение",
        "adv2": "Real-time мониторинг и аналитика",
        "adv3": "Быстрая окупаемость (3-6 месяцев)",
        "adv4": "Масштабируемая и гибкая архитектура",
        "adv5": "Адаптировано к условиям Узбекистана",
        "adv6": "Построено на open-source компонентах",
        "adv7": "Поддержка Cloud и on-premise развертывания",
        "adv8": "Техническая поддержка 24/7",
        "impact": "Влияние",
        "team_footer": "Команда Iceberg",
        "footer_text": "© 2025 Команда Iceberg | Конкурс AI500 | Сделано с ❤️ в Узбекистане"
    },
    "en": {
        "title": "♻️ Waste Container Monitoring System",
        "subtitle": "This application automatically sends a notification when containers are full.",
        "map_title": "🗺️ WALL-E Map",
        "container_stats": "📊 Container Statistics",
        "truck_stats": "🚛 Truck Statistics",
        "full": "Full",
        "half": "Half",
        "empty": "Empty",
        "total_trucks": "Total Trucks",
        "active": "Active",
        "loading": "Loading",
        "info": "💡 Click on markers for information!",
        "resend_email": "📧 Resend Email",
        "email_sent": "✅ Email sent!",
        "no_full": "ℹ️ No full containers",
        "container": "Container",
        "type": "Type",
        "status": "Status",
        "coordinates": "Coordinates",
        "driver": "Driver",
        "language": "🌐 Language / Til",
        "success_msg": "full containers and nearest trucks info sent via email!",
        "analytics": "📊 Analytics Dashboard",
        "view_analytics": "📈 View Analytics",
        "back_to_map": "🗺️ Back to Map",
        "daily_stats": "Daily Statistics",
        "weekly_stats": "Weekly Statistics",
        "total_collected": "Total Waste Collected",
        "avg_per_day": "Average per Day",
        "most_full": "Most Filled Container",
        "best_driver": "Best Driver",
        "collection_trend": "Collection Trend (Weekly)",
        "container_performance": "Container Performance",
        "truck_efficiency": "Truck Efficiency",
        "collections": "Collections",
        "distance_km": "Distance (km)",
        "kg": "kg",
        "problem": "Problem",
        "problem_text": "Nowadays, the excessive overflow of waste containers and its negative impact on the environment.",
        "problem_detail": "Waste collection vehicles operate according to a set schedule. In some cases, waste containers remain unfilled, while in others, they overflow excessively. This leads to disorder in waste disposal areas.",
        "solutions": "Solutions",
        "solution1": "It is possible to automatically determine when waste containers need to be filled and emptied.",
        "solution2": "Development of special weighing containers and automatic transmission of information about the condition of containers to the 'CLEAN AREA' organization.",
        "solution3": "Automatic notifications can be sent to the call center based on special sensors.",
        "why_us": "Why Our Team",
        "why_us_text": "Our team can solve this problem. Our team members have participated in many hackathons, especially 'Navruz Hackathon 2025, Anti-corruption and Coding Challenges'. Additionally, our team consists of Frontend, Backend, Full-stack, AI developers and UI/UX Designers.",
        "roadmap_title": "A TIMELINE ALWAYS WORKS FINE",
        "roadmap_label": "ROAD MAP:",
        "test_mode": "Test mode",
        "test_mode_period": "Current - 6 months",
        "test_mode_desc": "First in Tashkent city with 10 specialized containers",
        "next_6_months": "Next 6 Months",
        "next_6_period": "Month 7-12",
        "next_6_desc": "Next in Tashkent region with 100 specialized containers",
        "next_9_months": "Next 9 Months",
        "next_9_period": "Month 13-21",
        "next_9_desc": "In All Regions with 1000 containers",
        "year_2026": "2026",
        "year_2026_period": "Year 2026",
        "year_2026_desc": "Cover every container which is connected to 'CLEAN AREA'",
        "timeline_viz": "Project Timeline Visualization",
        "detailed_phase": "Detailed Phase Information",
        "timeline": "Timeline",
        "location": "Location",
        "containers": "Containers",
        "goal": "Goal",
        "test_validate": "Test and validate the system",
        "regional_expansion": "Regional expansion",
        "national_deployment": "National scale deployment",
        "full_integration": "Full integration with CLEAN AREA",
        "overall_progress": "Overall Progress",
        "current_phase": "Current Phase",
        "total_duration": "Total Duration",
        "target_containers": "Target Containers",
        "months": "months",
        "key_milestones": "Key Milestones",
        "launch_test": "Launch test phase in Tashkent",
        "expand_region": "Expand to Tashkent region (100 containers)",
        "deploy_all": "Deploy across all regions (1000 containers)",
        "full_toza": "Full CLEAN AREA integration",
        "tech_approach": "WALL-E Technical Approach",
        "tech_subtitle": "Our approach to the problem and AI technologies",
        "tech_stack": "Tech Stack",
        "ai_tech": "AI Technologies",
        "architecture": "Architecture",
        "innovation": "Innovation",
        "tools_tech": "Tools and Technologies Used",
        "backend_tech": "Backend Technologies",
        "frontend_tech": "Frontend Technologies",
        "ai_ml_tech": "AI/ML Technologies",
        "iot_hardware": "IoT & Hardware",
        "tech_distribution": "Technology Distribution",
        "ai_usage": "Using AI Technologies",
        "main_ai_components": "Main AI Components",
        "computer_vision": "Computer Vision",
        "route_optimization": "Route Optimization",
        "predictive_analytics": "Predictive Analytics",
        "anomaly_detection": "Anomaly Detection",
        "technology": "Technology",
        "purpose": "Purpose",
        "working_principle": "Working Principle",
        "algorithm": "Algorithm",
        "model": "Model",
        "example_cases": "Example Cases",
        "ai_performance": "AI Model Performance Metrics",
        "cv_accuracy": "Computer Vision Accuracy",
        "route_opt": "Route Optimization",
        "savings": "savings",
        "prediction_accuracy": "Prediction Accuracy",
        "ai_training": "AI Model Training Pipeline",
        "data_collection": "Data Collection",
        "data_preprocessing": "Data Preprocessing",
        "feature_engineering": "Feature Engineering",
        "model_training": "Model Training",
        "validation_testing": "Validation & Testing",
        "deployment": "Deployment",
        "monitoring": "Monitoring & Retraining",
        "system_arch": "System Architecture",
        "layered_arch": "Layered Architecture",
        "iot_layer": "IoT Layer",
        "edge_computing": "Edge Computing",
        "ai_processing": "AI/ML Processing",
        "app_layer": "Application Layer",
        "user_interface": "User Interface",
        "security_devops": "Security & DevOps",
        "innovation_features": "Innovation & Unique Features",
        "our_innovation": "Our Innovation Approach",
        "smart_fill": "Smart Fill Level Detection",
        "smart_fill_desc": "99% accuracy in detecting fullness through combination of computer vision and weight sensors",
        "efficiency_increase": "efficiency increase",
        "ai_route": "AI-Powered Route Optimization",
        "ai_route_desc": "Dynamic route planning based on real-time traffic and container status",
        "fuel_saving": "fuel saving",
        "predictive_maint": "Predictive Maintenance",
        "predictive_desc": "Predicting container and vehicle conditions to plan maintenance in advance",
        "repair_reduction": "repair cost reduction",
        "waste_class": "Waste Classification AI",
        "waste_desc": "Automatic waste type sorting and recycling optimization",
        "recycling_efficiency": "recycling efficiency",
        "env_tracking": "Environmental Impact Tracking",
        "env_desc": "Real-time tracking of CO2 emissions and environmental impact",
        "city_ecology": "City ecology improvement",
        "mobile_first": "Mobile-First Approach",
        "mobile_desc": "Convenient mobile interface for drivers and operators",
        "user_satisfaction": "user satisfaction",
        "competitive_adv": "Our Competitive Advantages",
        "adv1": "Fully AI-powered solution",
        "adv2": "Real-time monitoring and analytics",
        "adv3": "Quick ROI (3-6 months)",
        "adv4": "Scalable and flexible architecture",
        "adv5": "Adapted to Uzbekistan conditions",
        "adv6": "Built on open-source components",
        "adv7": "Cloud and on-premise deployment support",
        "adv8": "24/7 technical support",
        "impact": "Impact",
        "team_footer": "Iceberg Team",
        "footer_text": "© 2025 Iceberg Team | AI500 Competition | Made with ❤️ in Uzbekistan"
    }
}

# Til tanlash (session state)
if 'language' not in st.session_state:
    st.session_state.language = 'uz'

if 'view_mode' not in st.session_state:
    st.session_state.view_mode = 'map'

def get_text(key):
    """Tanlangan tildagi matnni olish"""
    return LANGUAGES[st.session_state.language][key]

# 📊 Namunaviy analitika ma'lumotlari
def generate_analytics_data():
    """Test uchun analitika ma'lumotlarini yaratish"""
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    
    weekly_data = pd.DataFrame({
        'date': dates,
        'waste_collected_kg': [450, 520, 480, 510, 490, 530, 500]
    })
    
    container_data = pd.DataFrame({
        'container_id': ['#1', '#2', '#3', '#4', '#5'],
        'collections': [12, 8, 15, 11, 9],
        'total_kg': [1200, 800, 1500, 1100, 900]
    })
    
    truck_data = pd.DataFrame({
        'truck': ['Truck-001', 'Truck-002', 'Truck-003'],
        'driver': ['Alisher', 'Bobur', 'Sardor'],
        'trips': [25, 22, 28],
        'distance_km': [145, 132, 156],
        'waste_kg': [2500, 2200, 2800]
    })
    
    return weekly_data, container_data, truck_data

# 📌 Masofa hisoblash funksiyasi (km)
def calculate_distance(lat1, lon1, lat2, lon2):
    from math import radians, sin, cos, sqrt, atan2
    R = 6371
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    return distance

def find_nearest_truck(container, trucks):
    min_distance = float('inf')
    nearest_truck = None
    for truck in trucks:
        distance = calculate_distance(
            container['lat'], container['lon'],
            truck['lat'], truck['lon']
        )
        if distance < min_distance:
            min_distance = distance
            nearest_truck = truck
    return nearest_truck, min_distance

def send_full_container_alert(containers, trucks):
    full_containers = [c for c in containers if c["status"] == get_text("full")]
    if not full_containers:
        return False
    
    subject = "🚨 Ogohlantirish: To'lib ketgan konteynerlar mavjud!"
    body = "Quyidagi konteynerlar to'lib ketgan va bo'shatilishi kerak:\n\n"
    body += "=" * 60 + "\n\n"
    
    for container in full_containers:
        google_maps_link = f"https://www.google.com/maps?q={container['lat']},{container['lon']}"
        nearest_truck, distance = find_nearest_truck(container, trucks)
        
        body += f"📦 KONTEYNER #{container['id']}\n"
        body += f"   • Turi: {container['type']}\n"
        body += f"   • Holati: {container['status']}\n"
        body += f"   • 📍 Joylashuv: {google_maps_link}\n"
        body += f"   • Koordinatalar: {container['lat']:.4f}, {container['lon']:.4f}\n\n"
        
        if nearest_truck:
            body += f"   🚛 ENG YAQIN MASHINA:\n"
            body += f"   • Nomi: {nearest_truck['name']}\n"
            body += f"   • Haydovchi: {nearest_truck['driver']}\n"
            body += f"   • Holati: {nearest_truck['status']}\n"
            body += f"   • Masofa: {distance:.2f} km\n"
            body += f"   • Taxminiy yetib borish vaqti: {int(distance * 3)} daqiqa\n"
        
        body += "\n" + "-" * 60 + "\n\n"
    
    body += "⚠️ Iltimos, darhol bo'shatish choralarini ko'ring!\n"
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        st.error(f"❌ Email yuborishda xatolik: {e}")
        return False

def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode()
        
        page_bg_img = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_img}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)
    except FileNotFoundError:
        pass

# **Streamlit sahifasi**
st.set_page_config(page_title="WALL-E APP", layout="wide")

# Background
add_bg_from_local("background.png")

st.markdown(
    """
    <style>
    .stApp {
        margin-top: 0px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Ma'lumotlarni oldindan tayyorlash (ikkala view uchun kerak)
containers = [
    {"id": 1, "lat": 41.2995, "lon": 69.2401, "type": "Plastik", "status": get_text("full")},
    {"id": 2, "lat": 41.3111, "lon": 69.2797, "type": "Qog'oz", "status": get_text("empty")},
    {"id": 3, "lat": 41.2856, "lon": 69.2034, "type": "Shisha", "status": get_text("half")},
    {"id": 4, "lat": 41.3267, "lon": 69.2887, "type": "Metall", "status": get_text("full")},
    {"id": 5, "lat": 41.2709, "lon": 69.2164, "type": "Plastik", "status": get_text("empty")},
]

trucks = [
    {"id": 1, "name": "Truck-001", "lat": 41.3111, "lon": 69.2401, "status": get_text("active"), "driver": "Alisher"},
    {"id": 2, "name": "Truck-002", "lat": 41.2700, "lon": 69.2500, "status": get_text("loading"), "driver": "Bobur"},
    {"id": 3, "name": "Truck-003", "lat": 41.3400, "lon": 69.2100, "status": get_text("active"), "driver": "Sardor"},
]

# 🌐 Til tanlash (Sidebar'da yuqorida)
st.sidebar.markdown(f"### {get_text('language')}")
selected_lang = st.sidebar.selectbox(
    "",
    options=['uz', 'ru', 'en'],
    format_func=lambda x: {"uz": "O'zbekcha", "ru": "Русский", "en": "English"}[x],
    index=['uz', 'ru', 'en'].index(st.session_state.language),
    key='lang_selector'
)

if selected_lang != st.session_state.language:
    st.session_state.language = selected_lang
    st.session_state.email_sent = False
    st.rerun()

st.sidebar.markdown("---")

# 📊 View mode switcher
col_map, col_analytics = st.sidebar.columns(2)
if col_map.button("🗺️", use_container_width=True, help=get_text('back_to_map')):
    st.session_state.view_mode = 'map'
    st.rerun()
if col_analytics.button("📊", use_container_width=True, help=get_text('view_analytics')):
    st.session_state.view_mode = 'analytics'
    st.rerun()

st.sidebar.markdown("---")

# Konteynerlar statistikasi (Sidebar)
st.sidebar.header(get_text("container_stats"))
tola = len([c for c in containers if c["status"] == get_text("full")])
yarim = len([c for c in containers if c["status"] == get_text("half")])
bosh = len([c for c in containers if c["status"] == get_text("empty")])

col1, col2, col3 = st.sidebar.columns(3)
col1.metric(f"🔴 {get_text('full')}", tola)
col2.metric(f"🟠 {get_text('half')}", yarim)
col3.metric(f"🟢 {get_text('empty')}", bosh)

st.sidebar.markdown("---")

# 🚛 Mashinalar statistikasi (Sidebar)
st.sidebar.header(get_text("truck_stats"))
faol = len([t for t in trucks if t["status"] == get_text("active")])
yuklanmoqda = len([t for t in trucks if t["status"] == get_text("loading")])
total_trucks = len(trucks)

st.sidebar.metric(get_text("total_trucks"), total_trucks)
st.sidebar.metric(f"🔵 {get_text('active')}", faol)
st.sidebar.metric(f"🟣 {get_text('loading')}", yuklanmoqda)

st.sidebar.markdown("---")
st.sidebar.info(get_text("info"))

# 📧 Qo'lda email yuborish tugmasi
st.sidebar.markdown("---")
if st.sidebar.button(get_text("resend_email")):
    if send_full_container_alert(containers, trucks):
        st.sidebar.success(get_text("email_sent"))
    else:
        st.sidebar.info(get_text("no_full"))

# 🔀 View Mode bo'yicha ko'rinish
if st.session_state.view_mode == 'map':
    # ========== XARITA KO'RINISHI ==========
    st.markdown(f"<h1 style='font-size: 70px;color: white;text-align: center;'>{get_text('title')}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='color: white;text-align: center;'>{get_text('subtitle')}</h1>", unsafe_allow_html=True)
    st.title(get_text('map_title'))
    
    # 📧 Sahifa yuklanganida email yuborish (faqat bir marta)
    if 'email_sent' not in st.session_state:
        st.session_state.email_sent = False
    
    if not st.session_state.email_sent:
        full_count = len([c for c in containers if c["status"] == get_text("full")])
        if full_count > 0:
            if send_full_container_alert(containers, trucks):
                st.session_state.email_sent = True
                st.success(f"✅ {full_count} {get_text('success_msg')}")
    
    # Xarita yaratish
    m = folium.Map(location=[41.2995, 69.2401], zoom_start=12)
    
    # Konteynerlarni xaritaga qo'shish
    for container in containers:
        if container["status"] == get_text("full"):
            color = "red"
            icon = "exclamation-sign"
        elif container["status"] == get_text("half"):
            color = "orange"
            icon = "warning-sign"
        else:
            color = "green"
            icon = "ok-sign"
        
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: #2c3e50;">{get_text('container')} #{container['id']}</h4>
            <hr style="margin: 5px 0;">
            <p style="margin: 5px 0;"><b>{get_text('type')}:</b> {container['type']}</p>
            <p style="margin: 5px 0;"><b>{get_text('status')}:</b> <span style="color: {color};">{container['status']}</span></p>
            <p style="margin: 5px 0;"><b>{get_text('coordinates')}:</b><br>
            {container['lat']:.4f}, {container['lon']:.4f}</p>
        </div>
        """
        
        folium.Marker(
            location=[container["lat"], container["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            tooltip=f"{get_text('container')} #{container['id']} - {container['type']}",
            icon=folium.Icon(color=color, icon=icon, prefix='glyphicon')
        ).add_to(m)
    
    # 🚛 Mashinalarni xaritaga qo'shish
    for truck in trucks:
        if truck["status"] == get_text("active"):
            truck_color = "#2196F3"
            truck_emoji = "🚛"
        elif truck["status"] == get_text("loading"):
            truck_color = "#9C27B0"
            truck_emoji = "🚚"
        else:
            truck_color = "#757575"
            truck_emoji = "🚙"
        
        truck_popup_html = f"""
        <div style="font-family: Arial; width: 240px; padding: 10px;">
            <h4 style="margin: 0; color: {truck_color};">🚛 {truck['name']}</h4>
            <hr style="margin: 8px 0; border: 1px solid {truck_color};">
            <p style="margin: 5px 0; font-size: 14px;"><b>👤 {get_text('driver')}:</b> {truck['driver']}</p>
            <p style="margin: 5px 0; font-size: 14px;"><b>📊 {get_text('status')}:</b> <span style="color: {truck_color}; font-weight: bold;">{truck['status']}</span></p>
            <p style="margin: 5px 0; font-size: 12px; color: #666;"><b>📍 {get_text('coordinates')}:</b><br>
            {truck['lat']:.4f}, {truck['lon']:.4f}</p>
        </div>
        """
        
        truck_icon_html = f"""
        <div style="
            font-size: 32px;
            text-align: center;
            background-color: white;
            border: 3px solid {truck_color};
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
        ">
            {truck_emoji}
        </div>
        """
        
        folium.Marker(
            location=[truck["lat"], truck["lon"]],
            popup=folium.Popup(truck_popup_html, max_width=260),
            tooltip=f"🚛 {truck['name']} - {truck['status']}",
            icon=folium.DivIcon(html=truck_icon_html)
        ).add_to(m)
    
    folium_static(m, width=1200, height=600)
    
    # Problem va yechimlar
    st.markdown(f"# {get_text('problem')}")
    st.markdown(f"### {get_text('problem_text')}")
    st.markdown(f"### {get_text('problem_detail')}")
    
    st.markdown(f"# {get_text('solutions')}")
    st.markdown(f"### {get_text('solution1')}")
    st.markdown(f"### {get_text('solution2')}")
    st.markdown(f"### {get_text('solution3')}")

else:
    # ========== ANALYTICS DASHBOARD ==========
    st.markdown(f"<h1 style='font-size: 60px;color: white;text-align: center;'>{get_text('analytics')}</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    weekly_data, container_data, truck_data = generate_analytics_data()
    
    # 📊 Asosiy metriklar
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label=f"📦 {get_text('total_collected')}",
            value=f"{weekly_data['waste_collected_kg'].sum()} {get_text('kg')}",
            delta=f"+{weekly_data['waste_collected_kg'].iloc[-1]} {get_text('kg')}"
        )
    
    with col2:
        avg_daily = int(weekly_data['waste_collected_kg'].mean())
        st.metric(
            label=f"📈 {get_text('avg_per_day')}",
            value=f"{avg_daily} {get_text('kg')}",
            delta=f"{((weekly_data['waste_collected_kg'].iloc[-1] - avg_daily) / avg_daily * 100):.1f}%"
        )
    
    with col3:
        most_full_container = container_data.loc[container_data['collections'].idxmax()]
        st.metric(
            label=f"🏆 {get_text('most_full')}",
            value=f"{most_full_container['container_id']}",
            delta=f"{most_full_container['collections']} {get_text('collections')}"
        )
    
    with col4:
        best_driver_row = truck_data.loc[truck_data['waste_kg'].idxmax()]
        st.metric(
            label=f"⭐ {get_text('best_driver')}",
            value=best_driver_row['driver'],
            delta=f"{best_driver_row['waste_kg']} {get_text('kg')}"
        )
    
    st.markdown("---")
    
    # 📈 Haftalik trend grafigi
    st.subheader(f"📈 {get_text('collection_trend')}")
    fig_trend = px.line(
        weekly_data, 
        x='date', 
        y='waste_collected_kg',
        markers=True,
        line_shape='spline'
    )
    fig_trend.update_traces(line_color='#00C853', marker=dict(size=10))
    fig_trend.update_layout(
        xaxis_title="",
        yaxis_title=get_text('kg'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=400
    )
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # 📊 Ikki ustunli grafiklar
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader(f"📦 {get_text('container_performance')}")
        fig_containers = px.bar(
            container_data,
            x='container_id',
            y='total_kg',
            color='collections',
            color_continuous_scale='Viridis'
        )
        fig_containers.update_layout(
            xaxis_title="",
            yaxis_title=get_text('kg'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            showlegend=False
        )
        st.plotly_chart(fig_containers, use_container_width=True)
    
    with col_right:
        st.subheader(f"🚛 {get_text('truck_efficiency')}")
        fig_trucks = go.Figure()
        fig_trucks.add_trace(go.Bar(
            name=get_text('distance_km'),
            x=truck_data['truck'],
            y=truck_data['distance_km'],
            marker_color='#2196F3'
        ))
        fig_trucks.add_trace(go.Bar(
            name=get_text('kg'),
            x=truck_data['truck'],
            y=truck_data['waste_kg'] / 10,
            marker_color="#9B0A0A"
        ))
        fig_trucks.update_layout(
            barmode='group',
            xaxis_title="",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_trucks, use_container_width=True)
    
    # 📋 Jadval
    st.markdown("---")
    st.subheader(f"📋 {get_text('truck_stats')}")
    truck_display = truck_data.copy()
    truck_display.columns = ['Mashina', get_text('driver'), 'Trips', get_text('distance_km'), get_text('kg')]
    st.dataframe(truck_display, use_container_width=True, hide_index=True)


# Footer - Har ikkala view uchun ham
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 10px; margin-top: 50px;'>
    <h3 style='color: white; margin-bottom: 15px;'>👥 {get_text('team_footer')}</h3>
    <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 5px 0;font-size: 20px'>
        🎯 Iskandarov Asilbek - Project Manager<br>
        💻 Sarmonov Orifjon - Full Stack Developer<br>
        ⚙️ Urazbaev Qudaybergen - Backend Developer<br>
        🤖 Esanov Jafar - AI Developer<br>
        🎨 Sherov Ilhom - UI/UX Designer
    </p>
    <p style='color: rgba(255,255,255,0.6); font-size: 12px; margin-top: 15px;'>
        {get_text('footer_text')}
    </p>
</div>
""", unsafe_allow_html=True)


# ========== NEGA BIZNING JAMOA ==========
st.markdown(f"## {get_text('why_us')}")
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 20px; background: rgba(0,0,0,0.2); border-radius: 10px; margin-top: 50px;'>
    <h3 style='color: white; margin-bottom: 15px;'>
    <p style='color: rgba(255,255,255,0.8); font-size: 14px; margin: 5px 0; font-size: 20px'>
     {get_text('why_us_text')}<br>
</div>
""", unsafe_allow_html=True)


# ========== ROADMAP ==========
st.markdown("---")
st.markdown(f"""
<style>
    .roadmap-header {{
        background: #0f7c9a;
        color: white;
        padding: 30px;
        border-radius: 50px;
        text-align: center;
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 50px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    .roadmap-label {{
        background: #c82333;
        color: white;
        padding: 15px 30px;
        font-size: 32px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 30px;
        letter-spacing: 2px;
    }}
    .phase-card {{
        background: white;
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }}
    .phase-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 12px 35px rgba(0,0,0,0.2);
    }}
    .phase-title {{
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 15px;
        color: #2c3e50;
    }}
    .phase-description {{
        font-size: 18px;
        color: #555;
        line-height: 1.6;
    }}
</style>
""", unsafe_allow_html=True)

st.markdown(f'<div class="roadmap-header">{get_text("roadmap_title")}</div>', unsafe_allow_html=True)
st.markdown(f'<div class="roadmap-label">{get_text("roadmap_label")}</div>', unsafe_allow_html=True)

# Timeline ma'lumotlari
phases = [
    {
        "title": get_text("test_mode"),
        "period": get_text("test_mode_period"),
        "description": get_text("test_mode_desc"),
        "color": "#3498db",
        "icon": "🧪",
        "status": "active"
    },
    {
        "title": get_text("next_6_months"),
        "period": get_text("next_6_period"),
        "description": get_text("next_6_desc"),
        "color": "#95a5a6",
        "icon": "📍",
        "status": "planned"
    },
    {
        "title": get_text("next_9_months"),
        "period": get_text("next_9_period"),
        "description": get_text("next_9_desc"),
        "color": "#1abc9c",
        "icon": "🌍",
        "status": "future"
    },
    {
        "title": get_text("year_2026"),
        "period": get_text("year_2026_period"),
        "description": get_text("year_2026_desc"),
        "color": "#ecf0f1",
        "icon": "♻️",
        "status": "vision"
    }
]

# Timeline vizualizatsiyasi
st.markdown(f"## 📅 {get_text('timeline_viz')}")

# Plotly timeline
fig = go.Figure()

# Timeline chizig'i
x_positions = [0, 1, 2, 3]
y_positions = [0, 0, 0, 0]

# Asosiy chiziq
fig.add_trace(go.Scatter(
    x=x_positions,
    y=y_positions,
    mode='lines',
    line=dict(color='#34495e', width=4),
    showlegend=False
))

# Nuqtalar va matnlar
colors = ['#3498db', '#95a5a6', '#1abc9c', '#ecf0f1']
for i, phase in enumerate(phases):
    # Nuqta
    fig.add_trace(go.Scatter(
        x=[i],
        y=[0],
        mode='markers',
        marker=dict(size=30, color=colors[i], line=dict(color='#2c3e50', width=3)),
        showlegend=False,
        hovertemplate=f"<b>{phase['title']}</b><br>{phase['description']}<extra></extra>"
    ))
    
    # Yuqoridagi matn
    fig.add_annotation(
        x=i,
        y=0.3,
        text=f"<b>{phase['icon']} {phase['title']}</b><br>{phase['period']}",
        showarrow=False,
        font=dict(size=14, color='#2c3e50'),
        align='center'
    )
    
    # Pastdagi matn
    fig.add_annotation(
        x=i,
        y=-0.3,
        text=phase['description'],
        showarrow=False,
        font=dict(size=11, color='#555'),
        align='center'
    )

fig.update_layout(
    height=400,
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 3.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, 0.5]
    ),
    margin=dict(l=50, r=50, t=50, b=50)
)

st.plotly_chart(fig, use_container_width=True)

# Fazalar bo'yicha batafsil ma'lumot
st.markdown(f"## 📋 {get_text('detailed_phase')}")

col1, col2 = st.columns(2)

with col1:
    # Phase 1
    st.markdown(f"""
    <div class="phase-card">
        <div style="border-left: 5px solid {phases[0]['color']}; padding-left: 20px;">
            <div class="phase-title">{phases[0]['icon']} {phases[0]['title']}</div>
            <div class="phase-description">
                <b>📅 {get_text('timeline')}:</b> {phases[0]['period']}<br>
                <b>📍 {get_text('location')}:</b> Tashkent city<br>
                <b>📦 {get_text('containers')}:</b> 10<br>
                <b>🎯 {get_text('goal')}:</b> {get_text('test_validate')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 3
    st.markdown(f"""
    <div class="phase-card">
        <div style="border-left: 5px solid {phases[2]['color']}; padding-left: 20px;">
            <div class="phase-title">{phases[2]['icon']} {phases[2]['title']}</div>
            <div class="phase-description">
                <b>📅 {get_text('timeline')}:</b> {phases[2]['period']}<br>
                <b>📍 {get_text('location')}:</b> All regions<br>
                <b>📦 {get_text('containers')}:</b> 1000<br>
                <b>🎯 {get_text('goal')}:</b> {get_text('national_deployment')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    # Phase 2
    st.markdown(f"""
    <div class="phase-card">
        <div style="border-left: 5px solid {phases[1]['color']}; padding-left: 20px;">
            <div class="phase-title">{phases[1]['icon']} {phases[1]['title']}</div>
            <div class="phase-description">
                <b>📅 {get_text('timeline')}:</b> {phases[1]['period']}<br>
                <b>📍 {get_text('location')}:</b> Tashkent region<br>
                <b>📦 {get_text('containers')}:</b> 100<br>
                <b>🎯 {get_text('goal')}:</b> {get_text('regional_expansion')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Phase 4
    st.markdown(f"""
    <div class="phase-card">
        <div style="border-left: 5px solid #95a5a6; padding-left: 20px;">
            <div class="phase-title">{phases[3]['icon']} {phases[3]['title']}</div>
            <div class="phase-description">
                <b>📅 {get_text('timeline')}:</b> {phases[3]['period']}<br>
                <b>📍 {get_text('location')}:</b> Nationwide<br>
                <b>📦 {get_text('containers')}:</b> All<br>
                <b>🎯 {get_text('goal')}:</b> {get_text('full_integration')}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Progress bar
st.markdown(f"## 📊 {get_text('overall_progress')}")
progress_col1, progress_col2, progress_col3 = st.columns(3)

with progress_col1:
    st.metric(get_text("current_phase"), get_text("test_mode"), "✅ Active")
with progress_col2:
    st.metric(get_text("total_duration"), f"24+ {get_text('months')}", "2024-2026")
with progress_col3:
    st.metric(get_text("target_containers"), "1000+", "By 2026")

# Milestones
st.markdown(f"## 🎯 {get_text('key_milestones')}")

milestones = [
    {"date": "Q1 2024", "event": get_text("launch_test"), "status": "completed"},
    {"date": "Q4 2024", "event": get_text("expand_region"), "status": "in-progress"},
    {"date": "Q3 2025", "event": get_text("deploy_all"), "status": "upcoming"},
    {"date": "2026", "event": get_text("full_toza"), "status": "upcoming"},
]

for milestone in milestones:
    status_color = {
        "completed": "🟢",
        "in-progress": "🟡",
        "upcoming": "⚪"
    }
    st.markdown(f"{status_color[milestone['status']]} **{milestone['date']}** - {milestone['event']}")


# ========== TEXNOLOGIYA BO'LIMI ==========
st.markdown("---")

# CSS Stillar
st.markdown("""
<style>
    .tech-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 40px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    }}
    .tech-card {
        background: white;
        border-radius: 15px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border-left: 5px solid #667eea;
    }
    .tech-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .section-title {
        color: white;
        font-size: 36px;
        font-weight: bold;
        margin: 30px 0 20px 0;
        padding: 15px;
        background: rgba(255,255,255,0.1);
        border-radius: 10px;
        border-left: 5px solid #00ff88;
    }
    .feature-box {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #00ff88;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    .ai-feature {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown(f"""
<div class="tech-header">
    <h1 style="font-size: 48px; margin: 0;">🤖 {get_text('tech_approach')}</h1>
    <p style="font-size: 20px; margin-top: 15px;">{get_text('tech_subtitle')}</p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    f"🛠️ {get_text('tech_stack')}", 
    f"🤖 {get_text('ai_tech')}", 
    f"📊 {get_text('architecture')}", 
    f"💡 {get_text('innovation')}"
])

with tab1:
    st.markdown(f'<div class="section-title">🛠️ {get_text("tools_tech")}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"### 💻 {get_text('backend_tech')}")
        backend_tech = [
            {"name": "Python 3.11+", "icon": "🐍", "purpose": "Main programming language"},
            {"name": "FastAPI", "icon": "⚡", "purpose": "REST API creation"},
            {"name": "PostgreSQL", "icon": "🗄️", "purpose": "Database"},
            {"name": "Redis", "icon": "🔴", "purpose": "Caching & real-time data"},
            {"name": "SQLAlchemy", "icon": "🔗", "purpose": "ORM framework"},
            {"name": "Celery", "icon": "⏰", "purpose": "Background tasks"},
        ]
        
        for tech in backend_tech:
            st.markdown(f"""
            <div class="feature-box">
                <h4>{tech['icon']} {tech['name']}</h4>
                <p style="color: #666; margin: 5px 0;">{tech['purpose']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### 📱 {get_text('frontend_tech')}")
        frontend_tech = [
            {"name": "Streamlit", "icon": "🎈", "purpose": "Web dashboard"},
            {"name": "React.js", "icon": "⚛️", "purpose": "Mobile app UI"},
            {"name": "Folium", "icon": "🗺️", "purpose": "Interactive maps"},
            {"name": "Plotly", "icon": "📊", "purpose": "Data visualization"},
        ]
        
        for tech in frontend_tech:
            st.markdown(f"""
            <div class="feature-box">
                <h4>{tech['icon']} {tech['name']}</h4>
                <p style="color: #666; margin: 5px 0;">{tech['purpose']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"### 🤖 {get_text('ai_ml_tech')}")
        ai_tech = [
            {"name": "TensorFlow", "icon": "🧠", "purpose": "Deep learning models"},
            {"name": "PyTorch", "icon": "🔥", "purpose": "Computer vision"},
            {"name": "OpenCV", "icon": "👁️", "purpose": "Image processing"},
            {"name": "Scikit-learn", "icon": "📈", "purpose": "ML algorithms"},
            {"name": "YOLO v8", "icon": "🎯", "purpose": "Object detection"},
            {"name": "Pandas/NumPy", "icon": "🔢", "purpose": "Data processing"},
        ]
        
        for tech in ai_tech:
            st.markdown(f"""
            <div class="feature-box">
                <h4>{tech['icon']} {tech['name']}</h4>
                <p style="color: #666; margin: 5px 0;">{tech['purpose']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"### 🔧 {get_text('iot_hardware')}")
        iot_tech = [
            {"name": "Raspberry Pi", "icon": "🥧", "purpose": "Edge computing"},
            {"name": "Arduino", "icon": "🔌", "purpose": "Sensor control"},
            {"name": "LoRaWAN", "icon": "📡", "purpose": "Long-range communication"},
            {"name": "Load Sensors", "icon": "⚖️", "purpose": "Weight measurement"},
        ]
        
        for tech in iot_tech:
            st.markdown(f"""
            <div class="feature-box">
                <h4>{tech['icon']} {tech['name']}</h4>
                <p style="color: #666; margin: 5px 0;">{tech['purpose']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Tech Stack Chart
    st.markdown(f"### 📊 {get_text('tech_distribution')}")
    tech_distribution = pd.DataFrame({
        'Category': ['Backend', 'Frontend', 'AI/ML', 'IoT', 'Database', 'DevOps'],
        'Percentage': [25, 20, 30, 15, 5, 5]
    })
    
    fig_tech = px.pie(tech_distribution, values='Percentage', names='Category', 
                 hole=0.4, color_discrete_sequence=px.colors.sequential.RdBu)
    fig_tech.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=14)
    )
    st.plotly_chart(fig_tech, use_container_width=True)

with tab2:
    st.markdown(f'<div class="section-title">🤖 {get_text("ai_usage")}</div>', unsafe_allow_html=True)
    
    st.markdown(f"### 🎯 {get_text('main_ai_components')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="ai-feature">
            <h3>🔍 1. {get_text('computer_vision')}</h3>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p><b>{get_text('technology')}:</b> YOLO v8, OpenCV, TensorFlow</p>
            <p><b>{get_text('purpose')}:</b> Container fill level detection and waste type classification</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ai-feature">
            <h3>🧮 3. {get_text('predictive_analytics')}</h3>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p><b>{get_text('technology')}:</b> LSTM, Prophet, Scikit-learn</p>
            <p><b>{get_text('purpose')}:</b> Predict when containers will be full and optimal collection times</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="ai-feature">
            <h3>🗺️ 2. {get_text('route_optimization')}</h3>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p><b>{get_text('technology')}:</b> Genetic Algorithms, Reinforcement Learning</p>
            <p><b>{get_text('purpose')}:</b> Find shortest route for waste collection vehicles</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="ai-feature">
            <h3>📊 4. {get_text('anomaly_detection')}</h3>
            <hr style="border-color: rgba(255,255,255,0.3);">
            <p><b>{get_text('technology')}:</b> Isolation Forest, Autoencoder</p>
            <p><b>{get_text('purpose')}:</b> Detect faulty sensors and unusual situations</p>
        </div>
        """, unsafe_allow_html=True)
    
    # AI Model Performance
    st.markdown(f"### 📈 {get_text('ai_performance')}")
    
    metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
    
    with metrics_col1:
        st.metric(get_text("cv_accuracy"), "94.5%", "+2.3%")
    with metrics_col2:
        st.metric(get_text("route_opt"), f"38% {get_text('savings')}", "+8%")
    with metrics_col3:
        st.metric(get_text("prediction_accuracy"), "91.2%", "+5.1%")
    with metrics_col4:
        st.metric(get_text("anomaly_detection"), "96.8%", "+1.2%")

with tab3:
    st.markdown(f'<div class="section-title">📊 {get_text("system_arch")}</div>', unsafe_allow_html=True)
    
    st.markdown(f"### 🏗️ {get_text('system_arch')}")
    
    # Architecture diagram using Plotly
    fig_arch = go.Figure()
    
    # Layers
    layers = [
        {"name": get_text("iot_layer"), "y": 4, "color": "#FF6B6B"},
        {"name": get_text("edge_computing"), "y": 3, "color": "#4ECDC4"},
        {"name": get_text("ai_processing"), "y": 2, "color": "#45B7D1"},
        {"name": get_text("app_layer"), "y": 1, "color": "#96CEB4"},
        {"name": get_text("user_interface"), "y": 0, "color": "#FFEAA7"}
    ]
    
    for layer in layers:
        fig_arch.add_trace(go.Bar(
            x=[layer["name"]],
            y=[1],
            base=layer["y"],
            marker=dict(color=layer["color"]),
            name=layer["name"],
            text=layer["name"],
            textposition='inside',
            textfont=dict(size=16, color='white'),
            hoverinfo='name'
        ))
    
    fig_arch.update_layout(
        title=get_text("layered_arch"),
        showlegend=False,
        height=500,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False, range=[0, 5]),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white')
    )
    
    st.plotly_chart(fig_arch, use_container_width=True)

with tab4:
    st.markdown(f'<div class="section-title">💡 {get_text("innovation_features")}</div>', unsafe_allow_html=True)
    
    st.markdown(f"### 🌟 {get_text('our_innovation')}")
    
    innovations = [
        {
            "title": f"🎯 {get_text('smart_fill')}",
            "description": get_text('smart_fill_desc'),
            "impact": f"40% {get_text('efficiency_increase')}"
        },
        {
            "title": f"🧠 {get_text('ai_route')}",
            "description": get_text('ai_route_desc'),
            "impact": f"35% {get_text('fuel_saving')}"
        },
        {
            "title": f"📊 {get_text('predictive_maint')}",
            "description": get_text('predictive_desc'),
            "impact": f"50% {get_text('repair_reduction')}"
        },
        {
            "title": f"♻️ {get_text('waste_class')}",
            "description": get_text('waste_desc'),
            "impact": f"60% {get_text('recycling_efficiency')}"
        },
        {
            "title": f"🌍 {get_text('env_tracking')}",
            "description": get_text('env_desc'),
            "impact": get_text('city_ecology')
        },
        {
            "title": f"📱 {get_text('mobile_first')}",
            "description": get_text('mobile_desc'),
            "impact": f"80% {get_text('user_satisfaction')}"
        }
    ]
    
    col1, col2 = st.columns(2)
    
    for idx, innovation in enumerate(innovations):
        col = col1 if idx % 2 == 0 else col2
        with col:
            st.markdown(f"""
            <div class="tech-card">
                <h3 style="color: #000;">{innovation['title']}</h3>
                <p style="color: #000; line-height: 1.6;">{innovation['description']}</p>
                <div style="background: #667eea; color: white; padding: 10px; border-radius: 8px; margin-top: 10px;">
                    <b>{get_text('impact')}:</b> {innovation['impact']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Competitive Advantages
    st.markdown(f"### 🏆 {get_text('competitive_adv')}")
    
    advantages = [
        f"✅ {get_text('adv1')}",
        f"✅ {get_text('adv2')}",
        f"✅ {get_text('adv3')}",
        f"✅ {get_text('adv4')}",
        f"✅ {get_text('adv5')}",
        f"✅ {get_text('adv6')}",
        f"✅ {get_text('adv7')}",
        f"✅ {get_text('adv8')}"
    ]
    
    cols = st.columns(2)
    for idx, adv in enumerate(advantages):
        with cols[idx % 2]:
            st.markdown(f"""
            <div style="background: white; padding: 15px; margin: 8px 0; border-radius: 10px; border-left: 4px solid #00ff88;">
                <p style="margin: 0; color: #2c3e50; font-size: 16px;">{adv}</p>
            </div>
            """, unsafe_allow_html=True)
