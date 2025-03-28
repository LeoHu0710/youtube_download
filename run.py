import yt_dlp
import sys

def download_video(url, format_id):
    ydl_opts = {
        'format': format_id,
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([url])
            print("\n下載完成！")
        except Exception as e:
            print(f"\n下載失敗: {str(e)}")

def get_format_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            formats = info['formats']
            
            # 分類存儲不同類型的格式
            video_only = []  # 只有視頻
            audio_only = []  # 只有音頻
            video_audio = [] # 視頻和音頻都有
            
            # 記錄最佳質量
            best_video = {'quality': 0, 'format_id': None}
            best_audio = {'bitrate': 0, 'format_id': None}
            
            for f in formats:
                format_id = f.get('format_id', 'N/A')
                ext = f.get('ext', 'N/A')
                vcodec = f.get('vcodec', 'none')
                acodec = f.get('acodec', 'none')
                
                # 準備格式信息
                if vcodec != 'none':
                    vcodec_info = f"視頻編碼: {vcodec}"
                    vquality = f.get('height', 'N/A')
                    if vquality != 'N/A':
                        vquality = f"{vquality}p"
                        # 更新最佳視頻質量
                        if isinstance(vquality, str) and vquality.endswith('p'):
                            quality = int(vquality[:-1])
                            if quality > best_video['quality']:
                                best_video['quality'] = quality
                                best_video['format_id'] = format_id
                else:
                    vcodec_info = "無視頻"
                    vquality = "None"
                
                if acodec != 'none':
                    acodec_info = f"音頻編碼: {acodec}"
                    abr = f.get('abr', 0)
                    if abr:
                        audio_quality = f"{abr:.3f}kbps"
                        # 更新最佳音頻質量
                        if abr > best_audio['bitrate']:
                            best_audio['bitrate'] = abr
                            best_audio['format_id'] = format_id
                    else:
                        audio_quality = "N/A"
                else:
                    acodec_info = "無音頻"
                    audio_quality = "0"
                
                # 格式信息字符串
                format_info = (
                    f"格式代碼: {format_id}, 格式: {ext}, "
                    f"影片質量: {vquality}, 語音質量: {audio_quality}\n"
                    f"編碼信息: {vcodec_info}, {acodec_info}\n"
                )
                
                # 根據編碼類型分類
                if vcodec != 'none' and acodec != 'none':
                    video_audio.append(format_info)
                elif vcodec != 'none' and acodec == 'none':
                    video_only.append(format_info)
                elif vcodec == 'none' and acodec != 'none':
                    audio_only.append(format_info)
            
            # 輸出分類結果
            print("\n=== 純視頻格式（無聲音）===")
            print("這些格式只包含視頻流，沒有音頻：")
            for info in video_only:
                print(info)
            
            print("\n=== 純音頻格式 ===")
            print("這些格式只包含音頻流，沒有視頻：")
            for info in audio_only:
                print(info)
            
            print("\n=== 完整格式（視頻+音頻）===")
            print("這些格式同時包含視頻和音頻：")
            for info in video_audio:
                print(info)
            
            print("\n>>> 下載說明 <<<")
            print("1. 下載完整格式：")
            print("   - 直接輸入格式代碼，如：18")
            
            print("\n2. 自由組合視頻和音頻：")
            print("   - 從上方選擇任意一個「純視頻格式」和任意一個「純音頻格式」")
            print("   - 使用加號連接它們的格式代碼，如：137+251")
            print("   - 程式會自動下載並合併視頻和音頻")
            
            # 顯示最佳質量建議
            if best_video['format_id'] and best_audio['format_id']:
                print(f"\n3. 最佳質量組合建議：")
                print(f"   - 格式代碼: {best_video['format_id']}+{best_audio['format_id']}")
                print(f"   - 可獲得 {best_video['quality']}p視頻 + {best_audio['bitrate']:.3f}kbps音頻")
            
            # 詢問下載
            format_id = input("\n請輸入要下載的格式代碼（直接按Enter退出）: ")
            if format_id:
                download_video(url, format_id)
                
        except Exception as e:
            print(f"錯誤: {str(e)}")

if __name__ == "__main__":
    while True :
        url = input("請輸入YouTube視頻URL（直接按Enter退出）: ")
        if url :
            get_format_info(url)
        else :
            sys.exit()
