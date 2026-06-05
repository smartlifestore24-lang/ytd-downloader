from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# --- পেজের রুট সমূহ ---
@app.route('/')
def home(): return render_template('index.html')

@app.route('/youtube')
def youtube(): return render_template('youtube.html')

@app.route('/tiktok')
def tiktok(): return render_template('tiktok.html')

@app.route('/facebook')
def facebook(): return render_template('facebook.html')

@app.route('/instagram')
def instagram(): return render_template('instagram.html')

@app.route('/twitter')
def twitter(): return render_template('twitter.html')

@app.route('/vimeo')
def vimeo(): return render_template('vimeo.html')

@app.route('/likee')
def likee(): return render_template('likee.html')

@app.route('/pinterest')
def pinterest(): return render_template('pinterest.html')

@app.route('/linkedin')
def linkedin(): return render_template('linkedin.html')

@app.route('/snapchat')
def snapchat(): return render_template('snapchat.html')


# --- ১০০% গ্যারান্টিড ইউনিভার্সাল ব্যাকএন্ড লজিক ---
@app.route('/fetch_video', methods=['POST'])
def fetch_video():
    data = request.get_json()
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'দয়া করে একটি সঠিক লিংক দিন!'}), 400

    # এখানে আমরা কুকি ডাটাবেজের লক সিস্টেম বাদ দিয়ে স্ট্যান্ডার্ড মেথড ব্যবহার করছি
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'no_color': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # টাইটেল ও থাম্বনেইল প্রসেসিং
            title = info.get('title') or info.get('description') or 'Social Video'
            if len(title) > 60: 
                title = title[:60] + "..."
                
            thumbnail = info.get('thumbnail') or (info.get('thumbnails')[0]['url'] if info.get('thumbnails') else 'https://placehold.co/600x400?text=Video+Ready')
            
            # ডাউনলোড লিংক খোঁজার প্রফেশনাল ফিল্টার
            download_url = info.get('url')
            if not download_url and info.get('formats'):
                # এমন ফরম্যাট খোঁজা যা সরাসরি প্লে বা ডাউনলোড করা যায়
                valid_formats = [f for f in info['formats'] if f.get('url')]
                if valid_formats:
                    # সবচেয়ে সেরা কোয়ালিটির লিংকটি নেওয়া
                    download_url = valid_formats[-1].get('url')

            if not download_url:
                return jsonify({'error': 'দুঃখিত, এই ভিডিওর মূল ডাউনলোড লিংকটি খুঁজে পাওয়া যায়নি!'}), 404

            return jsonify({
                'title': title,
                'thumbnail': thumbnail,
                'download_url': download_url
            })
            
    except Exception as e:
        # এরর মেসেজটিকে সহজভাবে ফ্রন্টএন্ডে পাঠানো
        return jsonify({'error': f'লিংকটি প্রসেস করা যায়নি। অনুগ্রহ করে লিংকটি আবার চেক করুন!'}), 500

if __name__ == '__main__':
    app.run(debug=True)