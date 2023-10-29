<h3><b> Hesap Makinesi </b></h3>

Telegram için [Pyrogram](https://github.com/pyrogram) ile yazılmış basit bir hesap makinesi botu.

<h3><b> VPS/Yerel Dağıtım Yöntemi </b></h3>

- Yükseltme ve Güncelleme:
`sudo apt-get update && sudo apt-get upgrade -y`
- Gerekli paketleri şu şekilde yükleyin:
`sudo apt-get install python3-pip -y`
- Pip'i şu şekilde yükleyin:
`sudo pip3 install -U pip`
- Depoyu şu şekilde klonlayın :
`git clone https://github.com/suphiozturk8/HesapMakinesi && cd HesapMakinesi`
- Setuptools'u şu şekilde yükleyin/yükseltin:
`pip3 install --upgrade pip setuptools`
- Gereksinimleri şu şekilde yükleyin :
`pip3 install -U -r requirements.txt`
- Terminali kapattığınızda botunuzu çalıştırmaya devam etmek için tmux'u kurun:
`sudo apt install tmux && tmux`
- Son olarak botu şu şekilde çalıştırın:
`python3 hesap.py`
- Tmux oturumundan çıkmak için:
`Ctrl+b` ve ardından `d` tuşlarına basın