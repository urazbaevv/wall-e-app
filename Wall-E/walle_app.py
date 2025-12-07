# import streamlit as st
# import folium
# import random
# import pandas as pd
# from datetime import datetime
# from streamlit_folium import folium_static
# import base64
# # Streamlit sahifa konfiguratsiyasi
# st.set_page_config(page_title="Smart Waste Monitoring", layout="wide")
# def set_background(image_file):
#     page_bg_img = f"""
#     <style>
#     .stApp {{
#         background: url(data:image/png;base64,{image_file}) no-repeat center center fixed;
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# # Rasmni base64 formatga o'tkazish
# def get_base64_of_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Background.png faylini yuklash
# image_base64 = get_base64_of_image("background.png")
# set_background(image_base64)

# # **Konteynerlar ma'lumotlari**
# def get_containers():
#     if "containers" not in st.session_state:
#         st.session_state.containers = [
#             {"id": i, "name": f"Container #{i}", "lat": 41.3 + i * 0.02, "lon": 69.24 + i * 0.02, 
#              "weight": random.randint(20, 90) if i not in [3, 7] else 100, 
#              "max_weight": 100} for i in range(1, 6)
#         ]
#     return st.session_state.containers

# # **Vazn sensor sinfi**
# class WeightSensor:
#     def __init__(self, container_id, max_weight, initial_weight):
#         self.container_id = container_id
#         self.max_weight = max_weight
#         self.current_weight = initial_weight

#     def get_weight(self):
#         return self.current_weight

#     def get_fill_percentage(self):
#         return (self.current_weight / self.max_weight) * 100

# # **Tablar**
# tab1, tab2, tab3 = st.tabs(["📍 Container Map", "⚖️ Weight Sensors", "➕ Add Container"])

# # **Konteynerlar ro‘yxati**
# containers = get_containers()

# # **Xarita yaratish**
# with tab1:
#     st.markdown("<h1 style='text-align: center;'>♻️ Smart Waste Container Map</h1>", unsafe_allow_html=True)

#     map_center = [41.305, 69.25]
#     m = folium.Map(location=map_center, zoom_start=12)

#     for container in containers:
#         color = "red" if container["weight"] >= container["max_weight"] else "green"
#         folium.Marker(
#             [container["lat"], container["lon"]],
#             popup=f"{container['name']} ({container['weight']} kg / {container['max_weight']} kg)",
#             icon=folium.Icon(color=color),
#         ).add_to(m)

#     folium_static(m)

# # **Sensor ma'lumotlari**
# with tab2:
#     st.markdown("<h1 style='text-align: center;'>⚖️ Real-time Weight Sensors</h1>", unsafe_allow_html=True)
    
#     sensor_data = []
#     for container in containers:
#         sensor = WeightSensor(container["id"], container["max_weight"], container["weight"])
#         current_weight = sensor.get_weight()
#         fill_percentage = sensor.get_fill_percentage()

#         sensor_data.append({
#             "Container": container["name"],
#             "Weight": f"{current_weight:.2f} kg",
#             "Capacity": f"{container['max_weight']} kg",
#             "Fill Level": f"{fill_percentage:.1f}%",
#             "Status": "Connected"
#         })

#     sensor_df = pd.DataFrame(sensor_data)
#     st.dataframe(sensor_df, use_container_width=True)

# # **Yangi konteyner qo'shish**
# with tab3:
#     st.markdown("<h1 style='text-align: center;'>➕ Add New Container</h1>", unsafe_allow_html=True)
#     container_name = st.text_input("Container Name:")
#     container_lat = st.number_input("Latitude:", min_value=-90.0, max_value=90.0, value=41.3)
#     container_lon = st.number_input("Longitude:", min_value=-180.0, max_value=180.0, value=69.24)
#     container_weight = st.number_input("Initial Weight (kg):", min_value=0, max_value=200, value=50)
#     container_max_weight = st.number_input("Max Weight (kg):", min_value=50, max_value=500, value=100)

#     if st.button("Add Container"):
#         new_id = len(containers) + 1
#         new_container = {
#             "id": new_id,
#             "name": container_name if container_name else f"Container #{new_id}",
#             "lat": container_lat,
#             "lon": container_lon,
#             "weight": container_weight,
#             "max_weight": container_max_weight,
#         }
#         st.session_state.containers.append(new_container)
#         st.success(f"✅ {new_container['name']} successfully added!")
#         st.rerun()

