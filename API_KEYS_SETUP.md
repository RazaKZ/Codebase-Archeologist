# API Keys Setup Guide

## 🔑 Snyk API Key Kaise Banayein (How to Create Snyk API Key)

### Step 1: Snyk Dashboard Mein Login Karein
1. https://snyk.io par jayein
2. "Sign in" par click karein
3. "Sign in with GitHub" choose karein (aapne pehle se GitHub se signup kiya hai)

### Step 2: Service Account Banayein (API Key Ke Liye)
1. Login ke baad, left sidebar mein **"Settings"** par click karein (aap already yahan hain!)
2. **"General"** tab par jayein (agar nahi hain to)
3. Page ko **neeche scroll karein** - "Organization API key" section tak
4. **"Organization API key"** section mein **"Manage service accounts"** (green button) par click karein
5. New page par:
   - **"Create service account"** ya **"Add service account"** button par click karein
   - Service account ka **name** dein (jaise: "Codebase Archeologist")
   - **Role dropdown empty hai?** Try these:
     - **Option A**: Page refresh karein (F5) aur phir try karein
     - **Option B**: Role field ko skip karein aur directly **"API Key (no expiry)"** select karein
     - **Option C**: Browser cache clear karein aur phir try karein
     - **Option D**: Agar aap organization admin nahi hain, to admin se permission lein
   - **Service account type**: **"API Key (no expiry)"** select karein (recommended)
   - **"Create"** ya **"Save"** par click karein
6. **API Token automatically generate hoga** - isko **immediately copy karein**!
   - ⚠️ **Important**: Yeh token sirf ek baar dikhega, isliye turant copy kar lein
   - Token kuch is tarah dikhega: `snyk_xxxxxxxxxxxxxxxxxxxxx`
7. Token ko safe jagah save kar lein

### ⚠️ Role Dropdown Empty Hai?
Agar Role dropdown mein kuch nahi aa raha, to:
- **Directly "API Key (no expiry)" select karein** - Role ke bina bhi kaam karega
- Ya **Organization Owner/Admin se contact karein** - unhe proper permissions set karne honge
- **Alternative**: Personal API token use karein (next section dekhein)

### Step 3: Token Ko Project Mein Add Karein

#### Option 1: Environment Variable (Recommended)
```bash
# backend folder mein .env file banayein
cd backend
copy env.example .env  # Windows
# ya
cp env.example .env    # Mac/Linux
```

Phir `.env` file mein add karein:
```env
SNYK_API_KEY=your_snyk_token_here
```

#### Option 2: Direct in Code (Not Recommended for Production)
```python
# backend/config/settings.py mein
SNYK_API_KEY = "your_snyk_token_here"
```

### Alternative: Personal Auth Token (Already Available!)
Aapke paas already ek **Auth Token** hai! Yeh use kar sakte hain:

**Your Current Token:**
- Auth Token: `45e0b45d-b9bb-4381-a57f-d50586900110`
- Created: 12 February 2026

**Important Note:**
- ✅ **Auth Token ko API key ki tarah use kar sakte hain!**
- Snyk mein Auth Token aur API Key dono same tarah kaam karte hain
- `.env` file mein `SNYK_API_KEY` ke naam se add karein

**Token Ko Project Mein Add Karein:**
1. `backend` folder mein `.env` file banayein (agar nahi hai)
2. Token add karein:
```env
SNYK_API_KEY=45e0b45d-b9bb-4381-a57f-d50586900110
```

**Ya Naya Token Generate Karein (Agar Chahiye):**
1. "Revoke & Regenerate" (red button) par click karein
2. New token automatically generate hoga
3. **Turant copy karein** - yeh sirf ek baar dikhega!

**Note**: 
- Personal auth token bhi kaam karega API calls ke liye
- Agar token expire ho jaye to "Revoke & Regenerate" se naya bana sakte hain
- Service account zyada secure hai, lekin personal auth token bhi theek hai

---

## 🤖 Gemini API Key Kaise Banayein (How to Create Gemini API Key)

### Step 1: Google AI Studio Mein Jayein
1. https://makersuite.google.com/app/apikey par jayein
2. Google account se login karein

