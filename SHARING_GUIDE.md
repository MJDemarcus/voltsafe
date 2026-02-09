# How to Share VoltSafe

There are three ways to share this app with others:

## Option 1: Share on Local Wi-Fi (Simplest)
If your colleague is in the same office and on the same Wi-Fi network:
1. Run the app on your computer.
2. Give them this Network URL: `http://192.168.1.60:8503`
   *(Note: This URL might change if your IP address changes).*

## Option 2: Send the Code (For Developers)
If you want to send the app to someone who has Python installed:
1. Zip the entire `voltsafe_project` folder.
2. Send them the zip file.
3. They must install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. They run `python3 -m streamlit run app.py`.

## Option 3: Deploy to the Web (Professional)
To make the app accessible to anyone via a public link:
https://voltsafe-systems.streamlit.app

1. The app is hosted on your GitHub repository `MJDemarcus/voltsafe`.
2. Any changes you push to GitHub will automatically update the live app.