# # **Sidebar ma'lumotlari**
# st.sidebar.write("Developed by group called ICEBERG ♻️")
# st.sidebar.markdown("---")
# st.sidebar.write("### System Status")
# st.sidebar.write(f"Total Containers: {len(containers)}")
# full_containers = sum(1 for c in containers if c["weight"] >= c["max_weight"])
# st.sidebar.write(f"Full Containers: {full_containers}")

# # **Oxirgi yangilanish vaqti**
# st.sidebar.markdown("---")
# st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")





# import streamlit as st
# import folium
# import random
# import pandas as pd
# from datetime import datetime
# from streamlit_folium import folium_static
# import base64
# import smtplib
# from email.mime.text import MIMEText

# def send_email(full_containers):
#     sender_email = "orazbaevqudaybergen0@gmail.com"
#     receiver_email = "iskandarovasilbek70@gmail.com"
#     app_password = "jwig ssky uiuy djli"  # Gmail App Password o'rniga haqiqiy parolni qo'ying

#     if not full_containers:
#         return None  # Agar hech qanday to'la konteyner bo'lmasa, email jo‘natilmaydi

#     subject = "🚨 Alert: Containers Are FULL!"
#     body = "🔔 **Full Containers Alert!**\n\n"

#     for container in full_containers:
#         name = container["name"]
#         weight = container["weight"]
#         max_weight = container["max_weight"]
#         height = container["height"]
#         max_height = container["max_height"]
#         lat = container["lat"]
#         lon = container["lon"]

#         google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
#         body += (
#             f"🔹 **{name}**\n"
#             f"⚖️ **Weight:** {weight}/{max_weight} kg\n"
#             f"📏 **Height:** {height}/{max_height} cm\n"
#             f"📍 **Location:** [Google Maps]({google_maps_link})\n\n"
#         )

#     body += "🚛 Please take necessary action immediately!"

#     msg = MIMEText(body, "plain")
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = receiver_email

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, app_password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         print(f"✅ Email sent to {receiver_email}")
#         return receiver_email
#     except Exception as e:
#         print(f"❌ Error sending email: {e}")
#         return None


# def set_background(image_file):
#     page_bg_img = f"""
#     <style>
#     .stApp {{
#         background: url(data:image/png;base64,{image_file}) no-repeat center center fixed;
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# def get_base64_of_image(image_path):
#     try:
#         with open(image_path, "rb") as image_file:
#             return base64.b64encode(image_file.read()).decode()
#     except FileNotFoundError:
#         print("❌ Background image not found!")
#         return ""

# image_base64 = get_base64_of_image("background.png")
# if image_base64:
#     set_background(image_base64)

# class ContainerSensor:
#     def __init__(self, container_id, max_weight, max_height):
#         self.container_id = container_id
#         self.max_weight = max_weight
#         self.max_height = max_height
#         self.current_weight = random.randint(20, 120)
#         self.current_height = random.randint(50, 160)
    
#     def is_full(self):
#         return self.current_weight >= self.max_weight or self.current_height >= self.max_height

# def get_containers():
#     containers = []
#     full_containers_info = []
#     for i in range(1, 11):
#         sensor = ContainerSensor(i, 100, 150)
#         container = {
#             "id": i,
#             "name": f"Container #{i}",
#             "lat": round(41.3 + i * 0.02, 6),
#             "lon": round(69.24 + i * 0.02, 6),
#             "weight": sensor.current_weight,
#             "height": sensor.current_height,
#             "max_weight": sensor.max_weight,
#             "max_height": sensor.max_height,
#             "is_full": sensor.is_full(),
#         }
        
#         if container["is_full"]:
#             full_containers_info.append(container)
        
#         containers.append(container)
    
#     # Faqat to'lib ketgan konteynerlar uchun email jo‘natish
#     email_sent_to = send_email(full_containers_info)
#     return containers, full_containers_info, email_sent_to

# containers, full_containers_info, email_sent_to = get_containers()

# tab1, tab2 = st.tabs(["📍 Container Map", "⚖️ Sensor Data"])

# with tab1:
#     st.markdown("<h1 style='text-align: center;'>♻️ Smart Waste Container Map</h1>", unsafe_allow_html=True)
#     m = folium.Map(location=[41.305, 69.25], zoom_start=12)
#     for container in containers:
#         color = "red" if container["is_full"] else "green"
#         folium.Marker(
#             [container["lat"], container["lon"]],
#             popup=f"{container['name']} ({container['weight']} kg, {container['height']} cm)",
#             icon=folium.Icon(color=color),
#         ).add_to(m)
#     folium_static(m)

#     if full_containers_info:
#         st.markdown("## 🚨 Full Containers & Notifications Sent")
#         for container in full_containers_info:
#             st.write(f"**{container['name']}** is FULL (Weight: {container['weight']} kg, Height: {container['height']} cm)")
#             st.write(f"📍 **Location:** {container['lat']}, {container['lon']}")
        
