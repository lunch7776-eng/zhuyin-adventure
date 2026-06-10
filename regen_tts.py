#!/usr/bin/env python3
"""
重新生成遊戲用的預錄 TTS 音檔（女聲 HsiaoYu / 男聲 YunJhe）。

需求：
    pip install --user edge-tts

使用：
    python3 regen_tts.py

加新句子：直接把字串塞進下面 PHRASES，再跑一次就好。
換 voice：改 VOICES 字典；可用 voice 清單 `edge-tts --list-voices | grep zh-TW`。

目前可選的台灣口音 Azure Neural voice：
    zh-TW-HsiaoChenNeural  曉臻（女，標準成熟）
    zh-TW-HsiaoYuNeural    曉雨（女，年輕活潑）← 預設女聲
    zh-TW-YunJheNeural     雲哲（男，年輕）   ← 預設男聲
"""
import asyncio, os, sys

try:
    import edge_tts
except ImportError:
    sys.exit("缺套件 — 先跑：python3 -m pip install --user edge-tts")

PHRASES = [
    # 聲符例字（21 個）
    "爸","皮","媽","飛","弟","兔","牛","鹿","哥","苦","猴",
    "雞","汽","西","豬","車","蛇","日","字","醋","絲",
    # 韻符例字（16 個）
    "啊","喔","鵝","也","愛","黑","高","樓","安","恩","王","鷹","兒","衣","屋","魚",
    # 結合韻例字（21 個 — 結合韻有些跟韻符共用例字，僅列新增）
    "鴨","喲","葉","腰","油","鹽","音","羊","蛙","我","歪","為","彎","文","翁",
    "月","圓","雲","用",
    # 例詞（Lv3 拼字小工匠）
    "西瓜","月亮","蘋果","雨傘","魚兒","花朵","牛奶","蛋糕",
    # 遊戲反饋短句
    "好棒","答對了","再聽一次","太厲害了","過關了",
    # 設定面板試聽
    "注音真好玩","爸爸",
    # v2 冒險地圖版 — 引導語
    "你好","我是BOBO","我們一起去冒險吧","出發囉",
    "聽聽看","找找看","我想吃","好好吃","謝謝你",
    "換你念念看","沒關係","再試一次",
    "你學會了","拿到新貼紙","挑戰成功","複習時間",
    "翻翻看","找出一樣的好朋友","跟著淡淡的字描描看",
]

VOICES = {
    "female": "zh-TW-HsiaoYuNeural",
    "male":   "zh-TW-YunJheNeural",
}

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "audio", "tts")
RATE = "-15%"  # 慢一點點給小孩聽

async def gen():
    for gender, voice in VOICES.items():
        d = os.path.join(OUT, gender)
        os.makedirs(d, exist_ok=True)
        for p in PHRASES:
            path = os.path.join(d, f"{p}.mp3")
            await edge_tts.Communicate(p, voice, rate=RATE).save(path)
        print(f"  {gender:7s} {voice:30s} {len(PHRASES)} 個")

if __name__ == "__main__":
    print(f"輸出到：{OUT}")
    asyncio.run(gen())
    print(f"完成 — 共 {len(PHRASES)*2} 個 mp3")