### Step 2: API Key Banayein

**Agar "Failed to create project" Error Aa Raha Hai:**

#### Option A: Existing Project Use Karein
1. **"Create API Key"** button par click karein
2. Dropdown se **existing project** select karein (agar koi hai)
3. API key automatically generate hogi
4. **Key copy karein**

#### Option B: Google Cloud Console Se Project Banayein
1. https://console.cloud.google.com par jayein
2. Top par **project dropdown** par click karein
3. **"New Project"** par click karein
4. Project name dein (jaise: "Codebase Archeologist")
5. **"Create"** par click karein
6. Phir wapas https://makersuite.google.com/app/apikey par jayein
7. **"Create API Key"** par click karein
8. Ab naya project dropdown mein dikhega - select karein
9. API key generate hogi - **copy karein**

#### Option C: Direct API Key Generate (Without Project)
1. https://aistudio.google.com/app/apikey par jayein
2. **"Get API Key"** par click karein
3. Agar project creation fail ho, to:
   - **"Create API key in new project"** try karein
   - Ya **"Create API key in existing project"** se existing project use karein
4. API key generate hogi - **copy karein**

#### Option D: Gemini API Key Alternative URL
1. Direct jayein: https://aistudio.google.com/app/apikey
2. Ya: https://console.cloud.google.com/apis/credentials
3. **"Create Credentials"** > **"API Key"** select karein
4. API key generate hogi

### Step 3: Project Mein Add Karein
`.env` file mein:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### ⚠️ Important Notes
- **Project creation fail ho to**: Existing project use karein ya Google Cloud Console se manually project banayein
- **API key optional hai**: System fallback mode mein bhi kaam karega
- **Free tier available**: Gemini free tier generous hai

---

## ⚠️ Important Notes

### Security
- ❌ **Kabhi bhi API keys ko Git mein commit na karein!**
- ✅ `.env` file ko `.gitignore` mein add karein (already done)
- ✅ Production mein environment variables use karein

### Free Tier Limits
- **Snyk**: Free tier available, limited scans per month
- **Gemini**: Free tier with generous limits

### Fallback Mode
- Agar API keys nahi hain, to bhi system kaam karega
- Business Logic Extractor fallback mode mein kaam karega
- Sabhi features available honge, bas AI-powered descriptions limited honge

---

## 🧪 Testing API Keys

### Snyk Key Test
```bash
curl -H "Authorization: token YOUR_SNYK_TOKEN" https://api.snyk.io/v1/user/me
```

### Gemini Key Test
```python
# Python mein test karein
import httpx

async def test_gemini():
    response = await httpx.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_KEY",
        json={"contents": [{"parts": [{"text": "Hello"}]}]}
    )
    print(response.json())
```

---

## 📝 Complete .env Example

```env
# API Keys (optional - system works in fallback mode without them)
SNYK_API_KEY=snyk_xxxxxxxxxxxxxxxxxxxxx
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxx

# Database
DATABASE_URL=sqlite:///./codebase_archeologist.db

# CORS Origins
CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Analysis Settings
MAX_REPO_SIZE_MB=100
ANALYSIS_TIMEOUT_SECONDS=300
CACHE_TTL_SECONDS=3600

# LLM Settings
LLM_MODEL=gemini-pro
LLM_TEMPERATURE=0.3
LLM_MAX_TOKENS=2000
```

---

## 🆘 Troubleshooting

### Snyk Key Kaam Nahi Kar Raha?
- Token ko verify karein: https://snyk.io/user/me
- Token expire to nahi hua hai check karein
- Organization permissions check karein

### Gemini Key Kaam Nahi Kar Raha?
- API key sahi hai ya nahi verify karein
- Quota exceeded to nahi hai check karein
- Billing enabled hai ya nahi check karein (free tier ke liye bhi)

### Keys Ke Bina Kaam Karega?
- ✅ Haan! System fallback mode mein kaam karega
- Sabhi features available honge
- Bas AI-powered descriptions limited honge

---

**Need help? Check the main README.md or QUICKSTART.md**