#         if email_sent_to:
#             st.write(f"📧 Notification sent to: {email_sent_to}")
#         else:
#             st.write("⚠️ Failed to send notification")

# with tab2:
#     st.markdown("<h1 style='text-align: center;'>⚖️ Real-time Sensor Data</h1>", unsafe_allow_html=True)
#     sensor_df = pd.DataFrame([
#         {
#             "Container": c["name"],
#             "Weight": f"{c['weight']} kg / {c['max_weight']} kg",
#             "Height": f"{c['height']} cm / {c['max_height']} cm",
#             "Location": f"{c['lat']}, {c['lon']}",
#             "Status": "FULL" if c["is_full"] else "OK"
#         }
#         for c in containers
#     ])
#     st.dataframe(sensor_df, use_container_width=True)

# st.sidebar.write("Developed by ICEBERG ♻️")
# st.sidebar.write(f"Total Containers: {len(containers)}")
# st.sidebar.write(f"Full Containers: {sum(1 for c in containers if c['is_full'])}")
# st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



# import streamlit as st 
# import folium
# import random
# import pandas as pd
# from datetime import datetime
# from streamlit_folium import folium_static
# import base64
# import smtplib
# from email.mime.text import MIMEText

#  def set_background(image_file):
#     page_bg_img = f"""
#     <style>
#     .stApp {{
#         background: url(data:image/png;base64,{image_file}) no-repeat center center fixed;
#         background-size: cover;
#     }}
#     </style>
#     """
#     st.markdown(page_bg_img, unsafe_allow_html=True)

# # Rasmni base64 formatga o'tkazish
# def get_base64_of_image(image_path):
#     with open(image_path, "rb") as image_file:
#         return base64.b64encode(image_file.read()).decode()

# # Background.png faylini yuklash
# image_base64 = get_base64_of_image("background.png")
# set_background(image_base64)

# def send_email(full_containers):
#     sender_email = "orazbaevqudaybergen0@gmail.com"
#     receiver_email = "iskandarovasilbek70@gmail.com"
#     app_password = "jwig ssky uiuy djli"

#     if not full_containers:
#         return None

#     subject = "🚨 Alert: Containers Are FULL!"
#     body = "🔔 **Full Containers Alert!**\n\n"

#     for container in full_containers:
#         name = container["name"]
#         weight = container["weight"]
#         max_weight = container["max_weight"]
#         height = container["height"]
#         max_height = container["max_height"]
#         lat = container["lat"]
#         lon = container["lon"]

#         google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
#         body += (
#             f"🔹 **{name}**\n"
#             f"⚖️ **Weight:** {weight}/{max_weight} kg\n"
#             f"👥 **Height:** {height}/{max_height} cm\n"
#             f"📍 **Location:** [Google Maps]({google_maps_link})\n\n"
#         )

#     body += "🚛 Please take necessary action immediately!"

#     msg = MIMEText(body, "plain")
#     msg["Subject"] = subject
#     msg["From"] = sender_email
#     msg["To"] = receiver_email

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(sender_email, app_password)
#             server.sendmail(sender_email, receiver_email, msg.as_string())
#         return receiver_email
#     except Exception as e:
#         return None

# class ContainerSensor:
#     def __init__(self, container_id, max_weight, max_height):
#         self.container_id = container_id
#         self.max_weight = max_weight
#         self.max_height = max_height
#         self.current_weight = random.randint(20, 120)
#         self.current_height = random.randint(50, 160)
    
#     def is_full(self):
#         return self.current_weight >= self.max_weight or self.current_height >= self.max_height

# def get_containers():
#     locations = [
#         (41.311081, 69.240562, "Tashkent"),
#         (39.654503, 66.975884, "Samarkand"),
#         (40.103922, 65.371875, "Navoi"),
#         (40.524529, 72.798537, "Andijan"),
#         (40.38942, 71.78432, "Namangan"),
#         (39.776667, 64.425, "Bukhara"),
#         (41.550277, 60.631944, "Nukus"),
#         (39.712, 67.003, "Jizzakh"),
#         (38.838611, 65.784722, "Kashkadarya")
#     ]

#     containers = []
#     full_containers_info = []
#     for i, (lat, lon, region) in enumerate(locations, start=1):
#         sensor = ContainerSensor(i, 100, 150)
#         container = {
#             "id": i,
#             "name": f"Container #{i} ({region})",
#             "lat": lat,
#             "lon": lon,
#             "weight": sensor.current_weight,
#             "height": sensor.current_height,
#             "max_weight": sensor.max_weight,
#             "max_height": sensor.max_height,
#             "is_full": sensor.is_full(),
#         }
        
