import os
import subprocess


timestamps = """
(00:00:00) Lesson 0: Welcome To Blockchain
(00:09:05) Lesson 1: Blockchain Basics
(02:01:16) Lesson 2: Welcome to Remix! Simple Storage
(03:05:34) Lesson 3: Remix Storage Factory
(03:31:55) Lesson 4: Remix Fund Me
(05:30:42) Lesson 5: Ethers.js Simple Storage
(08:20:17) Lesson 6: Hardhat Simple Storage
(10:00:48) Lesson 7: Hardhat Fund Me
(12:32:57) Lesson 8: HTML / Javascript Fund Me (Full Stack / Front End)
(13:41:02) Lesson 9: Hardhat Smart Contract Lottery
(16:34:07) Lesson 10: NextJS Smart Contract Lottery (Full Stack / Front End)
(18:51:36) Lesson 11: Hardhat Starter Kit
(18:59:24) Lesson 12: Hardhat ERC20s
(19:16:13) Lesson 13: Hardhat DeFi & Aave
(20:28:51) Lesson 14: Hardhat NFTs 
(23:37:03) Lesson 15: NextJS NFT Marketplace (Full Stack / Front End)
(28:53:11) Lesson 16: Hardhat Upgrades
(29:45:24) Lesson 17: Hardhat DAOs
(31:28:32) Lesson 18: Security & Auditing 
 """

long_video = "D:\@Videos\-2024 March\Mia Khalifa Threesome BBC - EPORNER.mp4"
long_video_name = long_video.split(os.sep)[-1]
sections = timestamps.splitlines()

cmds = [f"mkdir -p \"{long_video_name}\"",
        f"cd \"{long_video_name}\"",
        f"pwd",
        f"ffmpeg -ss 00:00:00 -i \"{long_video}\" -t 180 -c copy \"{long_video_name}\{long_video_name}_out.mp4\""]
print(f"\n\n{cmds}")
for cmd in cmds:
    completed = subprocess.run(cmd, shell=True, capture_output=True)
    print("\n\nreturns", completed.returncode)
    print("\n\nstdout", completed.stdout)
    print("\n\nstderr", completed.stderr)
