## install telegram bot

1. Open your telegram account and in the search bar type “BotFather”.
2. Click on the “BotFather” and Click on the “Start” button.
3. Type “/newbot”.
4. Type your unique bot name.
5. Now type a unique username for your bot.
    After that you can see the token to access the HTTP API.
    Keep your token secure and store it safely.
    You can replace this token in env file.
6. Run the python code.
7. NGROK setup
    1) Install Choco
        - Click Start and type “powershell“
        - Right-click Windows Powershell and choose “Run as Administrator“
        - Paste the following command into Powershell and press enter.
                Set-ExecutionPolicy Bypass -Scope Process -Force; `
                iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
        - Answer Yes when prompted
    2) install NGROK
        - Close and reopen an elevated PowerShell window to start using choco
        - choco install ngrok
        - ngrok http 5000
8. Setup webhook.
    You can do it by running the link in your browser.
    https://api.telegram.org/bot5773306905:AAFmcc0xlg5B6Sut6lAM39LF6J5uhYZhA5U/setWebhook?url=https://03d9-216-73-160-240.ngrok.io
    
    If you see the result is {"ok":true,"result":true,"description":"Webhook was set"}, then everything is okay.