#         if container["is_full"]:
#             full_containers_info.append(container)
        
#         containers.append(container)
    
#     email_sent_to = send_email(full_containers_info)
#     return containers, full_containers_info, email_sent_to

# containers, full_containers_info, email_sent_to = get_containers()

# tab1, tab2 = st.tabs(["📍 Container Map", "⚖️ Sensor Data"])

# with tab1:
#     st.markdown("<h1 style='text-align: center;'>♻️ Smart Waste Container Map</h1>", unsafe_allow_html=True)
#     m = folium.Map(location=[41.0, 64.0], zoom_start=6)
#     for container in containers:
#         color = "red" if container["is_full"] else "green"
#         folium.Marker(
#             [container["lat"], container["lon"]],
#             popup=f"{container['name']} ({container['weight']} kg, {container['height']} cm)",
#             icon=folium.Icon(color=color),
#         ).add_to(m)
#     folium_static(m)

#     if full_containers_info:
#         st.markdown("## 🚨 Full Containers & Notifications Sent")
#         for container in full_containers_info:
#             st.write(f"**{container['name']}** is FULL (Weight: {container['weight']} kg, Height: {container['height']} cm)")
#             st.write(f"📍 **Location:** {container['lat']}, {container['lon']}")
        
#         if email_sent_to:
#             st.write(f"📧 Notification sent to: {email_sent_to}")
#         else:
#             st.write("⚠️ Failed to send notification")

# # with tab2:
# #     st.markdown("<h1 style='text-align: center;'>⚖️ Real-time Sensor Data</h1>", unsafe_allow_html=True)
# #     sensor_df = pd.DataFrame([
# #         {
# #             "Container": c["name"],
# #             "Weight": f"{c['weight']} kg / {c['max_weight']} kg",
# #             "Height": f"{c['height']} cm / {c['max_height']} cm",
# #             "Location": f"{c['lat']}, {c['lon']}",
# #             "Status": "FULL" if c["is_full"] else "OK"
# #         }
# #         for c in containers
# #     ])
# #     st.dataframe(sensor_df, use_container_width=True)
# with tab2:
#     st.markdown("<h1 style='text-align: center;'>⚖️ Real-time Sensor Data</h1>", unsafe_allow_html=True)
#     sensor_df = pd.DataFrame([
#         {
#             "№": i + 1,  # Indeksni 1 dan boshlash
#             "Container": c["name"],
#             "Weight": f"{c['weight']} kg / {c['max_weight']} kg",
#             "Height": f"{c['height']} cm / {c['max_height']} cm",
#             "Location": f"{c['lat']}, {c['lon']}",
#             "Status": "FULL" if c["is_full"] else "OK"
#         }
#         for i, c in enumerate(containers)  # enumerate() yordamida indeksni qo'shish
#     ])
    
#     # Pandas DF indekslarini o'chirib chiqarish
#     sensor_df.set_index("№", inplace=True)

#     st.dataframe(sensor_df, use_container_width=True)




# st.sidebar.write("Developed by ICEBERG ♻️")
# st.sidebar.write(f"Total Containers: {len(containers)}")
# st.sidebar.write(f"Full Containers: {sum(1 for c in containers if c['is_full'])}")
# st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")



import streamlit as st 
import folium
import random
import pandas as pd
from datetime import datetime
from streamlit_folium import folium_static
import base64
import smtplib
import os
from email.mime.text import MIMEText


st.markdown("<h1 style='text-align: center; font-size: 50px; font-weight: bold;'>WALL-E APP</h1>", unsafe_allow_html=True)


# Rasmni base64 formatga o'tkazish
def get_base64_of_image(image_path):
    if os.path.exists(image_path):  # Fayl mavjudligini tekshiramiz
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    return None

# Background rasmini qo'shish
def set_background(image_file):
    if image_file:
        page_bg_img = f"""
        <style>
        .stApp {{
            background: url(data:image/png;base64,{image_file}) no-repeat center center fixed;
            background-size: cover;
        }}
        </style>
        """
        st.markdown(page_bg_img, unsafe_allow_html=True)

# Background.png faylini yuklash
image_base64 = get_base64_of_image("background.png")
set_background(image_base64)

