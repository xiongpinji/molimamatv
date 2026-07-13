"""
提示词库数据种子脚本
用于初始化系统预设的分类和提示词数据
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import text


CATEGORIES = [
    {"name": "镜头角度", "slug": "camera-angle", "icon": "Camera", "sort_order": 1, "is_system": True},
    {"name": "光线效果", "slug": "lighting", "icon": "Sunny", "sort_order": 2, "is_system": True},
    {"name": "色彩风格", "slug": "color-style", "icon": "Brush", "sort_order": 3, "is_system": True},
    {"name": "构图方式", "slug": "composition", "icon": "Grid", "sort_order": 4, "is_system": True},
    {"name": "场景描述", "slug": "scene", "icon": "Picture", "sort_order": 5, "is_system": True},
    {"name": "人物描述", "slug": "character", "icon": "User", "sort_order": 6, "is_system": True},
    {"name": "镜头运动", "slug": "camera-movement", "icon": "VideoCamera", "sort_order": 10, "is_system": True},
    {"name": "转场效果", "slug": "transition", "icon": "Switch", "sort_order": 11, "is_system": True},
    {"name": "视频节奏", "slug": "rhythm", "icon": "Timer", "sort_order": 12, "is_system": True},
    {"name": "特效动作", "slug": "effect", "icon": "MagicStick", "sort_order": 13, "is_system": True},
    {"name": "语音风格", "slug": "voice-style", "icon": "Microphone", "sort_order": 20, "is_system": True},
    {"name": "情感语调", "slug": "emotion", "icon": "Mood", "sort_order": 21, "is_system": True},
    {"name": "背景音乐", "slug": "bgm", "icon": "Headset", "sort_order": 22, "is_system": True},
    {"name": "音效", "slug": "sound-effect", "icon": "Bell", "sort_order": 23, "is_system": True},
]

TAGS = [
    {"name": "电影级", "color": "danger"},
    {"name": "专业", "color": "primary"},
    {"name": "新手友好", "color": "success"},
    {"name": "热门", "color": "warning"},
    {"name": "短剧常用", "color": "info"},
    {"name": "Seedance", "color": "primary"},
    {"name": "可灵", "color": "success"},
    {"name": "Sora", "color": "warning"},
]


async def seed_categories(session) -> dict:
    category_map = {}
    for cat in CATEGORIES:
        result = await session.execute(
            text("SELECT id FROM prompt_categories WHERE slug = :slug"),
            {"slug": cat["slug"]}
        )
        existing = result.fetchone()
        if existing:
            category_map[cat["slug"]] = existing[0]
        else:
            cat_id = uuid.uuid4()
            now = datetime.now(timezone.utc)
            await session.execute(
                text("""INSERT INTO prompt_categories (id, name, slug, icon, sort_order, is_system, created_at, updated_at)
                        VALUES (:id, :name, :slug, :icon, :sort_order, :is_system, :now, :now)"""),
                {"id": cat_id, "name": cat["name"], "slug": cat["slug"], "icon": cat.get("icon"),
                 "sort_order": cat.get("sort_order", 0), "is_system": cat.get("is_system", False), "now": now}
            )
            category_map[cat["slug"]] = cat_id
    return category_map


async def seed_tags(session) -> dict:
    tag_map = {}
    for tag in TAGS:
        result = await session.execute(
            text("SELECT id FROM prompt_tags WHERE name = :name"),
            {"name": tag["name"]}
        )
        existing = result.fetchone()
        if existing:
            tag_map[tag["name"]] = existing[0]
        else:
            tag_id = uuid.uuid4()
            now = datetime.now(timezone.utc)
            await session.execute(
                text("""INSERT INTO prompt_tags (id, name, color, created_at, updated_at)
                        VALUES (:id, :name, :color, :now, :now)"""),
                {"id": tag_id, "name": tag["name"], "color": tag.get("color", "default"), "now": now}
            )
            tag_map[tag["name"]] = tag_id
    return tag_map


async def seed_prompts(session, category_map: dict, tag_map: dict):
    system_user_id = uuid.uuid4()
    now = datetime.now(timezone.utc)

    prompts = [
        ("电影级特写镜头", "Extreme close-up shot, cinematic lighting, shallow depth of field, 8K resolution, hyper-realistic, detailed skin texture, dramatic atmosphere", "text2img", "camera-angle", ["电影级", "专业"], True),
        ("中景人物构图", "Medium shot of person, rule of thirds composition, natural lighting, cinematic color grading, professional photography, 4K", "text2img", "camera-angle", ["专业", "短剧常用"], False),
        ("全景环境展示", "Wide establishing shot, panoramic view, epic landscape, golden hour lighting, cinematic aspect ratio, ultra detailed", "text2img", "camera-angle", ["电影级"], False),
        ("低角度仰拍", "Low angle shot looking up, dramatic perspective, powerful imposing presence, sky background, cinematic lighting, heroic composition", "text2img", "camera-angle", ["电影级", "短剧常用"], False),
        ("俯拍鸟瞰视角", "Bird's eye view, aerial perspective, overhead shot, detailed ground texture, geometric patterns, cinematic composition", "text2img", "camera-angle", ["电影级"], False),
        ("过肩镜头", "Over-the-shoulder shot, OTS framing, shallow depth of field, two characters in conversation, cinematic lighting, soft bokeh background", "text2img", "camera-angle", ["电影级", "短剧常用"], False),
        ("金色黄昏光", "Golden hour lighting, warm sunset glow, long shadows, magical atmosphere, soft diffused light, cinematic color grading", "text2img", "lighting", ["电影级", "热门"], True),
        ("戏剧性侧光", "Dramatic side lighting, chiaroscuro effect, strong contrast, deep shadows, Rembrandt lighting, moody atmosphere", "text2img", "lighting", ["电影级", "专业"], False),
        ("柔和自然光", "Soft natural daylight, diffused lighting, even illumination, gentle shadows, natural color temperature, clean aesthetic", "text2img", "lighting", ["新手友好"], False),
        ("霓虹灯光效果", "Neon lighting, cyberpunk aesthetic, colorful reflections, vibrant glow, night scene, urban atmosphere, cinematic", "text2img", "lighting", ["电影级", "热门"], False),
        ("逆光剪影", "Backlit silhouette, strong backlight, rim lighting, dramatic outline, sunset background, emotional atmosphere", "text2img", "lighting", ["电影级"], False),
        ("工作室打光", "Professional studio lighting, three-point lighting setup, softbox, key light fill light back light, commercial photography", "text2img", "lighting", ["专业"], False),
        ("电影胶片色调", "Cinematic film color grading, warm tones, vintage film look, Kodak Portra 400, natural skin tones, soft contrast", "text2img", "color-style", ["电影级", "专业"], True),
        ("冷色调氛围", "Cool blue tones, cold color palette, icy atmosphere, desaturated colors, moody cinematic look, teal and orange", "text2img", "color-style", ["电影级"], False),
        ("高饱和鲜艳", "Vibrant saturated colors, high color intensity, punchy vivid tones, energetic mood, bold color palette", "text2img", "color-style", ["热门"], False),
        ("黑白经典", "Black and white photography, high contrast monochrome, dramatic shadows, timeless classic look, fine art style", "text2img", "color-style", ["电影级", "专业"], False),
        ("日系清新", "Japanese aesthetic, soft pastel colors, light and airy, dreamy atmosphere, overexposed highlights, gentle tones", "text2img", "color-style", ["新手友好", "热门"], False),
        ("三分法构图", "Rule of thirds composition, subject placed at intersection points, balanced frame, professional photography composition", "text2img", "composition", ["专业", "新手友好"], True),
        ("对称构图", "Symmetrical composition, centered subject, mirror reflection, balanced frame, architectural photography style", "text2img", "composition", ["电影级"], False),
        ("引导线构图", "Leading lines composition, converging lines, depth perspective, visual path, dynamic composition, architectural elements", "text2img", "composition", ["专业"], False),
        ("框架构图", "Frame within frame composition, natural framing, doorway window frame, layered depth, visual storytelling", "text2img", "composition", ["电影级"], False),
        ("现代都市夜景", "Modern city nightscape, skyscrapers, neon lights, wet streets reflecting lights, urban atmosphere, cinematic cyberpunk", "text2img", "scene", ["电影级", "短剧常用"], True),
        ("古风庭院场景", "Traditional Chinese courtyard, ancient architecture, red lanterns, cherry blossoms, moonlight, ethereal atmosphere, oriental aesthetic", "text2img", "scene", ["电影级", "短剧常用"], False),
        ("温馨家庭场景", "Cozy home interior, warm lighting, comfortable furniture, soft textures, family atmosphere, inviting space", "text2img", "scene", ["短剧常用"], False),
        ("办公室商务场景", "Modern office space, professional environment, clean design, corporate atmosphere, business meeting room", "text2img", "scene", ["短剧常用"], False),
        ("浪漫户外场景", "Romantic outdoor setting, sunset beach, gentle waves, warm breeze, couple silhouette, dreamy atmosphere", "text2img", "scene", ["电影级", "短剧常用"], False),
        ("优雅女性肖像", "Elegant woman portrait, graceful pose, soft smile, flowing hair, professional makeup, fashion photography, studio lighting", "text2img", "character", ["专业", "短剧常用"], True),
        ("帅气男性肖像", "Handsome man portrait, strong jawline, confident expression, styled hair, sharp features, cinematic lighting, professional photo", "text2img", "character", ["专业", "短剧常用"], False),
        ("可爱儿童肖像", "Cute child portrait, innocent smile, bright eyes, natural expression, soft lighting, playful atmosphere, family photo style", "text2img", "character", ["新手友好", "短剧常用"], False),
        ("古风人物造型", "Traditional Chinese costume, hanfu, elegant ancient style, flowing robes, jade accessories, ethereal beauty, oriental aesthetic", "text2img", "character", ["电影级", "短剧常用"], False),
        ("缓慢推进", "Slow dolly in, gradual camera push forward, subtle movement, building tension, cinematic reveal", "img2video", "camera-movement", ["电影级", "Seedance", "可灵"], True),
        ("环绕拍摄", "Orbiting camera movement, 360 degree orbit, smooth circular motion, dynamic perspective, cinematic orbit shot", "img2video", "camera-movement", ["电影级", "Seedance"], False),
        ("跟随镜头", "Tracking shot, following subject, smooth camera movement, dynamic motion, cinematic pursuit", "img2video", "camera-movement", ["电影级", "可灵"], False),
        ("缓慢拉远", "Slow dolly out, gradual camera pull back, revealing wider scene, establishing shot, cinematic movement", "img2video", "camera-movement", ["电影级", "Seedance", "Sora"], False),
        ("摇镜头", "Pan shot, horizontal camera movement, smooth pan left or right, surveying scene, cinematic pan", "img2video", "camera-movement", ["电影级"], False),
        ("俯冲镜头", "Crane down shot, dramatic descending movement, overhead to ground level, dynamic camera movement", "img2video", "camera-movement", ["电影级", "Seedance"], False),
        ("淡入淡出", "Fade in and fade out transition, smooth opacity change, gentle dissolve, cinematic transition", "img2video", "transition", ["新手友好"], True),
        ("闪白转场", "Flash white transition, bright flash, overexposed moment, dramatic impact, high energy transition", "img2video", "transition", ["电影级", "短剧常用"], False),
        ("模糊转场", "Blur transition, focus pull effect, depth of field change, rack focus, cinematic blur", "img2video", "transition", ["电影级"], False),
        ("时间流逝", "Time lapse transition, accelerated time, day to night, seasonal change, temporal progression", "img2video", "transition", ["电影级", "Seedance"], False),
        ("慢动作特写", "Slow motion, 0.5x speed, cinematic slow-mo, detailed movement, dramatic effect, high frame rate", "img2video", "rhythm", ["电影级", "Seedance", "可灵"], True),
        ("正常节奏", "Normal speed, natural movement, real-time action, standard frame rate, everyday pace", "img2video", "rhythm", ["新手友好"], False),
        ("快节奏剪辑", "Fast paced, quick cuts, energetic rhythm, dynamic editing, action sequence style", "img2video", "rhythm", ["热门", "短剧常用"], False),
        ("风吹发丝飘动", "Gentle wind blowing hair, soft breeze, flowing strands, natural movement, cinematic wind effect", "img2video", "effect", ["电影级", "Seedance", "可灵"], True),
        ("雨滴下落", "Raindrops falling, gentle rain, water droplets, wet surface reflections, atmospheric rain effect", "img2video", "effect", ["电影级"], False),
        ("烟雾弥漫", "Smoke or fog effect, misty atmosphere, ethereal haze, mysterious ambiance, cinematic fog", "img2video", "effect", ["电影级"], False),
        ("光斑闪烁", "Light particles, bokeh effect, sparkle and glimmer, magical atmosphere, fairy light effect", "img2video", "effect", ["电影级", "热门"], False),
        ("人物微笑", "Character smiling, gentle smile, warm expression, natural facial movement, emotional animation", "img2video", "effect", ["可灵", "短剧常用"], False),
        ("人物行走", "Character walking, natural stride, body movement, walking animation, cinematic movement", "img2video", "effect", ["可灵", "Sora"], False),
        ("专业旁白", "Professional narrator voice, clear articulation, steady pace, authoritative tone, documentary style", "tts", "voice-style", ["专业"], True),
        ("温柔女声", "Gentle female voice, soft spoken, warm tone, soothing quality, conversational style", "tts", "voice-style", ["热门", "短剧常用"], False),
        ("磁性男声", "Deep male voice, resonant quality, confident delivery, attractive tone, professional broadcast", "tts", "voice-style", ["热门", "短剧常用"], False),
        ("活泼少女", "Youthful female voice, energetic tone, bright quality, cheerful delivery, animated style", "tts", "voice-style", ["短剧常用"], False),
        ("沉稳长者", "Mature elder voice, wise tone, measured pace, authoritative yet gentle, storytelling quality", "tts", "voice-style", ["短剧常用"], False),
        ("新闻播报", "News anchor voice, formal tone, clear pronunciation, professional broadcast style, serious delivery", "tts", "voice-style", ["专业"], False),
        ("开心愉悦", "Happy and cheerful tone, upbeat delivery, positive energy, smiling voice, joyful expression", "tts", "emotion", ["热门", "短剧常用"], True),
        ("悲伤低落", "Sad and melancholic tone, somber delivery, emotional weight, tearful quality, heartbroken voice", "tts", "emotion", ["电影级", "短剧常用"], False),
        ("愤怒激动", "Angry and intense tone, forceful delivery, heated emotion, confrontational style, passionate voice", "tts", "emotion", ["电影级", "短剧常用"], False),
        ("紧张悬念", "Tense and suspenseful tone, hushed delivery, building anticipation, mysterious quality, thriller style", "tts", "emotion", ["电影级"], False),
        ("温柔深情", "Tender and affectionate tone, loving delivery, intimate quality, heartfelt expression, romantic voice", "tts", "emotion", ["短剧常用"], False),
        ("严肃正式", "Serious and formal tone, professional delivery, authoritative style, business communication, official voice", "tts", "emotion", ["专业"], False),
        ("紧张悬疑配乐", "Tense suspense background music, orchestral strings, building tension, dark atmosphere, thriller soundtrack", "tts", "bgm", ["电影级", "短剧常用"], True),
        ("浪漫抒情配乐", "Romantic emotional music, piano and strings, soft melody, touching atmosphere, love theme soundtrack", "tts", "bgm", ["电影级", "短剧常用"], False),
        ("欢快活泼配乐", "Upbeat cheerful music, positive energy, bright instruments, happy atmosphere, feel-good soundtrack", "tts", "bgm", ["热门"], False),
        ("史诗宏大配乐", "Epic grand orchestral music, powerful brass, dramatic percussion, heroic theme, blockbuster soundtrack", "tts", "bgm", ["电影级"], False),
        ("古风中国风配乐", "Traditional Chinese music, guzheng erhu, oriental melody, ancient atmosphere, cultural soundtrack", "tts", "bgm", ["短剧常用"], False),
        ("环境氛围音", "Ambient atmosphere sound, background environment, natural room tone, spatial audio, immersive soundscape", "tts", "sound-effect", ["专业"], True),
        ("脚步声", "Footsteps sound effect, walking sounds, shoe impact, floor surface variation, natural walking pace", "tts", "sound-effect", ["短剧常用"], False),
        ("门开关声", "Door opening closing sound, latch click, hinge creak, wooden or metal door, entry exit effect", "tts", "sound-effect", ["短剧常用"], False),
        ("手机提示音", "Phone notification sound, message alert, digital tone, modern device sound, attention signal", "tts", "sound-effect", ["短剧常用"], False),
        ("自然环境音", "Natural environment sounds, birds chirping, wind through trees, water flowing, outdoor ambiance", "tts", "sound-effect", ["电影级"], False),
    ]

    for title, content, use_case, cat_slug, tag_names, is_featured in prompts:
        result = await session.execute(
            text("SELECT id FROM user_prompts WHERE title = :title"),
            {"title": title}
        )
        if result.fetchone():
            continue

        prompt_id = uuid.uuid4()
        category_id = category_map.get(cat_slug)
        await session.execute(
            text("""INSERT INTO user_prompts (id, user_id, category_id, title, content, use_case, is_featured, source_type, usage_count, sort_order, is_active, is_public, created_at, updated_at)
                    VALUES (:id, :user_id, :category_id, :title, :content, :use_case, :is_featured, :source_type, 0, 0, true, true, :now, :now)"""),
            {"id": prompt_id, "user_id": system_user_id, "category_id": category_id,
             "title": title, "content": content, "use_case": use_case,
             "is_featured": is_featured, "source_type": "imported", "now": now}
        )

        for tag_name in tag_names:
            tag_id = tag_map.get(tag_name)
            if tag_id:
                await session.execute(
                    text("""INSERT INTO user_prompt_tags (id, prompt_id, tag_id, created_at, updated_at)
                            VALUES (:id, :prompt_id, :tag_id, :now, :now)"""),
                    {"id": uuid.uuid4(), "prompt_id": prompt_id, "tag_id": tag_id, "now": now}
                )