def send_email(full_containers):
    sender_email = "orazbaevqudaybergen0@gmail.com"
    receiver_email = "jasurbekmaxamatjonov0603@gmail.com"
    app_password = "jwig ssky uiuy djli"

    if not full_containers:
        return None

    subject = "🚨 Alert: Containers Are FULL!"
    body = "🔔 **Full Containers Alert!**\n\n"

    for container in full_containers:
        name = container["name"]
        weight = container["weight"]
        max_weight = container["max_weight"]
        height = container["height"]
        max_height = container["max_height"]
        lat = container["lat"]
        lon = container["lon"]

        google_maps_link = f"https://www.google.com/maps?q={lat},{lon}"
        body += (
            f"🔹 **{name}**\n"
            f"⚖️ **Weight:** {weight}/{max_weight} kg\n"
            f"👥 **Height:** {height}/{max_height} cm\n"
            f"📍 **Location:** [Google Maps]({google_maps_link})\n\n"
        )

    body += "🚛 Please take necessary action immediately!"

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        return receiver_email
    except Exception:
        return None

class ContainerSensor:
    def __init__(self, container_id, max_weight, max_height):
        self.container_id = container_id
        self.max_weight = max_weight
        self.max_height = max_height
        self.current_weight = random.randint(20, 120)
        self.current_height = random.randint(50, 160)
    
    def is_full(self):
        return self.current_weight >= self.max_weight or self.current_height >= self.max_height

def get_containers():
    locations = [
        (41.311081, 69.240562, "Tashkent"),
        (39.654503, 66.975884, "Samarkand"),
        (40.103922, 65.371875, "Navoi"),
        (40.524529, 72.798537, "Andijan"),
        (40.38942, 71.78432, "Namangan"),
        (39.776667, 64.425, "Bukhara"),
        (41.550277, 60.631944, "Nukus"),
        (39.712, 67.003, "Jizzakh"),
        (38.838611, 65.784722, "Kashkadarya")
    ]

    containers = []
    full_containers_info = []
    for i, (lat, lon, region) in enumerate(locations, start=1):
        sensor = ContainerSensor(i, 100, 150)
        container = {
            "id": i,
            "name": f"Container #{i} ({region})",
            "lat": lat,
            "lon": lon,
            "weight": sensor.current_weight,
            "height": sensor.current_height,
            "max_weight": sensor.max_weight,
            "max_height": sensor.max_height,
            "is_full": sensor.is_full(),
        }
        
        if container["is_full"]:
            full_containers_info.append(container)
        
        containers.append(container)
    
    email_sent_to = send_email(full_containers_info)
    return containers, full_containers_info, email_sent_to

containers, full_containers_info, email_sent_to = get_containers()

tab1, tab2 = st.tabs(["📍 Container Map", "⚖️ Sensor Data"])

with tab1:
    st.markdown("<h1 style='text-align: center;'>♻️ Smart Waste Container Map</h1>", unsafe_allow_html=True)
    m = folium.Map(location=[41.0, 64.0], zoom_start=6)
    for container in containers:
        color = "red" if container["is_full"] else "green"
        folium.Marker(
            [container["lat"], container["lon"]],
            popup=f"{container['name']} ({container['weight']} kg, {container['height']} cm)",
            icon=folium.Icon(color=color),
        ).add_to(m)
    folium_static(m)

    if full_containers_info:
        st.markdown("## 🚨 Full Containers & Notifications Sent")
        for container in full_containers_info:
            st.write(f"**{container['name']}** is FULL (Weight: {container['weight']} kg, Height: {container['height']} cm)")
            st.write(f"📍 **Location:** {container['lat']}, {container['lon']}")

        if email_sent_to:
            st.write(f"📧 Notification sent to: {email_sent_to}")
        else:
            st.write("⚠️ Failed to send notification")

with tab2:
    st.markdown("<h1 style='text-align: center;'>⚖️ Real-time Sensor Data</h1>", unsafe_allow_html=True)
    sensor_df = pd.DataFrame([
        {
            "№": i + 1,  # Indeksni 1 dan boshlash
            "Container": c["name"],
            "Weight": f"{c['weight']} kg / {c['max_weight']} kg",
            "Height": f"{c['height']} cm / {c['max_height']} cm",
            "Location": f"{c['lat']}, {c['lon']}",
            "Status": "FULL" if c["is_full"] else "OK"
        }
        for i, c in enumerate(containers)  # enumerate() yordamida indeksni qo'shish
    ])
    
    # Pandas DF indekslarini o'chirib chiqarish
    sensor_df.set_index("№", inplace=True)

    st.dataframe(sensor_df, use_container_width=True)

st.sidebar.write("Developed by ICEBERG ♻️")
st.sidebar.write(f"Total Containers: {len(containers)}")
st.sidebar.write(f"Full Containers: {sum(1 for c in containers if c['is_full'])}")
st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

